from django.urls import path
from .views import VRegistroUsuario, cerrar_sesion, iniciar_sesion
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

urlpatterns = [    
    path('', VRegistroUsuario.as_view(), name="Autentificacion"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
    path('login', iniciar_sesion, name="login"), 
]

urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,
                       {'document_root': settings.MEDIA_ROOT}),
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
