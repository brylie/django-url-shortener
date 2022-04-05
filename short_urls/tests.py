from typing import List
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import ShortUrl
from .views import ShortUrlDetailView

class ShortUrlTestCase(TestCase):
    def setUp(self):
        ShortUrl.objects.create(redirect_url="https://test.com")

    def test_short_url_has_automatic_slug(self):
        """Make sure short URLs have auto-generated slug"""
        short_url = ShortUrl.objects.get(id=1)

        self.assertIsNotNone(short_url.slug)


class ShortUrlDetailViewTest(TestCase):
    def setUp(self):
        # Create a testing short URL
        self.short_url = ShortUrl.objects.create(
            redirect_url="https://google.com",
        )

    def test_analytics_list_in_context(self):
        """Short URL detail view should have analytics list in context"""
        short_url_url = reverse(
            "short-url-detail",
            kwargs={
                "slug": self.short_url.slug,
            }
        )
        response = self.client.get(short_url_url)
        
        context = response.context

        self.assertIn("analytics", context)
        self.assertIsInstance(context["analytics"], List)
