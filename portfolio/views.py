import os

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from .models import Project


@never_cache
def home(request):
    projects = Project.objects.all()

    return render(request, "home.html", {"projects": projects})


@never_cache
def healthz(request):
    """Comprobación de salud usada por Railway/monitorización."""
    engine = settings.DATABASES.get("default", {}).get("ENGINE", "")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:  # noqa: BLE001
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)

    if "postgresql" in engine:
        storage = "postgresql"
    elif os.getenv("RAILWAY_VOLUME_MOUNT_PATH"):
        storage = "volume"
    else:
        storage = "ephemeral"

    return JsonResponse(
        {
            "status": "ok",
            "database": engine.rsplit(".", 1)[-1] if engine else "unknown",
            "storage": storage,
            "persistent": storage != "ephemeral",
        }
    )
