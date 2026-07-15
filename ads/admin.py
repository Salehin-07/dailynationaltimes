from django.contrib import admin

from ads.models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("name", "slot", "active", "order")
    list_filter = ("slot", "active")
