from .forms import BlogSearchForm
from .models import Blog, Category


def blogfilters(request):
    return {
        "form": BlogSearchForm(),
        "categories": Category.objects.all(),
        "popularblogs": Blog.modelmanager.order_by("-total_views")[0:4],
        "recentblogs": Blog.modelmanager.order_by("-published_date")[0:4],
    }
