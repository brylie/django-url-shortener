from typing import List

from django.test import TestCase
from django.urls import reverse

from .models import ShortUrl


class ShortUrlTestCase(TestCase):
    def setUp(self):
        ShortUrl.objects.create(redirect_url="https://test.com")

    def test_short_url_has_automatic_slug(self):
        """Make sure short URLs have auto-generated slug"""
        short_url = ShortUrl.objects.get(id=1)

        self.assertIsNotNone(short_url.slug)


class ShortUrlDetailViewTestCase(TestCase):
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

    def test_full_url_in_context(self):
        """Short URL detail view should have full URL string in context"""
        short_url_url = reverse(
            "short-url-detail",
            kwargs={
                "slug": self.short_url.slug,
            }
        )
        response = self.client.get(short_url_url)
        
        context = response.context

        self.assertIn("full_url", context)
        self.assertIsInstance(context["full_url"], str)


class FrontPageTestCase(TestCase):
    def test_front_page_contains_short_url_create_form(self):
        """Front page should render the short URL create form"""
        front_page_route = "/"
        response = self.client.get(front_page_route)

        # Response context should contain ShortUrlCreate form
        # The form class is created automatically by Django
        # so we look for the presence of a form property in the context
        # and check the form class
        expected_form_class = "<class 'django.forms.widgets.ShortUrlForm'>"
        response_form_class = str(type(response.context["form"]))

        self.assertIn("form", response.context)
        self.assertEqual(expected_form_class, response_form_class)