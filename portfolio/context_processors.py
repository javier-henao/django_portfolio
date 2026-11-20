from django.conf import settings
from django.templatetags.static import static

from .models import Profile

DEFAULT_CV = "portfolio/Javier_Henao_Software_Cybersecurity_CV.pdf"


def site_profile(request):
    """Expone el CV vigente y la versión de los assets a todas las plantillas."""
    profile = Profile.objects.first()

    if profile and profile.cv:
        cv_url = profile.cv.url
    else:
        cv_url = static(DEFAULT_CV)

    return {
        "site_profile": profile,
        "cv_url": cv_url,
        "asset_version": settings.ASSET_VERSION,
    }
