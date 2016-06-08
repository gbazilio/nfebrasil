from django.conf.urls import url, include
from django.contrib import admin

from api.views import NFeRoot, get_captcha

urlpatterns = [
    url(r'^captcha/?$', get_captcha),
]
