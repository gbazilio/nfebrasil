from django.conf.urls import url

from api.views import get_captcha

urlpatterns = [
    url(r'^captcha/?$', get_captcha),
]



# GET /api/captcha
# GET /api/captcha/<texto>/nfe/<chave>

# GET /api/nfe/<chave>
    # se não tiver cache, responde com Captcha

# GET /api/nfe/<chave>?captcha=<texto>