from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from editorials.forms import PostForm
from editorials.models import (
    STATUS_ARCHIVED,
    STATUS_DRAFT,
    STATUS_PENDING,
    STATUS_PUBLISHED,
    Category,
    Post,
    Tag,
)
from editorials.permissions import (
    ROLE_EDITOR,
    ROLE_REPORTER,
    ROLE_SUB_EDITOR,
    role_required,
    user_roles,
)


# ---------------------------------------------------------------------------
# Public-facing views
# ---------------------------------------------------------------------------

def post_detail(request, slug):
    from django.utils.html import strip_tags

    post = get_object_or_404(Post, slug=slug)
    if not post.is_published and not (
        request.user.is_authenticated
        and (ROLE_EDITOR in user_roles(request.user) or post.author == request.user)
    ):
        return redirect("core:home")
    if post.is_published:
        post.increment_views()
    related = (
        Post.objects.filter(status=STATUS_PUBLISHED, category=post.category)
        .exclude(pk=post.pk)
        .order_by("-published_at")[:4]
    )
    words = len(strip_tags(post.content or "").split())
    read_time = max(1, round(words / 200))
    return render(
        request,
        "editorials/post_detail.html",
        {"post": post, "related": related, "read_time": read_time},
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status=STATUS_PUBLISHED, category=category)
    paginator = Paginator(posts, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "editorials/category.html",
        {"category": category, "page_obj": page},
    )


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status=STATUS_PUBLISHED, tags=tag)
    paginator = Paginator(posts, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "editorials/tag.html",
        {"tag": tag, "page_obj": page},
    )


# ---------------------------------------------------------------------------
# Editorial dashboard & workflow (role based)
# ---------------------------------------------------------------------------

@role_required(ROLE_REPORTER, ROLE_SUB_EDITOR, ROLE_EDITOR)
def dashboard(request):
    roles = user_roles(request.user)
    can_manage_all = ROLE_EDITOR in roles or ROLE_SUB_EDITOR in roles
    can_publish = ROLE_EDITOR in roles
    can_delete_own = ROLE_REPORTER in roles
    view_all = request.GET.get("view") == "all" and can_manage_all

    if view_all:
        qs = Post.objects.all()
    else:
        qs = Post.objects.filter(author=request.user)
    qs = qs.order_by("-updated_at")

    # Personal statistics (always scoped to the current user)
    my = Post.objects.filter(author=request.user)
    stats = {
        "total": my.count(),
        "draft": my.filter(status=STATUS_DRAFT).count(),
        "pending": my.filter(status=STATUS_PENDING).count(),
        "published": my.filter(status=STATUS_PUBLISHED).count(),
        "archived": my.filter(status=STATUS_ARCHIVED).count(),
        "views": sum(p.views for p in my),
    }

    page_obj = Paginator(qs, 10).get_page(request.GET.get("page"))

    return render(
        request,
        "editorials/dashboard.html",
        {
            "posts": page_obj,
            "page_obj": page_obj,
            "roles": roles,
            "stats": stats,
            "view_all": view_all,
            "can_manage_all": can_manage_all,
            "can_publish": can_publish,
            "can_delete_all": can_manage_all,
            "can_delete_own": can_delete_own,
            "title": "All Posts" if view_all else "Dashboard",
        },
    )


@role_required(ROLE_REPORTER, ROLE_SUB_EDITOR, ROLE_EDITOR)
def post_create(request):
    roles = user_roles(request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Reporters may only save drafts; others may submit for review.
            if ROLE_EDITOR not in roles and ROLE_SUB_EDITOR not in roles:
                post.status = STATUS_DRAFT
            image = form.cleaned_data.get("image")
            if image:
                from editorials.github_storage import upload_image, GitHubStorageError

                try:
                    post.featured_image = upload_image(image)
                except GitHubStorageError as exc:
                    form.add_error("image", str(exc))
                    return render(
                        request,
                        "editorials/post_form.html",
                        {"form": form, "title": "New Post"},
                    )
            post.save()
            form.save_m2m()
            messages.success(request, "Post saved.")
            return redirect("editorials:dashboard")
    else:
        form = PostForm()
    return render(request, "editorials/post_form.html", {"form": form, "title": "New Post"})


@role_required(ROLE_REPORTER, ROLE_SUB_EDITOR, ROLE_EDITOR)
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    roles = user_roles(request.user)
    # Reporters can only edit their own posts; managers can edit any.
    if ROLE_EDITOR not in roles and ROLE_SUB_EDITOR not in roles:
        if post.author != request.user:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            image = form.cleaned_data.get("image")
            if image:
                from editorials.github_storage import upload_image, GitHubStorageError

                try:
                    post.featured_image = upload_image(image)
                except GitHubStorageError as exc:
                    form.add_error("image", str(exc))
                    return render(
                        request,
                        "editorials/post_form.html",
                        {"form": form, "post": post, "title": "Edit Post"},
                    )
            form.save()
            messages.success(request, "Post updated.")
            return redirect("editorials:dashboard")
    else:
        form = PostForm(instance=post)
    return render(request, "editorials/post_form.html", {"form": form, "post": post, "title": "Edit Post"})


@role_required(ROLE_SUB_EDITOR, ROLE_EDITOR)
def post_submit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.status == STATUS_DRAFT:
        post.status = STATUS_PENDING
        post.save(update_fields=["status"])
        messages.success(request, "Post submitted for review.")
    return redirect("editorials:dashboard")


@role_required(ROLE_EDITOR)
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.status = STATUS_PUBLISHED
    post.save(update_fields=["status"])
    messages.success(request, "Post published.")
    return redirect("editorials:dashboard")


@role_required(ROLE_EDITOR)
def post_archive(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.status = STATUS_ARCHIVED
    post.save(update_fields=["status"])
    messages.success(request, "Post archived.")
    return redirect("editorials:dashboard")


@role_required(ROLE_REPORTER, ROLE_SUB_EDITOR, ROLE_EDITOR)
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    roles = user_roles(request.user)
    is_manager = ROLE_SUB_EDITOR in roles or ROLE_EDITOR in roles
    # Reporters may only delete their own posts; managers may delete any.
    if not is_manager and post.author != request.user:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("editorials:dashboard")
    return render(request, "editorials/post_confirm_delete.html", {"post": post})
