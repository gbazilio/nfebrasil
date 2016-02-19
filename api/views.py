from django.http.response import JsonResponse
from oauth2_provider.ext.rest_framework.permissions import \
    TokenHasReadWriteScope

from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.views import APIView

from nferoot.api.navigator import NFeNavigator
from nferoot.api.errors_helper import _error_response


class NFeRoot(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        navigator = NFeNavigator(request.driver)

        try:
            _captcha_src = navigator.get_captcha()
        except ValueError as e:
            return _error_response(e.message)

        return Response({'captcha': _captcha_src})

    def post(self, request):
        driver = request.driver

        nfe_key = request.data['nfeAccessKey']
        nfe_captcha = request.data['nfeCaptcha']

        navigator = NFeNavigator(driver)

        try:
            result = navigator.get_nfe(nfe_captcha, nfe_key)
        except ValueError as e:
            return _error_response(e.message)

        driver.quit()
        return JsonResponse(result)

