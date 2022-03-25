import hashlib

from django.db import models, transaction
from django.urls import reverse

import base_repr


class ShortUrl(models.Model):
    redirect_url = models.URLField()
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        # Generate short URL slug from ID in a single transaction
        with transaction.atomic():
            # Save initial instance to generate unique ID
            super().save(*args, **kwargs)

            # Set slug based on item ID
            # We use base-36 since it contains the full alphanumeric character set
            # Pro: guaranteed to be unique, 
            # Con: sequential, so easy to guess
            # Con: uses third-party library, althouth reasonably well maintained at this time
            # https://github.com/h5kure/base_repr
            base_36_slug = base_repr.int_to_repr(self.id, base=36)
            self.slug = base_36_slug

            # Alternative approach with hashlib
            # Pro, non-sequential, so hard to guess
            # Pro: uses only standardlib
            # Pro: can specify hash length
            # Con: some liklihood of collision? Can be mitigated with increased hash length
            # https://stackoverflow.com/a/62699124/1191545

            # Decide on hash length
            # Note: will generate a has twice the length of this value
            # e.g. 5 will generate a 10 character hash
            hash_length = 5

            # Encode string with unique ID and redirect URL for unique hash
            hash_string = f"{ self.id }-{ self.redirect_url }".encode()
            # Generate hash of desired length
            hashlib_slug = hashlib.shake_256(hash_string).hexdigest(hash_length)
            self.slug = hashlib_slug

            # Save item with new slug
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('short-url-detail', kwargs={'pk': self.pk})
