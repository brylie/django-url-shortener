from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView

from .models import ShortUrl


class ShortUrlCreateView(CreateView):
    model = ShortUrl
    fields = ['redirect_url']

    def get_success_url(self):
        print("short url success url")
        return reverse('short-url-detail', kwargs={'pk' : self.object.pk})


class ShortUrlDeleteView(DeleteView):
    model = ShortUrl
    success_url = reverse_lazy('short-url-create')


class ShortUrlDetailView(DetailView):
    model = ShortUrl


class ShortUrlRedirectView(View):
    def get(self, request, pk):
        short_url = ShortUrl.objects.get(pk=pk)

        return redirect(short_url.redirect_url)
