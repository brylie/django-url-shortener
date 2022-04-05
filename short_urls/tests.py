from django.test import TestCase

from .models import ShortUrl

class ShortUrlTestCase(TestCase):
    def setUp(self):
        ShortUrl.objects.create(redirect_url="https://test.com")

    def test_short_url_has_automatic_slug(self):
        """Make sure short URLs have auto-generated slug"""
        short_url = ShortUrl.objects.get(id=1)

        self.assertIsNotNone(short_url.slug)
