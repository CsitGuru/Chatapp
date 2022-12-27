import debug_toolbar
from django.contrib import admin
from django.urls import include, path, re_path

"""
url() uses a regular expression to pattern match the
URL in your browser to a module in your Django project.
"""
urlpatterns = [  # contains list of url() instances.
    re_path(r"^admin/", admin.site.urls),
    # re_path(r"^", include("CsitGuru.apps.EHub.urls", namespace="Ehub")),
    # re_path(r"^", include("CsitGuru.apps.Blog.urls", namespace="Blog")),
    path("courses/", include("CsitGuru.apps.MCourse.urls", namespace="Courses")),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns



"""
Note: We are just providin the info of where is the custom page to be displayed
for the handler404 and handler500.
It can be created in any  one app.
"""

