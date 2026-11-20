from django.db import migrations

PROJECTS = [
    {
        "title": "Portafolio Personal",
        "description": "Portafolio personal desarrollado con Django y desplegado en Railway.",
        "image": "portfolio/images/Proyecto_en_construccion_57teEbW.jpg",
        "url": "https://javierhenao.com",
    },
    {
        "title": "Proyecto Web App",
        "description": "Aplicación web desarrollada con Python y Django.",
        "image": "portfolio/images/Proyecto_en_construccion_X8shDL1.jpg",
        "url": "https://github.com/javier-henao/ProyectoWeb.git",
    },
    {
        "title": "Gestion de Citas CASIN",
        "description": "Sistema de gestión de citas para el sector salud.",
        "image": "portfolio/images/Proyecto_en_construccion.jpg",
        "url": "",
    },
]


def seed_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    for project in PROJECTS:
        Project.objects.get_or_create(title=project["title"], defaults=project)


def unseed_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(title__in=[p["title"] for p in PROJECTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_projects, unseed_projects),
    ]
