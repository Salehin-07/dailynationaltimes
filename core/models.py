from django.db import models


class SiteSettings(models.Model):
    name = models.CharField(max_length=200, default="The Daily National Times")
    logo = models.URLField(
        max_length=500,
        blank=True,
        default="https://blogger.googleusercontent.com/img/a/AVvXsEgfNjTco0DS8LPt5dif0d1AcQnZa3O1QlTr3tFg9AIRZBUMnSVVaMZFGBX76xbMNrn4e_BkWQ5inC8CiEyl_yJQzUBgZ03JUg4tfUHZlLwoOiork6s1ATXdkOhCiky0aZ6h3uY8CckSHf_RWDpPVq9UrWUVwU3sHFBXUqKOsoeHNBh1UxBUqboW9Z8Xyd2k=s720",
    )
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(
        max_length=300,
        blank=True,
        default="© Copyright: The Daily National Times | Editor & Publisher: Samir Talukdar",
    )
    facebook = models.URLField(max_length=300, blank=True, default="https://facebook.com/")
    twitter = models.URLField(max_length=300, blank=True, default="https://x.com/")
    instagram = models.URLField(max_length=300, blank=True, default="https://www.instagram.com/")
    youtube = models.URLField(max_length=300, blank=True, default="https://youtube.com/")
    telegram = models.URLField(max_length=300, blank=True, default="https://telegram.me/")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.name

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def social_links(self):
        return [
            ("facebook", self.facebook, "bi-facebook"),
            ("twitter-x", self.twitter, "bi-twitter-x"),
            ("youtube", self.youtube, "bi-youtube"),
            ("instagram", self.instagram, "bi-instagram"),
            ("telegram", self.telegram, "bi-telegram"),
        ]


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
