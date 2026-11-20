import os
import platform
import sys
from pathlib import Path

import django
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from .models import Project


def home(request):
    projects = Project.objects.all()

    return render(request, "home.html", {"projects": projects})


def healthz(request):
    """Diagnóstico temporal: estado de base de datos y estáticos."""
    import traceback

    try:
        return _healthz(request)
    except Exception:  # noqa: BLE001
        return JsonResponse({"fatal": traceback.format_exc()}, status=500)


def _healthz(request):
    db_config = settings.DATABASES.get("default", {})
    info = {
        "ok": True,
        "debug": settings.DEBUG,
        "python": sys.version.split()[0],
        "django": django.get_version(),
        "platform": platform.platform(),
        "db_engine": db_config.get("ENGINE"),
        "db_host": db_config.get("HOST"),
        "db_name": str(db_config.get("NAME")) if db_config.get("NAME") else None,
        "db_options": db_config.get("OPTIONS", {}),
        "env": {
            "DATABASE_URL": bool(os.getenv("DATABASE_URL")),
            "DATABASE_PUBLIC_URL": bool(os.getenv("DATABASE_PUBLIC_URL")),
            "SECRET_KEY": bool(os.getenv("SECRET_KEY")),
            "RAILWAY_PUBLIC_DOMAIN": os.getenv("RAILWAY_PUBLIC_DOMAIN"),
        },
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            info["db"] = "ok"
            tables = sorted(connection.introspection.table_names())
            info["tables"] = tables
            info["has_project_table"] = "portfolio_project" in tables
            if "django_migrations" in tables:
                cursor.execute("SELECT count(*) FROM django_migrations")
                info["migrations_applied"] = cursor.fetchone()[0]
            if "portfolio_project" in tables:
                cursor.execute("SELECT count(*) FROM portfolio_project")
                info["projects"] = cursor.fetchone()[0]
    except Exception as exc:  # noqa: BLE001
        info["ok"] = False
        info["db"] = "error"
        info["db_error"] = f"{type(exc).__name__}: {exc}"[:500]

    static_root = Path(settings.STATIC_ROOT)
    media_root = Path(settings.MEDIA_ROOT)
    info["static_files"] = (
        sum(1 for p in static_root.rglob("*") if p.is_file())
        if static_root.exists()
        else 0
    )
    info["media_files"] = (
        sum(1 for p in media_root.rglob("*") if p.is_file())
        if media_root.exists()
        else 0
    )
    info["allowed_hosts"] = settings.ALLOWED_HOSTS

    return JsonResponse(info, status=200 if info["ok"] else 500)
