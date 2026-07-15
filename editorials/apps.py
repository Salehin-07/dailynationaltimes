from django.apps import AppConfig


class EditorialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "editorials"

    def ready(self):
        from editorials.permissions import ensure_roles

        ensure_roles()
