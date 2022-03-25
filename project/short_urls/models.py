from django.db import models
from django.urls import reverse

class ShortUrl(models.Model):
    redirect_url = models.URLField()

    def get_absolute_url(self):
        return reverse('short-url-detail', kwargs={'pk': self.pk})
