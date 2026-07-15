from django.db import models


class Ad(models.Model):
    SLOT_HOME_TOP = "home_top"
    SLOT_HOME_MID = "home_mid"
    SLOT_SIDEBAR = "sidebar"
    SLOT_ARTICLE_BOTTOM = "article_bottom"
    SLOT_FOOTER = "footer"

    SLOT_CHOICES = [
        (SLOT_HOME_TOP, "Home Top Banner"),
        (SLOT_HOME_MID, "Home Middle"),
        (SLOT_SIDEBAR, "Sidebar"),
        (SLOT_ARTICLE_BOTTOM, "Article Bottom"),
        (SLOT_FOOTER, "Footer"),
    ]

    name = models.CharField(max_length=150)
    slot = models.CharField(max_length=30, choices=SLOT_CHOICES, default=SLOT_SIDEBAR)
    image_url = models.URLField(max_length=600, blank=True)
    link = models.URLField(max_length=600, blank=True)
    html = models.TextField(
        blank=True, help_text="Raw ad HTML (e.g. AdSense snippet). Used when set."
    )
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["slot", "order"]

    def __str__(self):
        return f"{self.name} ({self.get_slot_display()})"
