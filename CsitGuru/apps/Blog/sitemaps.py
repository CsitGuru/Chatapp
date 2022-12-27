from django.contrib.sitemaps import Sitemap

from .models import Blog


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Blog.modelmanager.all()

    def lastmodified(self, obj):
        return obj.last_updated
