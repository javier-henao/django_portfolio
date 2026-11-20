# Portafolio personal — Django

Portafolio y blog personal desarrollado con Django y desplegado en Railway.

## Stack

- Python 3.13 + Django 6
- PostgreSQL (Railway) o SQLite
- Gunicorn + WhiteNoise
- Bootstrap 5

## Desarrollo local

```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements.txt

cp .env.example .env          # ajusta SECRET_KEY y DEBUG=True
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sin `DATABASE_URL` la aplicación usa `db.sqlite3`, así que no necesitas
PostgreSQL para trabajar localmente. Las migraciones de datos crean los
proyectos y el primer post de ejemplo.

## Despliegue en Railway

El arranque lo hace [`start.sh`](start.sh): aplica migraciones, ejecuta
`collectstatic`, crea el superusuario si hace falta y levanta Gunicorn en
`0.0.0.0:$PORT`. `Procfile` y `railway.json` apuntan a ese script.

Variables de entorno recomendadas en el servicio:

| Variable                      | Valor                                                        |
| ----------------------------- | ------------------------------------------------------------ |
| `SECRET_KEY`                  | Clave larga y aleatoria (obligatoria)                        |
| `DEBUG`                       | `False`                                                      |
| `DATABASE_URL`                | Referencia `${{Postgres.DATABASE_URL}}` (recomendado)        |
| `DJANGO_SUPERUSER_USERNAME`   | Usuario del admin que se crea al arrancar                    |
| `DJANGO_SUPERUSER_PASSWORD`   | Contraseña de ese usuario                                    |
| `DJANGO_SUPERUSER_EMAIL`      | Correo del usuario                                           |

`ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` detectan el dominio de Railway
(`RAILWAY_PUBLIC_DOMAIN`) y el dominio propio `javierhenao.com`.

### Base de datos

El proyecto usa PostgreSQL si existe `DATABASE_URL` (o `DATABASE_PUBLIC_URL`,
o las variables `PGHOST`/`PGUSER`/…). En caso contrario cae en SQLite.

Si el servicio no tiene PostgreSQL conectado, la base SQLite vive en el
sistema de archivos efímero de Railway: **los cambios hechos desde `/admin`
se pierden en cada redeploy**. Para evitarlo:

1. Conecta un servicio PostgreSQL y referencia su `DATABASE_URL` en las
   variables del servicio web (opción recomendada), o
2. monta un volumen de Railway: la app guarda `db.sqlite3` en
   `RAILWAY_VOLUME_MOUNT_PATH`.

### Archivos multimedia

Las imágenes incluidas en el repositorio (`media/`) se sirven bien, pero las
que se suban desde `/admin` también necesitan un volumen en `/app/media` o un
almacenamiento externo (S3, Cloudinary, etc.).

### Diagnóstico

`GET /healthz/` devuelve `{"status": "ok", "database": "postgresql"}` (o
`503` si la base no responde).

## Comprobaciones

```bash
python manage.py check --deploy
```
