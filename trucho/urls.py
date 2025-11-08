from django.contrib import admin
from django.urls import path, include
from django.conf import settings


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

# Add debug toolbar URLs in DEBUG mode
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
