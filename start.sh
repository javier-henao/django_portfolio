#!/usr/bin/env sh
# Script de arranque para Railway.
# Ejecuta migraciones (crea las tablas si la base está vacía), recolecta los
# archivos estáticos y levanta gunicorn en el puerto que Railway asigna.
set -e

PORT="${PORT:-8000}"
WORKERS="${WEB_CONCURRENCY:-2}"
TIMEOUT="${GUNICORN_TIMEOUT:-60}"

# En Railway el intérprete es `python`; en macOS suele ser `python3`.
if command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  PYTHON=python3
fi

# No abortamos el arranque si la base o los estáticos fallan: preferimos que
# la app levante y poder diagnosticar en /healthz (Railway no muestra logs
# sin iniciar sesión en el panel).
echo "==> Aplicando migraciones"
"$PYTHON" manage.py migrate --noinput || echo "!! migrate falló"

echo "==> Recolectando archivos estáticos"
"$PYTHON" manage.py collectstatic --noinput || echo "!! collectstatic falló"

echo "==> Iniciando gunicorn en 0.0.0.0:${PORT}"
exec gunicorn django_portfolio.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers "${WORKERS}" \
  --timeout "${TIMEOUT}" \
  --access-logfile "-" \
  --error-logfile "-"
