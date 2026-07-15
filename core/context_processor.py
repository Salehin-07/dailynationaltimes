from core.models import SiteSettings
from editorials.models import Category, Post
from editorials.permissions import ROLE_EDITOR, ROLE_SUB_EDITOR, user_roles
from ads.models import Ad


def site_context(request):
    settings = SiteSettings.get_settings()
    categories = list(Category.objects.all())
    popular = list(
        Post.objects.filter(status="published").order_by("-views")[:5]
    )
    ads = list(Ad.objects.filter(active=True))
    ads_by_slot = {}
    for ad in ads:
        ads_by_slot.setdefault(ad.slot, []).append(ad)
    roles = user_roles(request.user)
    can_manage_all = ROLE_EDITOR in roles or ROLE_SUB_EDITOR in roles
    return {
        "site_settings": settings,
        "categories": categories,
        "popular_posts": popular,
        "ads_by_slot": ads_by_slot,
        "roles": roles,
        "can_manage_all": can_manage_all,
    }
