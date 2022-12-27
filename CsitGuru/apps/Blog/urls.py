from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from .models import Blog
from .views import (
    BlogCategoryView,
    BlogDetailView,
    BlogSearchEngineView,
    BlogTagView,
    BlogView,
    YourBlogDetailView,
    YourBlogsView,
    add_to_bookmark,
    bookmark_list,
    remove_from_bookmark,
)

blog_dict = {
    "queryset": Blog.modelmanager.filter(visibility="Public"),
}
app_name = "Blog"

urlpatterns = [
    re_path(
       r'^blogs/sitemap\.xml$',
        sitemap,
        {"sitemaps": {"blogs": GenericSitemap(blog_dict, priority=0.8, changefreq="weekly")}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("blogs/addtobookmark/<int:pk>/", add_to_bookmark, name="add-to-bookmark"),
    path("blogs/removefrombookmark/<int:pk>/", remove_from_bookmark, name="remove-from-bookmark"),
    path("user-blogs/", YourBlogsView.as_view(), name="userblogs"),
    path("user-blogs/<int:pk>/<slug:slug>/", YourBlogDetailView.as_view(), name="yourblog_detail"),
    path("blogs/", BlogView.as_view(), name="blogs"),
    path("blogs/search/", BlogSearchEngineView.as_view(), name="blog_search"),
    path("blog_detail/<int:pk>/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    # re_path('blog_detail/(?P<slug>[-\w]+)-(?P<pk>\d+)/$',blog_detail,name="blog_detail"),
    path("blogs/tag/<slug:slug>/", BlogTagView.as_view(), name="blog-tags"),
    path("blogs/category/<category>/", BlogCategoryView.as_view(), name="blog-category"),
    path("blogs/user-bookmarks/", bookmark_list, name="user-bookmarks"),
]
