NFeBrasil API
---

A princípio, essa API tem um único objetivo que é recuperar dados de uma nota fiscal referente a chave de acesso desejada.

As informações são parseadas do site da [Fazenda](http://www.nfe.fazenda.gov.br/portal/consulta.aspx?tipoConsulta=completa).

# Documentação

### Recuperar dados da NF


Recupera dados de uma nota fiscal eletrônica, que esteja acessível através do site da Fazenda, usando um captcha capturado do site.


| URL  				   | Verbo | Query String | Descrição 				            |
| -------------------- | ----- | ------------ | ----------------------------------- |  
| /api/nfe/<chave_nfe> | GET   | -            | Busca um captcha                    |
| /api/nfe/<chave_nfe> | GET   | captcha      | Quando usado, recupera dados da NFE |


**Sucesso** `200 OK` - Buscando captcha
```json
{
	"captcha_src": "data:image/png;base64,iVBORw0K..."
}
```

**Sucesso** `200 OK` - Buscando dados da NFe
```json
{"nfe": {
	    "dados": {
	        "serie": number,
	        "numero": string,
	        "total": number
	    },
	    "emitente": {
	        "cnpj": string,
	        "razao_social": string,
	        "nome_fantasia": string,
	        "endereco": string,
	        "uf": string,
	        "cidade": string,
	    },
	    "items": [{
	    	"indice": number,
            "descricao": string,
            "quantidade": number,
            "unidade": string,
            "valor": number
	    }]
	}
}
```

**Erro** `403 Forbidden`

**Exemplo buscando captcha**
```
curl -H "Authorization: Bearer <access_token>" https://nfebrasil.herokuapp.com/api/nfe/<chave_de_acesso>
```

**Exemplo buscando informações da NFe**
```
curl -H "Authorization: Bearer <access_token>" https://nfebrasil.herokuapp.com/api/nfe/<chave_de_acesso>?captcha=<captcha>
```

# Consumindo a API

### 1. Autenticação
Faço o cadastro da aplicação que irá consumir a API em https://nfebrasil.herokuapp.com/o/applications.

Ex:
Client type: `Confidential`  
Grant type: `Client credentials`

**Importante:** É recomendado o uso de fluxos OAuth não baseados em redirecionamento. Por isso não é necessário se preocupar com o campo `redirect uris`.

### 1.1 Obtenha o Access Token

Client credential:
```
curl --user <client_id>:<client_secret> --data "grant_type=client_credentials" https://nfebrasil.herokuapp.com/o/token/
```

```json
{
	"access_token": "nuT0noX8eJgQQXc0o0mWL6uMoCFk88", 
	"scope": "read", 
	"expires_in": 36000, 
	"token_type": "Bearer"
}
```

### 2. Captcha
O site da fazenda solicita um captcha. Atualmente a forma que a API lida com isso é repassando o captcha para ser resolvido no lado do usuário:

Faça a primeira requisição para https://nfebrasil.herokuapp.com/api/nfe/<chave_nfe> com o Access Token da requisição anterior.

```
curl -H "Authorization: Bearer <access_token>" https://nfebrasil.herokuapp.com/api/nfe/<chave_nfe>
```

Receberá a seguinte resposta:

```json
{
	"captcha_src": "data:image/png;base64,iVBORw0K..."
}
```
O valor de `captcha_src` deve ser entrada para a formação de uma imagem, por exemplo:

```html
<img src="<captcha_src>" />
```

### 3. Informações da NFe

Com o mesmo access token usado para fazer a requisição do captcha, faça um nova requisição passando o captcha decifrado e a chave de acesso:

**Importante**: O tempo máximo entre a requisição do captcha e essa é de 50 segundos.

```
curl -H "Authorization: Bearer nuT0noX8eJgQQXc0o0mWL6uMoCFk88" https://nfebrasil.herokuapp.com/api/nfe/<chave_de_acesso>?captcha=<captcha>
```

# Considerações

- A versão está em desenvolvimento. Sugira o que quiser.
- O slash `/` no final das URLs são importantes.
- A API não é e provavelmente não será estável. O parseamento usa XPath e por isso qualquer alteração na página de exibição da NF no site da Fazenda irá quebrar a resposta.
- O código estará no GitHub em breve.
- Por pelo menos 30 minutos diário o serviço ficará offline pois está hospedado na conta free do Heroku.
