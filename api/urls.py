from django.conf.urls import url, include
from django.contrib import admin

from api.views import NFeRoot

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^/?$', NFeRoot.as_view()),
]
