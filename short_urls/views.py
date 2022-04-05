from typing import Any, Dict

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView

from analytics.models import ShortUrlVisit
from .models import ShortUrl


class ShortUrlCreateView(CreateView):
    model = ShortUrl
    fields = ["redirect_url"]

    def get_success_url(self) -> str:
        return reverse("short-url-detail", kwargs={"slug": self.object.slug})


class ShortUrlDeleteView(DeleteView):
    model = ShortUrl
    success_url = reverse_lazy("short-url-create")


class ShortUrlDetailView(DetailView):
    model = ShortUrl

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        short_url = context["shorturl"]

        # Aggregate visit counts by day
        # https://stackoverflow.com/a/41930880/1191545
        analytics = (
            short_url.visits.all()
            .annotate(date=TruncDay("occurred"))
            .values("date")
            .annotate(visits_count=Count("id"))
            .order_by("date")
        )
        # Add analytics to context data as list
        # so it can be parsed to JSON in the template
        context["analytics"] = list(analytics)

        return context


class ShortUrlRedirectView(View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        # Get desired short URL object
        short_url = ShortUrl.objects.get(slug=slug)

        # Get the current, timezone-aware datetime
        now = timezone.now()

        # Record a visit for this short URL
        # using current datetime
        ShortUrlVisit.objects.create(
            short_url=short_url,
            occurred=now,
        )

        return redirect(short_url.redirect_url)
