from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.decorators import embed_driver
from api.errors_helper import error_response
from api.navigator import NFeNavigator

application_webdrivers = {}


@api_view(['GET'])
@protected_resource(scopes=['read'])
def get_nfe(request, nfe_key):
    return _get_nfe(request, nfe_key)


@embed_driver(application_webdrivers)
def _get_nfe(request, nfe_key):

    navigator = NFeNavigator(request.driver)

    try:
        captcha = request.GET['captcha']
    except KeyError:
        try:
            _captcha_src = navigator.get_captcha()
        except ValueError as e:
            return error_response(e.args[0])
        return Response({'captcha_src': _captcha_src})

    try:
        nfe_json = navigator.get_nfe(captcha, nfe_key)
    except ValueError as e:
        return error_response(e.message)

    return Response(nfe_json)
