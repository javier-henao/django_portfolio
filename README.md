# Portafolio personal — Django

Portafolio y blog personal desarrollado con Django y desplegado en Railway.

## Stack

- Python 3.13 + Django 6
- PostgreSQL (Railway) / SQLite en local
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
PostgreSQL para trabajar localmente.

## Despliegue en Railway

El arranque lo hace [`start.sh`](start.sh): aplica migraciones, ejecuta
`collectstatic` y levanta Gunicorn en `0.0.0.0:$PORT`. `Procfile` y
`railway.json` apuntan a ese script.

Variables de entorno necesarias en el servicio:

| Variable        | Valor                                                        |
| --------------- | ------------------------------------------------------------ |
| `SECRET_KEY`    | Clave larga y aleatoria (obligatoria en producción)          |
| `DEBUG`         | `False`                                                      |
| `DATABASE_URL`  | La inyecta Railway al conectar el plugin de PostgreSQL       |
| `ALLOWED_HOSTS` | Opcional; el dominio de Railway se detecta automáticamente   |

> Si en el panel de Railway hay un **Start Command** personalizado, bórralo o
> pon `sh ./start.sh`; de lo contrario se ignoran `Procfile` y `railway.json`,
> no se ejecutan las migraciones y el sitio responde 500.

### Archivos multimedia

En Railway el sistema de archivos es efímero. Las imágenes incluidas en el
repositorio (`media/`) se sirven correctamente, pero las que se suban desde
`/admin` se pierden en cada redeploy. Para persistirlas, monta un volumen en
`/app/media` o configura un almacenamiento externo (S3, Cloudinary, etc.).

## Producción

```bash
python manage.py check --deploy
```
