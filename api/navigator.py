from api.parser import NFeParser


class NFeNavigator:

    URL = 'http://www.nfe.fazenda.gov.br/portal/consulta.aspx?tipoConsulta=completa&tipoConteudo=XbSeqxE8pl8='

    _CAPTCHA_SRC = 'ctl00_ContentPlaceHolder1_imgCaptcha'
    _BTN_SEARCH = 'ctl00_ContentPlaceHolder1_btnConsultar'
    _NFE_CAPTCHA = 'ctl00_ContentPlaceHolder1_txtCaptcha'
    _NFE_KEY = 'ctl00_ContentPlaceHolder1_txtChaveAcessoCompleta'

    def __init__(self, driver):
        self.driver = driver

    def get_captcha(self):
        try:
            self.driver.get(self.URL)
            captcha = self.driver.find_element_by_id(
                self._CAPTCHA_SRC).get_attribute('src')
        except:
            raise ValueError('No captcha image found on target URL %s '
                              'when trying to search for element %s.'
                              % (self.URL, self._CAPTCHA_SRC))

        return captcha

    def get_nfe(self, nfe_captcha, nfe_key):

        self.driver.execute_script(
                'document.getElementById("%s").value = "%s";' % (
                    self._NFE_CAPTCHA,
                    nfe_captcha))
        self.driver.execute_script(
                'document.getElementById("%s").value = "%s";' % (
                    self._NFE_KEY,
                    nfe_key))

        try:
            self.driver.find_element_by_id(self._BTN_SEARCH).click()
        except:
            return ValueError('No Continue button found on target URL %s '
                              'when trying to search for element %s.'
                              % (self.URL, self._BTN_SEARCH))

        page_source = self.driver.page_source()
        self.driver.quit()

        parser = NFeParser(page_source)
        return parser.parse_to_json()
