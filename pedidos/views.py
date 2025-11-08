from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.db import transaction
from django.conf import settings
from .models import Pedido, LineaPedido
from carro.carro import Carro
from tienda.models import Producto
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


@login_required(login_url="/autentificacion/logear")
def procesar_pedidos(request):
    """Procesa el pedido del usuario autenticado"""
    carro = Carro(request)

    # Validar que el carrito no esté vacío
    if not carro.carro:
        messages.warning(request, "Tu carrito está vacío. Agrega productos antes de realizar un pedido.")
        return redirect("Tienda")

    try:
        with transaction.atomic():
            # Crear un nuevo pedido asociado al usuario autenticado
            pedido = Pedido.objects.create(user=request.user)
            lineas_pedido = []

            # Crear líneas de pedido a partir del carro
            for producto_id, item_data in carro.carro.items():
                producto = get_object_or_404(Producto, id=producto_id)

                # Verificar disponibilidad del producto
                if not producto.disponibilidad:
                    raise ValueError(f"El producto '{producto.nombre}' ya no está disponible")

                lineas_pedido.append(LineaPedido(
                    user=request.user,
                    producto=producto,
                    cantidad=item_data["cantidad"],
                    precio=producto.precio,  # Guardar precio actual
                    pedido=pedido
                ))

            # Guardar todas las líneas de pedido en la base de datos
            LineaPedido.objects.bulk_create(lineas_pedido)

            # Enviar email de confirmación al usuario
            try:
                enviar_email(
                    pedido=pedido,
                    lineas_pedido=lineas_pedido,
                    nombre_usuario=request.user.username,
                    email_usuario=request.user.email
                )
            except Exception as e:
                logger.error(f"Error al enviar email de confirmación: {str(e)}")
                # No fallar el pedido si el email no se envía

            # Limpiar el carro de compras
            carro.limpiar_carro()

            # Mostrar mensaje de éxito y redirigir al usuario
            messages.success(request, f"El pedido #{pedido.id} se ha creado correctamente")
            return redirect("Tienda")

    except ValueError as ve:
        logger.warning(f"Error de validación al procesar pedido: {str(ve)}")
        messages.error(request, str(ve))
        return redirect("Tienda")
    except Exception as e:
        logger.error(f"Error al procesar pedido: {str(e)}")
        messages.error(request, "Hubo un error al procesar tu pedido. Por favor, intenta nuevamente.")
        return redirect("Tienda")


def enviar_email(**kwargs):
    """Envía email de confirmación de pedido al usuario"""
    try:
        # Configurar el asunto del correo
        pedido = kwargs.get('pedido')
        asunto = f"Confirmación de Pedido #{pedido.id}"

        # Renderizar el contenido del correo utilizando una plantilla HTML
        mensaje = render_to_string(
            'email/pedido.html',
            {
                'pedido': pedido,
                'lineas_pedido': kwargs.get('lineas_pedido'),
                'nombre_usuario': kwargs.get('nombre_usuario')
            }
        )

        # Convertir el contenido HTML a texto plano
        mensaje_texto = strip_tags(mensaje)

        # Configurar el remitente y destinatario del correo
        from_email = settings.EMAIL_HOST_USER
        to = kwargs.get('email_usuario')

        if not to:
            logger.warning("No se proporcionó email de usuario para confirmación de pedido")
            return

        # Enviar el correo electrónico
        send_mail(
            asunto,
            mensaje_texto,
            from_email,
            [to],
            html_message=mensaje,
            fail_silently=False
        )

        logger.info(f"Email de confirmación enviado a {to} para pedido #{pedido.id}")
    except Exception as e:
        logger.error(f"Error al enviar email: {str(e)}")
        raise