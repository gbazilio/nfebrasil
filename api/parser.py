from lxml import html

from nferoot.api.parseutils import assert_valid_html_string, sanitize, \
    remove_duplicate_entries


class NFeParser:
    def __init__(self, html_string):
        assert_valid_html_string(html_string)
        self.html_tree = html.fromstring(html_string)

    def parse_to_json(self):
        serie = self._get_serie()
        numero = self._get_numero()
        total = self._get_total()
        cnpj = self._get_cnpj()
        razao_social = self._get_razao_social()
        nome_fantasia = self._get_nome_fantasia()
        endereco = self._get_endereco()
        uf = self._get_uf()
        cidade = self._get_cidade()
        items = self._get_items()

        result = {
            'nfe': {
                'dados': {
                    'serie': serie,
                    'numero': numero,
                    'total': total
                },
                'emitente': {
                    'cnpj': cnpj,
                    'razao_social': razao_social,
                    'nome_fantasia': nome_fantasia,
                    'endereco': endereco,
                    'uf': uf,
                    'cidade': cidade,
                },
                'items': items
            }
        }
        return result

    def _get_serie(self):
        serie = self._get_value_by_xpath(
            '//*[@id="NFe"]/fieldset[1]/table/tbody/tr/td[2]/span/text()'
        )
        return int(serie) if serie else 0

    def _get_numero(self):
        return self._get_value_by_xpath(
            '//*[@id="NFe"]/fieldset[1]/table/tbody/tr/td[3]/span/text()'
        )

    def _get_total(self):
        total = self._get_value_by_xpath(
            '//*[@id="NFe"]/fieldset[1]/table/tbody/tr/td[6]/span/text()'
        ).replace(',', '.')
        return float(total) if total else 0

    def _get_cnpj(self):
        return self._get_value_by_xpath(
            '//*[@id="NFe"]/fieldset[2]/table/tbody/tr/td[1]/span/text()'
        )

    def _get_value_by_xpath(self, xpath, dom_element=None):
        if dom_element is None:
            dom_element = self.html_tree

        try:
            return sanitize(dom_element.xpath(xpath)[0])
        except:
            return ''

    def _get_razao_social(self):
        return self._get_value_by_xpath(
            '//*[@id="Emitente"]/fieldset/table/tbody/tr[1]/td[1]/span/text()'
        )

    def _get_nome_fantasia(self):
        return self._get_value_by_xpath(
            '//*[@id="Emitente"]/fieldset/table/tbody/tr[1]/td[2]/span/text()'
        )

    def _get_endereco(self):
        return self._get_value_by_xpath(
            '//*[@id="Emitente"]/fieldset/table/tbody/tr[2]/td[2]/span/text()'
        )

    def _get_uf(self):
        return self._get_value_by_xpath(
            '//*[@id="Emitente"]/fieldset/table/tbody/tr[5]/td[1]/span/text()'
        )

    def _get_cidade(self):
        return self._get_value_by_xpath(
            '//*[@id="Emitente"]/fieldset/table/tbody/tr[4]/td[1]/span/text()'
        )

    def _get_items(self):
        items = []

        try:
            tables = self.html_tree.xpath(
                '//*[@id="Prod"]/fieldset/div/table[@class="toggle box"]'
            )
        except:
            return ''

        for table in tables:
            try:
                index = self._get_value_by_xpath(
                        'tbody/tr/td[1]/span/text()', table)
                index = 0 if not index else int(index)

                description = self._get_value_by_xpath(
                        'tbody/tr/td[2]/span/text()', table)

                quantity = self._get_value_by_xpath(
                        'tbody/tr/td[3]/span/text()', table).replace(',', '.')
                quantity = 0.0 if not quantity else float(quantity)

                unit = self._get_value_by_xpath(
                        'tbody/tr/td[4]/span/text()', table)

                price = self._get_value_by_xpath(
                        'tbody/tr/td[5]/span/text()', table).replace(',', '.')
                price = 0.0 if not price else float(price)

                items.append(dict(
                    indice=index,
                    descricao=description,
                    quantidade=quantity,
                    unidade=unit,
                    valor=price
                ))
            except:
                items.append(None)

        items = remove_duplicate_entries(items)
        items = sorted(items, key=lambda item: item['indice'])

        return items
