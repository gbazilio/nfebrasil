from api.webdriver_threading import WebdriverThread


def embed_driver(drivers_dictionary):
    def embed_driver_decorator(func):
        def func_wrapper(*args, **kwargs):
            request = args[1]
            authorization_token = request.META['HTTP_AUTHORIZATION']
            session_key = authorization_token.replace('Bearer ', '')

            driver = WebdriverThread.get_driver(
                    drivers_dictionary, session_key)

            request.driver = driver
            return func(*args, **kwargs)
        return func_wrapper
    return embed_driver_decorator
