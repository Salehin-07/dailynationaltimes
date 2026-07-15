from functools import wraps

from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


# Editorial roles (Django groups)
ROLE_REPORTER = "Reporter"
ROLE_SUB_EDITOR = "SubEditor"
ROLE_EDITOR = "Editor"

EDITORIAL_ROLES = [ROLE_REPORTER, ROLE_SUB_EDITOR, ROLE_EDITOR]


def ensure_roles():
    """Create the editorial role groups if they do not exist yet."""
    from django.db.utils import OperationalError

    try:
        for role in EDITORIAL_ROLES:
            Group.objects.get_or_create(name=role)
    except OperationalError:
        # Database / tables not ready yet (e.g. during makemigrations).
        pass


def user_roles(user):
    if not user.is_authenticated:
        return set()
    return set(user.groups.values_list("name", flat=True))


def role_required(*roles):
    """Decorator: require the logged-in user to belong to one of ``roles``."""

    def decorator(view):
        @wraps(view)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if not (set(roles) & user_roles(request.user)):
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return _wrapped

    return decorator
