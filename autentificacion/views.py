from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages


class VRegistroUsuario(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registro/registro.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('Home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
                
            return render(request, 'registro/registro.html', {'form': form})
        
def cerrar_sesion(request):
    logout(request)
    return redirect('Home')

def iniciar_sesion(request):  # Cambiamos el nombre de la vista
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get('username')
            contrasena = form.cleaned_data.get('password')
            usuario = authenticate(username=nombre_usuario, password=contrasena)
            if usuario is not None:
                auth_login(request, usuario)  # Usamos auth_login en lugar de login
                return redirect('Home')
            else:
                messages.error(request, 'Usuario o contraseña incorrecta')
        else:
            messages.error(request, 'Información incorrecta')
    form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})    