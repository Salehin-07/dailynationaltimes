from django.urls import path

from editorials import views

app_name = "editorials"

urlpatterns = [
    # Public content
    path("article/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail"),
    # Editorial dashboard & workflow
    path("editorials/", views.dashboard, name="dashboard"),
    path("editorials/posts/new/", views.post_create, name="post_create"),
    path("editorials/posts/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("editorials/posts/<slug:slug>/submit/", views.post_submit, name="post_submit"),
    path("editorials/posts/<slug:slug>/publish/", views.post_publish, name="post_publish"),
    path("editorials/posts/<slug:slug>/archive/", views.post_archive, name="post_archive"),
    path("editorials/posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]
