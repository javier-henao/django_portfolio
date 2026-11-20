import datetime

from django.db import migrations


def seed_posts(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.get_or_create(
        title="Bienvenido al blog",
        defaults={
            "description": (
                "Este es el primer post del blog. Aquí compartiré contenido "
                "sobre desarrollo de software, ciberseguridad e inteligencia "
                "artificial."
            ),
            "image": "blog/images/Proyecto_en_construccion.jpg",
            "date": datetime.date.today(),
        },
    )


def unseed_posts(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(title="Bienvenido al blog").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_posts, unseed_posts),
    ]
