import os
from unittest import mock

from boto.beanstalk.exception import ValidationError
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import RequestFactory
from jsonschema.validators import validate

from api.parser import NFeParser
from api.views import NFeRoot


class NFeRootViewsTestCase(TestCase):

    @mock.patch('api.webdriver_threading.WebdriverThread.start')
    @mock.patch('api.navigator.NFeNavigator.get_captcha')
    def test_should_get_captcha_src_when_get_request_with_token(
            self, mock_captcha, mock_thread):

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

        request = RequestFactory().get(
            '/',
           HTTP_AUTHORIZATION='Bearer dkjsdalsj034='
        )
        SessionMiddleware().process_request(request)

        response = NFeRoot().get(request)

        try:
            validate(response.data, expected_json_schema)
        except ValidationError as e:
            self.fail(e.message)


class NFeRJParserTestCase(TestCase):
    def setUp(self):
        asset_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_assets/nfe_multiple_items.html'
        )

        self.asset_nfe_html = open(asset_path, 'rt', encoding='iso-8859-1').read()

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
