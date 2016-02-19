from nferoot.api.webdriver_threading import WebdriverThread


application_webdrivers = {}


class WebdriverThreadingMiddleware:

    def process_request(self, request):

        try:
            nfe_session_key = request.COOKIES['NFE_SESSION']
            driver = WebdriverThread.get_driver(
                    application_webdrivers, nfe_session_key)
            request.driver = driver
        finally:
            return None
