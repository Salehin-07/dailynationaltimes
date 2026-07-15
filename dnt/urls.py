from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

import accounts.views
import core.views
import editorials.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/logout/", accounts.views.logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("core.urls")),
    path("", include("editorials.urls")),
]
