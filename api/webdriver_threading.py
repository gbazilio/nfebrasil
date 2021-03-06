import os
import threading
import time

from selenium import webdriver


class WebDriverThread(threading.Thread):
    def __init__(self, application_scoped_drivers, unique_id,
                 timeout=50, interval=1):
        super(WebDriverThread, self).__init__()
        self.timeout = timeout
        self.interval = interval
        self.hasQuit = False
        self.driver = None
        self.application_scoped_drivers = application_scoped_drivers
        self.unique_id = unique_id

    def start(self):
        from django.conf import settings

        self.driver = webdriver.PhantomJS(settings.PHANTOMJS_EXECUTABLE)
        super(WebDriverThread, self).start()
        print('Started thread %s - %s' % (self.name, self.unique_id))

    def run(self):
        while self.timeout > 0 and not self.hasQuit:
            print('Timing out... %d - %s,%s' % (
                self.timeout, os.getppid(), os.getpid()))
            time.sleep(self.interval)
            self.timeout -= self.interval

        self.quit()
        print('Finished thread %s - %s' % (self.name, self.unique_id))

    def get(self, url):
        self._increase_timeout()
        self.driver.get(url)

    def _increase_timeout(self):
        self.timeout += 10

    def find_element_by_id(self, element_id):
        self._increase_timeout()
        return self.driver.find_element_by_id(element_id)

    def execute_script(self, script):
        self._increase_timeout()
        self.driver.execute_script(script)

    def click_button(self, button_id):
        self._increase_timeout()
        self.driver.find_element_by_id(button_id).click()

    def page_source(self):
        self._increase_timeout()
        return self.driver.page_source

    def quit(self):
        self._auto_remove_from_application_scope()
        self.driver.quit()
        self.hasQuit = True

    def _auto_remove_from_application_scope(self):
        try:
            del self.application_scoped_drivers[self.unique_id]
        except KeyError:
            return

    @staticmethod
    def get_driver(application_drivers_dictionary, session_key):
        try:
            driver = application_drivers_dictionary[session_key]
            if not driver.isAlive():
                driver = WebDriverThread(
                    application_drivers_dictionary, session_key)
                driver.start()
                application_drivers_dictionary[session_key] = driver
        except KeyError:
            driver = WebDriverThread(
                application_drivers_dictionary, session_key)
            driver.start()
            application_drivers_dictionary[session_key] = driver

        return driver
