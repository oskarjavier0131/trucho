from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('servicios/', include('servicios.urls')),
    path('notas/', include('notas.urls')),
    path('contacto/', include('contacto.urls')),
    path('tienda/', include('tienda.urls')),
    path('carro/', include('carro.urls')),
    path('', include('trucho_app.urls')),
    path('autentificacion/', include('autentificacion.urls')),
    path('pedidos/', include('pedidos.urls')),
]
