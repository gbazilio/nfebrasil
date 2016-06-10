from django.conf.urls import url

from api.views import get_nfe

urlpatterns = [
    url(r'^nfe/(?P<nfe_key>[0-9]{44})/?$', get_nfe),
]


# GET /api/nfe/<chave>
    # se não tiver cache, responde com Captcha

# GET /api/nfe/<chave>?captcha=<texto>