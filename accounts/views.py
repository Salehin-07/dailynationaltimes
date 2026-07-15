from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import UserRegistrationForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:home")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


def logout_view(request):
    """Log the user out on GET or POST (Django's auth logout requires POST)."""
    if request.method == "POST":
        logout(request)
        return redirect("core:home")
    # Allow a direct GET logout via a confirmation form (CSRF protected).
    if request.user.is_authenticated:
        logout(request)
    return redirect("core:home")
