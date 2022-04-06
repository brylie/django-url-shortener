from datetime import datetime, timedelta
import hashlib

from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from datetime import datetime


class ShortUrl(models.Model):
    redirect_url = models.URLField()
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        # Generate short URL slug from current datetime and redirect URL
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
        return reverse("short-url-detail", kwargs={"pk": self.pk})

    def get_recent_daily_visit_counts(self, num_days=7):
        """
        Return daily visit counts for past number of days.
        """
        today = timezone.now()
        time_delta = timedelta(days=num_days)
        previous_datetime = today - time_delta

        analytics_data = self.visits.filter(
            occurred__gte=previous_datetime
        ).extra({"date_occurred": "date(occurred)"}).values("date_occurred").annotate(visit_count=Count("id"))

        return analytics_data

    def __str__(self):
        return self.redirect_url
