from django.conf.urls import url
from . import views
from .views import UrlViewSet

urlpatterns = [
    url(r'[a-zA-Z0-9]{9}', UrlViewSet.getorgurl),
    url('newurl', UrlViewSet.shortenurl),
]

