NFeBrasil API
---

A princípio, essa API tem um único objetivo que é recuperar dados de uma nota fiscal referente a chave de acesso desejada.

## Resposta
```json
{
	nfe: {
	    dados: {
	        serie: number,
	        numer: string,
	        total: number
	    },
	    emitente: {
	        cnpj: string,
	        razao_social: string,
	        nome_fantasia: string,
	        endereco: string,
	        uf: string,
	        cidade: string,
	    },
	    items: [{
	    	indice: number,
            descricao: string,
            quantidade: number,
            unidade: string,
            valor: number
	    }]
	}
}
```

# Consumindo a API

## Credenciais
Faço o cadastro da aplicação que irá consumir a API em (https://nfebrasil.herokuapp.com/o/applications).

Ex:
Client type: `Confidential`  
Grant type: `Client credentials`

**Importante:** É recomendado o uso de fluxos OAuth não baseados em redirecionamento. Por isso não é necessário se preocupar com o campo `redirect uris`.

## Access Token

Client credential:
```
curl --user <client_id>:<client_secret> --data "grant_type=client_credentials" https://nfebrasil.herokuapp.com/o/token/
```

## Captcha
O site da fazenda solicita um captcha. Atualmente a forma que a API lida com isso é repassando o captcha para ser resolvido no lado do usuário:

Faça a primeira requisição para (https://nfebrasil.herokuapp.com/api/). A resposta é:
```json
{
	captcha_src: string
}
```
O valor de `captcha_src` deve ser entrada para a formação de uma imagem:

```html
<img src="<captcha_src>" />
```
