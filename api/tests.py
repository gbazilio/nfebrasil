import os
from collections import namedtuple
from unittest import mock

from django.test import TestCase
from django.test.client import Client
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from oauth2_provider.models import AccessToken
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

import api.views as views
from api.parser import NFeParser
from api.webdriver_threading import WebDriverThread


class NFeRootViewsTestCase(TestCase):

    def tearDown(self):
        views.application_webdrivers.clear()

    @mock.patch('api.webdriver_threading.WebDriverThread.quit')
    @mock.patch('api.webdriver_threading.WebDriverThread.start')
    @mock.patch('api.navigator.NFeNavigator.get_captcha')
    def test_should_get_captcha_src(
            self, mock_captcha, mock_thread, mock_quit):

        expected_json_schema = {
            'type': 'object',
            'properties': {
                'captcha_src': {
                    'type': 'string',
                    'pattern': '^data:image/png;base64,.+'
                }
            },
            'required': ['captcha_src'],
            'additionalProperties': False
        }
        mock_captcha.return_value = 'data:image/png;base64,asdkjdlasdsd='
        # There is no need to really start the threaded web driver
        mock_thread.return_value = None
        mock_quit.return_value = None

        nfe_key = '1' * 44
        request = self._make_authenticated_request_object(
            '18273319832', nfe_key)
        response = views._get_nfe(request, nfe_key)

        try:
            validate(response.data, expected_json_schema)
        except ValidationError as e:
            self.fail(e.message)

    def _mock_request_auth_token(self, request, token):
        auth_mock = namedtuple('AuthMock', 'token')
        auth = auth_mock(token=token)
        setattr(request, 'auth', auth)

    def _make_authenticated_request_object(self, token, nfe_key, captcha=None):

        url = '/nfe/%s' % nfe_key
        url = url + '?captcha=%s' % captcha if captcha else url

        captcha_get_request = APIRequestFactory().get(url)
        captcha_get_request = APIView().initialize_request(captcha_get_request)
        self._mock_request_auth_token(captcha_get_request, token)
        return captcha_get_request

    @mock.patch('api.webdriver_threading.WebDriverThread.quit')
    @mock.patch('api.webdriver_threading.WebDriverThread.start')
    @mock.patch('api.navigator.NFeNavigator.get_captcha')
    @mock.patch('api.navigator.NFeNavigator.get_nfe')
    def test_should_get_nfe_with_using_same_webdriver(
            self, mock_nfe, mock_captcha, mock_thread, mock_quit):

        expected_number_of_drivers_in_scope = 1
        expected_token_key_in_scope = 'asdkj312313'

        mock_captcha.return_value = 'data:image/png;base64,asdkjdlasdsd='
        mock_nfe.return_value = {}

        # There is no need to really start the threaded web driver
        mock_thread.return_value = None
        mock_quit.return_value = None

        # NFe key
        nfe_key = '1' * 44

        captcha_get_request = self._make_authenticated_request_object(
            expected_token_key_in_scope, nfe_key)
        captcha_get_response = views._get_nfe(captcha_get_request, nfe_key)

        nfe_get_request = self._make_authenticated_request_object(
            expected_token_key_in_scope, nfe_key,
            captcha_get_response.data['captcha_src'])
        views._get_nfe(nfe_get_request, nfe_key)

        self.assertTrue(expected_token_key_in_scope in
                        views.application_webdrivers.keys())
        self.assertEquals(len(views.application_webdrivers.keys()),
                          expected_number_of_drivers_in_scope)


class NFeParserTestCase(TestCase):
    def setUp(self):
        asset_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_assets/nfe_multiple_items.html'
        )

        self.asset_nfe_html = open(asset_path, 'rt',
                                   encoding='iso-8859-1').read()

    def test_should_parse_nfe_html(self):
        expected = {
            'nfe': {
                'dados': {
                    'serie': 3,
                    'numero': '10611731',
                    'total': 47.90
                },
                'emitente': {
                    'cnpj': '00.776.574/0007-41',
                    'razao_social': 'B2W Companhia Digital',
                    'nome_fantasia': '',
                    'endereco': 'Estrada dos Alpes, 555, S/N',
                    'uf': 'SP',
                    'cidade': '3522505 - ITAPEVI'
                },
                'items': [
                    {
                        'indice': 1,
                        'descricao': 'Livro - 7 Habitos das Pessoas Altamente Eficazes',
                        'quantidade': 1.0,
                        'unidade': 'PC',
                        'valor': 26.90
                    },
                    {
                        'indice': 2,
                        'descricao': 'Livro - Vendendo o Invisivel',
                        'quantidade': 1.0,
                        'unidade': 'PC',
                        'valor': 21.0
                    }
                ]
            }
        }

        sut = NFeParser(self.asset_nfe_html)
        result = sut.parse_to_json()

        self.assertDictEqual(expected, result)


class NFeRoutesTestCase(TestCase):
    fixtures = ['oauth2_valid_token.json']

    def setUp(self):
        self.access_token = AccessToken.objects.last()

    def tearDown(self):
        thread = WebDriverThread.get_driver(
            views.application_webdrivers, self.access_token.token)
        thread.quit()

    @mock.patch('api.navigator.NFeNavigator.get_captcha')
    def test_should_get_a_valid_captcha(self, mock_captcha):
        nfe_key = '11223344556677889900112233445566778899112233'
        expected_captcha_src = 'data:image/png;base64,asdkjdlasdsd='

        mock_captcha.return_value = expected_captcha_src

        sut = Client(HTTP_AUTHORIZATION='Bearer ' + self.access_token.token)
        response = sut.get('/api/nfe/%s' % nfe_key)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_captcha_src, response.data['captcha_src'])

    @mock.patch('selenium.webdriver.PhantomJS.find_element_by_id')
    def test_should_get_502_when_captcha_isnt_available(
            self, mock_find_element_by_id):
        nfe_key = '11223344556677889900112233445566778899112233'
        expected_error_message = {
            'errors': [
                {
                    'status': status.HTTP_502_BAD_GATEWAY,
                    'humanMessage': 'A pagina da receita sofreu '
                                    'modificacoes estruturais no HTML. '
                                    'Entre em contato com o desensolvedor '
                                    'desse modulo.',
                    'developerMessage': 'No captcha image found on target URL '
                                        'http://www.nfe.fazenda.gov.br/portal/'
                                        'consulta.aspx?tipoConsulta=completa&'
                                        'tipoConteudo=XbSeqxE8pl8= when trying'
                                        ' to search for element ctl00_'
                                        'ContentPlaceHolder1_imgCaptcha.'
                }
            ]
        }

        mock_find_element_by_id.side_effect = Exception()

        sut = Client(HTTP_AUTHORIZATION='Bearer ' + self.access_token.token)
        response = sut.get('/api/nfe/%s' % nfe_key)

        self.assertEquals(status.HTTP_502_BAD_GATEWAY, response.status_code)
        self.assertDictEqual(expected_error_message, response.data)

    @mock.patch('selenium.webdriver.PhantomJS.execute_script')
    def test_should_get_502_when_continue_button_isnt_available(
            self, mock_execute_script):
        nfe_key = '11223344556677889900112233445566778899112233'
        expected_error_message = {
            'errors': [
                {
                    'status': status.HTTP_502_BAD_GATEWAY,
                    'humanMessage': 'A pagina da receita sofreu '
                                    'modificacoes estruturais no HTML. '
                                    'Entre em contato com o desensolvedor '
                                    'desse modulo.',
                    'developerMessage': 'No Continue button found on target '
                                        'URL http://www.nfe.fazenda.gov.br/'
                                        'portal/consulta.aspx?tipoConsulta'
                                        '=completa&tipoConteudo=XbSeqxE8pl8= '
                                        'when trying to search for element '
                                        'ctl00_ContentPlaceHolder1_'
                                        'btnConsultar.'
                }
            ]
        }

        mock_execute_script.side_effect = Exception()

        sut = Client(HTTP_AUTHORIZATION='Bearer ' + self.access_token.token)
        response = sut.get('/api/nfe/%s' % nfe_key, data={'captcha': '123456'})

        self.assertEquals(status.HTTP_502_BAD_GATEWAY, response.status_code)
        self.assertDictEqual(expected_error_message, response.data)
