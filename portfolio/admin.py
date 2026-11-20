from django.contrib import admin

from .models import Profile, Project

admin.site.site_header = "Portafolio"
admin.site.site_title = "Portafolio"
admin.site.index_title = "Contenido"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = ("title", "description")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Identidad",
            {
                "fields": ("name", "role", "photo"),
                "description": "Nombre, cargo y retrato que encabezan el sitio.",
            },
        ),
        ("Portada", {"fields": ("hero_sentence",)}),
        (
            "Perfil",
            {
                "fields": (
                    "bio",
                    "sheet_role",
                    "sheet_education",
                    "sheet_specialty",
                    "sheet_learning",
                    "sheet_focus",
                ),
                "description": "La bio y las filas de la ficha. Deja una fila vacía para ocultarla.",
            },
        ),
        (
            "Proyectos y CV",
            {
                "fields": ("project_intro", "cv", "cv_heading"),
            },
        ),
        (
            "Buscadores",
            {
                "fields": ("meta_description",),
            },
        ),
        ("Registro", {"fields": ("updated_at",)}),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
