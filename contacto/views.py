from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ContactoForms
from django.core.mail import EmailMessage

def contacto(request):
    formulario_contacto = ContactoForms()

    if request.method == "POST":
        formulario_contacto = ContactoForms(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            contenido = request.POST.get("contenido")

            email_message = EmailMessage(
                "Mensaje desde TruchoApp",
                f"El usuario con nombre {nombre} con la dirección {email} escribe lo siguiente:\n\n {contenido}",
                "", ["lubianka01@gmail.com"],
                reply_to=[email]
            )
            try:
                email_message.send() 
                return HttpResponseRedirect("/contacto/?valido=True")
            except:
                return HttpResponseRedirect("/contacto/?valido=False")

    return render(request, "contacto/contacto.html", {'formulario': formulario_contacto})
