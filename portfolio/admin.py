from django.contrib import admin

from .models import Profile, Project

admin.site.site_header = "Portafolio de Javier Henao"
admin.site.site_title = "Portafolio"
admin.site.index_title = "Contenido"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = ("title", "description")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ("cv", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
