from django.apps import AppConfig
from django.db.models.signals import post_migrate


class EditorialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "editorials"

    def ready(self):
        from editorials.permissions import ensure_roles

        # Guarantee groups exist at app startup (e.g. production gunicorn).
        ensure_roles()
        # And after every migrate, so a fresh DB is seeded correctly even
        # though ready() runs before the auth tables exist during migrate.
        post_migrate.connect(ensure_roles, sender=self)
