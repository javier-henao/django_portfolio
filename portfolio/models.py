from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.fields import CharField, URLField
from django.db.models.fields.files import ImageField


class Project(models.Model):
    title = CharField(max_length=100)
    description = CharField(max_length=150)
    image = ImageField(upload_to="portfolio/images")
    url = URLField(blank=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    """Contenido editable del sitio. Fila única (pk=1)."""

    name = CharField(max_length=80, default="Javier Henao")
    role = CharField(max_length=80, default="Python FullStack Developer")
    hero_sentence = CharField(
        max_length=160,
        default="Ingeniero de software y especialista en ciberseguridad.",
    )
    bio = models.TextField(
        default=(
            "Ingeniero de Software, Especialista en Ciberseguridad y Especialista "
            "en Inteligencia Artificial (en formación), con experiencia en entornos "
            "industriales, optimización de procesos y liderazgo operativo. Poseo "
            "conocimientos en desarrollo backend, análisis de datos, seguridad "
            "informática y metodologías ágiles."
        )
    )
    meta_description = CharField(
        max_length=160,
        default=(
            "Portafolio de Javier Henao, ingeniero de software especializado en "
            "ciberseguridad e inteligencia artificial."
        ),
    )

    project_intro = models.TextField(
        blank=True,
        default=(
            "A continuación encontraras listados todos los proyectos que he "
            "realizado y los que están en desarrollo:"
        )
    )
    cv_heading = CharField(max_length=120, default="El CV completo, en PDF")

    sheet_role = CharField(max_length=80, blank=True, default="Python FullStack Developer")
    sheet_education = CharField(max_length=80, blank=True, default="Ingeniería de Software")
    sheet_specialty = CharField(max_length=80, blank=True, default="Ciberseguridad")
    sheet_learning = CharField(max_length=80, blank=True, default="Inteligencia Artificial")
    sheet_focus = CharField(max_length=80, blank=True, default="Backend, datos y seguridad")

    photo = ImageField(upload_to="photo/", blank=True)
    cv = models.FileField(
        upload_to="cv/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="PDF que se descarga con el botón «Descargar CV».",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "contenido del sitio"
        verbose_name_plural = "contenido del sitio"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
