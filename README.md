# Portafolio personal — Django

Portafolio y blog personal desarrollado con Django y desplegado en Railway.

## Stack

- Python 3.13 + Django 6
- PostgreSQL (Railway) o SQLite
- Gunicorn + WhiteNoise
- Tema claro y oscuro con preferencia guardada en el navegador

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

### Persistencia de datos (importante)

Si no hay PostgreSQL ni volumen, Railway usa un disco efímero y **lo que se
edite en `/admin` se pierde en cada despliegue**. Hay dos formas de evitarlo:

1. **PostgreSQL** (recomendado): conecta el servicio de Postgres y referencia
   `DATABASE_URL = ${{Postgres.DATABASE_URL}}` en las variables del servicio
   web. Los datos quedan en la base.
2. **Volumen de Railway**: añade un volumen al servicio con mount path
   `/data`. Railway inyecta `RAILWAY_VOLUME_MOUNT_PATH`; la app guarda ahí
   `db.sqlite3` y los medios. En el primer arranque copia las imágenes del
   repositorio al volumen; los archivos subidos desde `/admin` se conservan.

El proyecto usa PostgreSQL si existe `DATABASE_URL` (o `DATABASE_PUBLIC_URL`,
o las variables `PGHOST`/`PGUSER`/…). En caso contrario cae en SQLite dentro
de `RAILWAY_VOLUME_MOUNT_PATH` o, si no hay volumen, en el directorio de la
app.

## Contenido editable

Desde `/admin/` se gestiona todo el contenido visible sin tocar código:

- **Contenido del sitio** (fila única): nombre, cargo, retrato, frase de
  portada, bio, ficha del perfil (rol, formación, especialidad, en curso y
  enfoque), introducción de proyectos, texto y PDF del CV y meta descripción.
  Deja vacía una fila de la ficha para ocultarla.
- **Proyectos**: título, descripción, imagen y enlace.
- **Blog**: entradas con fecha, imagen y contenido.

Los botones «Descargar CV» usan el PDF subido; si no hay ninguno, sirven el
del repositorio (`portfolio/static/portfolio/Javier_Henao_Software_Cybersecurity_CV.pdf`).

### Modo claro y oscuro

El tema sigue la preferencia del sistema y el botón del nav la cambia; la
elección se guarda en `localStorage`. Todos los colores salen de
`portfolio/static/tokens.css` (bloque `:root` para oscuro y
`html[data-theme="light"]` para claro).

Al cambiar CSS o JS, sube `ASSET_VERSION` en `django_portfolio/settings.py`
(o define la variable `ASSET_VERSION`): las URLs llevan `?v=` para romper la
caché del navegador.

### Diagnóstico

`GET /healthz/` devuelve `{"status": "ok", "database": "sqlite3"}` (o `503`
si la base no responde).

## Comprobaciones

```bash
python manage.py check --deploy
```
