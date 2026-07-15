from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from core.forms import ContactForm
from core.models import ContactMessage
from editorials.models import Post, STATUS_PUBLISHED


def home(request):
    published = Post.objects.filter(status=STATUS_PUBLISHED)
    featured = list(published.filter(is_featured=True)[:4])
    if not featured:
        featured = list(published[:4])
    paginator = Paginator(published, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "core/home.html",
        {"featured": featured, "page_obj": page},
    )


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def search(request):
    query = request.GET.get("q", "").strip()
    results = (
        Post.objects.filter(status=STATUS_PUBLISHED)
        .filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(author_name__icontains=query)
            | Q(tags__name__icontains=query)
        )
        .distinct()
        if query
        else []
    )
    paginator = Paginator(results, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "core/search.html",
        {"query": query, "page_obj": page, "count": len(results)},
    )
