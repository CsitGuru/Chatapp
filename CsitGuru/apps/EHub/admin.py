from django.contrib import admin

from.models import (
    Profile,
    Contact,
    EmailSubscription, Media
)
# Register your models here.
admin.site.register((Profile,Contact,EmailSubscription,Media))
