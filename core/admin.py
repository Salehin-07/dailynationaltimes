from django.contrib import admin

from core.models import SiteSettings, ContactMessage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "read", "created_at")
    list_filter = ("read",)
    readonly_fields = ("created_at",)
