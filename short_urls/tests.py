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
    def setUp(self):
        self.front_page_route = "/"
        self.response = self.client.get(self.front_page_route)

    def test_front_page_returns_success(self):
        """Front page should return success response"""
        self.assertEqual(self.response.status_code, 200)
    
    def test_front_page_contains_short_url_create_form(self):
        """Front page should render the short URL create form"""
        response_form = self.response.context["form"]

        # Response context should contain ShortUrlCreate form
        # The form class is created automatically by Django
        # so we look for the presence of a form property in the context
        # and check the form class
        expected_form_class = "<class 'django.forms.widgets.ShortUrlForm'>"
        response_form_class = str(type(response_form))

        self.assertIn("form", self.response.context)
        self.assertEqual(expected_form_class, response_form_class)

    def test_front_page_success_redirects_to_short_url(self):
        """
        Successfully submitting the short URL form on the front page
        should redirect to the ShortUrl detail view
        """
        redirect_status_code = 302
        redirect_url = "https://test.com"

        # Prepare form data
        post_data = {
            "redirect_url": redirect_url,
        }

        # Submit form
        response = self.client.post(
            self.front_page_route,
            post_data,
        )

        # Get the newly created short URL and detail page URL
        short_url = ShortUrl.objects.get(redirect_url=redirect_url)
        short_url_detail_url = reverse("short-url-detail", kwargs={"slug": short_url.slug})

        # Ensure the response redirects to the new short URL detail page
        self.assertEqual(response.status_code, redirect_status_code)
        self.assertRedirects(response, short_url_detail_url)
