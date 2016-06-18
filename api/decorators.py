from api.webdriver_threading import WebDriverThread


def embed_driver(drivers_dictionary):
    def embed_driver_decorator(func):
        def func_wrapper(*args, **kwargs):
            request = args[0]

            driver = WebDriverThread.get_driver(
                drivers_dictionary, request.auth.token)

            if _current_token_has_webdriver(request):
                driver = _restart_webdriver(driver, request)

            request.driver = driver

            return func(*args, **kwargs)

        def _current_token_has_webdriver(request):
            if 'captcha' not in request.GET:
                return True
            return False

        def _restart_webdriver(driver, request):
            driver.quit()
            driver = WebDriverThread.get_driver(
                drivers_dictionary, request.auth.token)
            return driver

        return func_wrapper
    return embed_driver_decorator
