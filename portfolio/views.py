from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from .models import Project


def home(request):
    projects = Project.objects.all()

    return render(request, "home.html", {"projects": projects})


def healthz(request):
    """Comprobación de salud usada por Railway/monitorización."""
    engine = settings.DATABASES.get("default", {}).get("ENGINE", "")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:  # noqa: BLE001
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)

    return JsonResponse(
        {
            "status": "ok",
            "database": engine.rsplit(".", 1)[-1] if engine else "unknown",
        }
    )
