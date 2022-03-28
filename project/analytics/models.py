from django.db import models

from short_urls.models import ShortUrl


class ShortUrlVisit(models.Model):
    short_url = models.ForeignKey(to=ShortUrl, on_delete=models.CASCADE)
    occurred = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["occurred"])
        ]
