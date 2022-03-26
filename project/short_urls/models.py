import hashlib

from django.db import models, transaction
from django.urls import reverse

from datetime import datetime


class ShortUrl(models.Model):
    redirect_url = models.URLField()
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        # Generate short URL slug from ID in a single transaction
        # Using hashlib
        # Pro, non-sequential, so hard to guess
        # Pro: uses only standardlib
        # Pro: can specify hash length
        # Con: some liklihood of collision? Can be mitigated with increased hash length
        # or explicit uniqueness check (e.g. using "while slug not unique:" and db query)
        # https://stackoverflow.com/a/62699124/1191545

        # Decide on hash length
        # Note: will generate a has twice the length of this value
        # e.g. 5 will generate a 10 character hash
        hash_length = 5

        # Get current datetime string in ISO format
        datetime_now_iso = datetime.now().isoformat()

        # Create unique hash string from datetime now and redirect URL
        hash_string = f"{ datetime_now_iso }-{ self.redirect_url }".encode()
        
        # Generate hash of desired length
        hashlib_slug = hashlib.shake_256(hash_string).hexdigest(hash_length)
        self.slug = hashlib_slug

        # Save item with new slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('short-url-detail', kwargs={'pk': self.pk})
