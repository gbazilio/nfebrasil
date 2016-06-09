from api.webdriver_threading import WebDriverThread


def embed_driver(drivers_dictionary):
    def embed_driver_decorator(func):
        def func_wrapper(*args, **kwargs):
            request = args[0]

            driver = WebDriverThread.get_driver(
                    drivers_dictionary, request.auth.token)

            request.driver = driver
            return func(*args, **kwargs)

        return func_wrapper
    return embed_driver_decorator
