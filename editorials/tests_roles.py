from django.contrib.auth.models import Group
from django.test import TestCase

from editorials.permissions import EDITORIAL_ROLES, ensure_roles


class EditorialRolesTests(TestCase):
    def test_ensure_roles_creates_all(self):
        Group.objects.all().delete()
        self.assertEqual(Group.objects.count(), 0)
        ensure_roles()
        self.assertEqual(
            sorted(Group.objects.values_list("name", flat=True)),
            sorted(EDITORIAL_ROLES),
        )

    def test_ensure_roles_is_idempotent(self):
        ensure_roles()
        before = sorted(Group.objects.values_list("name", flat=True))
        ensure_roles()
        self.assertEqual(sorted(Group.objects.values_list("name", flat=True)), before)
        self.assertEqual(Group.objects.count(), len(EDITORIAL_ROLES))
