from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Blog, Category, Comment, Visitior


class SuperBlogModel(admin.ModelAdmin):
    exclude = (
        "contenttype",
        "bookmarks",
    )
    list_display = (
        "title",
        "visibility",
        "id",
        "published_date",
        "last_updated",
        "author",
    )
    list_filter = ["status", "author", "category", "visibility"]
    search_fields = ["title", "description"]

admin.site.register(Blog, SuperBlogModel)  
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register((Category,))
