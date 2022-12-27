import readtime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager


def blog_image_directory_path():
    return "Blogs/"


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = _("Categories")
    def __str__(self):
        return str(self.name)


class Visitior(models.Model):
    ipaddress = models.CharField(null=True, max_length=100)

    def __str__(self) -> str:
        return self.ipaddress


class Blog(models.Model):
    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    def get_absolute_url(self):
        return reverse("Blog:blog_detail", kwargs={"pk": self.id, "slug": self.slug})

    def get_private_url(self):
        return reverse("Blog:yourblog_detail", kwargs={"pk": self.id, "slug": self.slug})

    visibilitymode = (
        ("Private", "Private"),
        ("Public", "Public"),
    )

    class CustomManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(visibility="Public", status="published")

    contenttype = models.CharField(default="Blog", max_length=50)
    visibility = models.CharField(
        max_length=20,
        choices=visibilitymode,
        default="public",
        help_text="<p style='color:#b1b1b1;'>Private -> Only You can see this Blog.</p><p style='color:#b1b1b1;'>Public -> Anyone on the internet can see this Blog.</p>",
        verbose_name="type",
    )
    title = models.CharField(max_length=750, null=True, db_index=True)

    thumbnail = models.URLField(null=True, blank=True)

    description = RichTextUploadingField(
        null=True,
        help_text=_("Describe something.Dont repeat yourself."),
        config_name="sourcecode",
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(max_length=750, null=True, unique=True, editable=False)
    tags = TaggableManager()
    category = models.ManyToManyField(Category, blank=True)

    published_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    views = models.ManyToManyField(Visitior, blank=True, editable=False)
    total_views = models.IntegerField(default=0, editable=False)

    bookmarks = models.ManyToManyField(User, related_name="bookmarks", default=None, blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=options, default="draft")
    objects = models.Manager()
    modelmanager = CustomManager()

    class Meta:
        ordering = ("published_date",)
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def shortdescription(self):
        return str(self.description)

    def __str__(self):
        return str(self.title)

    @property
    def totalviews(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_read_time(self):
        result = readtime.of_html(self.description)
        return result.text


class Comment(MPTTModel):
    blog = models.ForeignKey(Blog, related_name="blogcomments", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="Commentor", on_delete=models.CASCADE, null=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    content = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ("-commented_on",)

    def __str__(self):
        return f"{self.user}: {self.content}"
