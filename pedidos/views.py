from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import Pedido, LineaPedido
from carro.carro import Carro
from tienda.models import Producto
from django.contrib import messages

@login_required(login_url="/autentificacion/logear")
def procesar_pedidos(request):
    # Crear un nuevo pedido asociado al usuario autenticado
    pedido = Pedido.objects.create(user=request.user)
    carro = Carro(request)  # Obtener el carro de compras del usuario
    lineas_pedido = list()  # Lista para almacenar las líneas de pedido
    
    # Crear líneas de pedido a partir del carro
    for key, value in carro.carro.items():
        producto = Producto.objects.get(id=key)  # Obtener el producto por su ID
        lineas_pedido.append(LineaPedido(
            user=request.user,  # Asignar el usuario autenticado
            producto=producto,
            cantidad=value["cantidad"],
            pedido=pedido
        ))
    
    # Guardar todas las líneas de pedido en la base de datos
    LineaPedido.objects.bulk_create(lineas_pedido)

    # Enviar email de confirmación al usuario
    enviar_email(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombre_usuario=request.user.username,
        email_usuario=request.user.email
    )

    # Limpiar el carro de compras
    carro.limpiar_carro()

    # Mostrar mensaje de éxito y redirigir al usuario
    messages.success(request, "El pedido se ha creado correctamente")
    return redirect("procesar_pedidos")


def enviar_email(**kwargs):
    # Configurar el asunto del correo
    asunto = "Pedido recibido"
    
    # Renderizar el contenido del correo utilizando una plantilla HTML
    mensaje = render_to_string(
        'email/pedido.html',
        {
            'pedido': kwargs.get('pedido'),
            'lineas_pedido': kwargs.get('lineas_pedido'),
            'nombre_usuario': kwargs.get('nombre_usuario')
        }
    )

    # Convertir el contenido HTML a texto plano
    mensaje_texto = strip_tags(mensaje)
    
    # Configurar el remitente y destinatario del correo
    from_email = "lubianka01@gmail.com"
    to = kwargs.get('email_usuario', "lubianka01@gmail.com")  # Email del usuario o fallback

    # Enviar el correo electrónico
    send_mail(
        asunto,
        mensaje_texto,
        from_email,
        [to],
        html_message=mensaje,
        fail_silently=False  # Lanzar un error si el correo no se envía
    )