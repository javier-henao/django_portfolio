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
    """Datos editables del propietario. Fila única (pk=1)."""

    cv = models.FileField(
        upload_to="cv/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="PDF que se descarga con el botón «Descargar CV».",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfil"

    def __str__(self):
        return "Perfil"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
