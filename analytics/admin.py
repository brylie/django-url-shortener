from django.contrib import admin

from .models import ShortUrlVisit


@admin.register(ShortUrlVisit)
class ShortUrlVisitAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'occurred',)
