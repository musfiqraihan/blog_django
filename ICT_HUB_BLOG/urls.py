from django.conf.urls import url
from django.views.static import serve

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include("userapp.urls")),
    path('', include("blogapp.urls")),

    url(r'^media/(?P<path>.*)$', serve, {'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
