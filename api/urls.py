from django.conf.urls import url, include
from django.contrib import admin

from api.views import NFeRoot

urlpatterns = [
    url(r'^$', NFeRoot.as_view()),
]
