from django.urls import path

from .views import ShortUrlCreateView, ShortUrlDeleteView, ShortUrlDetailView, ShortUrlRedirectView

urlpatterns = [
    path('', ShortUrlCreateView.as_view(), name='short-url-create'),
    path('<slug:slug>/delete', ShortUrlDeleteView.as_view(), name='short-url-delete'),
    path('<slug:slug>/detail', ShortUrlDetailView.as_view(), name='short-url-detail'),
    path('<slug>', ShortUrlRedirectView.as_view(), name='short-url-redirect'),
]