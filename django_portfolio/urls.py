"""
URL configuration for django_portfolio project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("blog/", include("blog.urls")),
]

# Archivos subidos (imágenes de proyectos/posts). En Railway el disco es
# efímero: los archivos del repositorio se sirven bien, pero lo que se suba
# desde /admin se pierde en cada redeploy salvo que uses un volumen o S3.
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
