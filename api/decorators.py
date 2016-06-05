from api.webdriver_threading import WebdriverThread


def embed_driver(drivers_dictionary):
    def embed_driver_decorator(func):
        def func_wrapper(*args, **kwargs):
            request = args[1]

            session_key = _get_webdriver_unique_key(request)

            driver = WebdriverThread.get_driver(
                    drivers_dictionary, session_key)

            request.driver = driver
            return func(*args, **kwargs)

        def _get_webdriver_unique_key(request):
            return request.auth.token

        return func_wrapper
    return embed_driver_decorator
