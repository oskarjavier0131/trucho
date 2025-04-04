from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

app_name = "carro"

urlpatterns = [    
    path("agregar/<int:producto_id>/", views.agregar_producto, name="agregar"),
    path("eliminar/<int:producto_id>/", views.eliminar_producto, name="eliminar"),
    path("restar/<int:producto_id>/", views.restar_producto, name="restar"),
    path("limpiar/", views.limpiar_carro, name="limpiar"),    
]


urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,
                       {'document_root': settings.MEDIA_ROOT}),
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
