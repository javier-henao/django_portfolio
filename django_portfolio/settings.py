"""
Django settings for django_portfolio project.

Configuración preparada para desarrollo local y despliegue en Railway.
"""

from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    """Lee un booleano desde una variable de entorno."""
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str) -> list[str]:
    """Lee una lista separada por comas desde una variable de entorno."""
    return [item.strip() for item in os.getenv(name, "").split(",") if item.strip()]


# SECURITY WARNING: keep the secret key used in production secret!
# En Railway define SECRET_KEY con un valor largo y aleatorio.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-local-dev-only-of5r@jje-f!n@t08jr0fcn*d#_fct_&k*2t1_q1py",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool("DEBUG", False)


# Hosts permitidos. Railway inyecta RAILWAY_PUBLIC_DOMAIN automáticamente.
_default_hosts = [
    "localhost",
    "127.0.0.1",
    "www.javierhenao.com",
    "javierhenao.com",
    "web-production-1ee9b.up.railway.app",
    ".up.railway.app",  # dominios/preview de Railway
]

_railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
if _railway_domain:
    _default_hosts.append(_railway_domain)

ALLOWED_HOSTS = list(dict.fromkeys(_default_hosts + env_list("ALLOWED_HOSTS")))

# Orígenes de confianza para CSRF (deben incluir esquema y host válidos).
_default_csrf_origins = [
    "https://www.javierhenao.com",
    "https://javierhenao.com",
    "https://web-production-1ee9b.up.railway.app",
    "https://*.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = list(
    dict.fromkeys(_default_csrf_origins + env_list("CSRF_TRUSTED_ORIGINS"))
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "blog",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_portfolio.wsgi.application"


# Database
# Prioriza la URL privada de Railway (DATABASE_URL); DATABASE_PUBLIC_URL
# queda como respaldo. Sin ninguna de las dos usa SQLite (desarrollo local).

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_PUBLIC_URL")

if DATABASE_URL:
    _db_config = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )

    # Railway exige TLS en la URL pública (proxy TCP). En la red interna
    # (*.railway.internal) la conexión va sin TLS.
    if DATABASE_URL.startswith(("postgres://", "postgresql://")):
        _host = (_db_config.get("HOST") or "").split(":")[0]
        _is_internal = _host.endswith(".railway.internal") or _host in {
            "localhost",
            "127.0.0.1",
        }
        _options = _db_config.setdefault("OPTIONS", {})
        if not _is_internal and "sslmode" not in _options:
            _options["sslmode"] = "require"

    DATABASES = {"default": _db_config}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# STORAGES reemplaza a STATICFILES_STORAGE (eliminado en Django 5.1+).
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Seguridad detrás del proxy de Railway
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG


# Logs a stdout para verlos en Railway
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
