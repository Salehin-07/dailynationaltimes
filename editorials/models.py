from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("editorials:category_detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("editorials:tag_detail", kwargs={"slug": self.slug})


# Editorial workflow statuses
STATUS_DRAFT = "draft"
STATUS_PENDING = "pending"
STATUS_PUBLISHED = "published"
STATUS_ARCHIVED = "archived"

STATUS_CHOICES = [
    (STATUS_DRAFT, "Draft"),
    (STATUS_PENDING, "Pending Review"),
    (STATUS_PUBLISHED, "Published"),
    (STATUS_ARCHIVED, "Archived"),
]


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    author_name = models.CharField(max_length=200, default="National Times")
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Article body (HTML allowed)")
    featured_image = models.URLField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:240] or "post"
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if self.status == STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        if self.status != STATUS_PUBLISHED:
            self.published_at = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("editorials:post_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == STATUS_PUBLISHED

    def increment_views(self):
        self.views += 1
        self.save(update_fields=["views"])
