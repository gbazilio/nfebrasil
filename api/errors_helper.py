from rest_framework import status
from rest_framework.response import Response


def error_response(message):
        error_message = {
            'errors': [
                {
                    'status': status.HTTP_502_BAD_GATEWAY,
                    'humanMessage': 'A pagina da receita sofreu '
                                    'modificacoes estruturais no HTML. '
                                    'Entre em contato com o desensolvedor '
                                    'desse modulo.',
                    'developerMessage': message
                }
            ]
        }
        return Response(error_message, status=status.HTTP_502_BAD_GATEWAY)

def error_response_missing_parameters(message):
        error_message = {
            'errors': [
                {
                    'status': status.HTTP_502_BAD_GATEWAY,
                    'humanMessage': 'A requisicao enviada nao esta '
                                    'de acordo com a documentacao. '
                                    'Verifique sua requisicao.',
                    'developerMessage': message
                }
            ]
        }
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
