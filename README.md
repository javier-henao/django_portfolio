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

## Contenido editable

Desde `/admin/` se gestionan los proyectos, las entradas del blog y el CV:

- **Perfil → CV**: sube el PDF que descargan los botones «Descargar CV».
  Mientras no haya un archivo subido se sirve el PDF del repositorio
  (`portfolio/static/portfolio/Javier_Henao_Software_Cybersecurity_CV.pdf`).
- **Proyectos**: título, descripción, imagen y enlace de cada proyecto.
- **Blog**: entradas con fecha, imagen y contenido.

### Archivos multimedia

En Railway el sistema de archivos es efímero: un CV o una imagen subidos
desde `/admin` desaparecen en el siguiente redeploy (y la fila del Perfil
también, porque la base SQLite vive en el mismo disco). Para conservarlos:

1. Conecta PostgreSQL y referencia `DATABASE_URL` (así persisten los datos).
2. Monta un volumen en `/app/media/cv` para los CV, o en `/data` y define
   `RAILWAY_VOLUME_MOUNT_PATH=/data` (así persisten también la base SQLite y
   los medios). O usa un almacenamiento externo (S3, Cloudinary, etc.).
3. Si no usas volumen, mantén el PDF del repositorio actualizado: es el
   respaldo que se sirve siempre.

### Diagnóstico

`GET /healthz/` devuelve `{"status": "ok", "database": "postgresql"}` (o
`503` si la base no responde).

## Comprobaciones

```bash
python manage.py check --deploy
```
