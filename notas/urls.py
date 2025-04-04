from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', views.notas, name="Notas"),
    path('categoria/<int:categoria_id>', views.categoria, name="categoria"),
]


urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,
                       {'document_root': settings.MEDIA_ROOT}),
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
