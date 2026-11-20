from django.conf import settings
from django.templatetags.static import static

from .models import Profile

DEFAULT_CV = "portfolio/Javier_Henao_Software_Cybersecurity_CV.pdf"
DEFAULT_PHOTO = "portfolio/foto.jpg"


def site_content(request):
    """Contenido editable y versión de assets para todas las plantillas."""
    site = Profile.objects.first() or Profile()

    return {
        "site": site,
        "cv_url": site.cv.url if site.cv else static(DEFAULT_CV),
        "photo_url": site.photo.url if site.photo else static(DEFAULT_PHOTO),
        "asset_version": settings.ASSET_VERSION,
    }
