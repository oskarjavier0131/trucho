from django.urls import path
from trucho_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', views.home, name="Home"),    
]


urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,
                       {'document_root': settings.MEDIA_ROOT}),
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
