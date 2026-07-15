from django.apps import AppConfig
from django.db.models.signals import post_migrate


class EditorialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "editorials"

    def ready(self):
        from editorials.permissions import ensure_roles

        # Seed the editorial role groups after every migrate. During the
        # migrate command django.setup() runs before the auth tables exist,
        # so we must not query the DB here.
        post_migrate.connect(ensure_roles, sender=self)
