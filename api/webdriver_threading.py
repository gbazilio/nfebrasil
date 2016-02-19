import threading
import time

from selenium import webdriver


class WebdriverThread(threading.Thread):
    def __init__(self, timeout=50, interval=1):
        super(WebdriverThread, self).__init__()
        self.timeout = timeout
        self.interval = interval
        self.hasQuit = False
        self.driver = None

    def start(self):
        self.driver = webdriver.PhantomJS()
        super(WebdriverThread, self).start()
        print('Started thread %s' % self.name)

    def run(self):
        while self.timeout > 0 and not self.hasQuit:
            print('Timing out... %d' % self.timeout)
            time.sleep(self.interval)
            self.timeout -= self.interval

        self.driver.quit()
        print('Finished thread %s' % self.name)

    def get(self, url):
        self.driver.get(url)

    def find_element_by_id(self, element_id):
        return self.driver.find_element_by_id(element_id)

    def execute_script(self, script):
        self.driver.execute_script(script)

    def click_button(self, button_id):
        self.driver.find_element_by_id(button_id).click()

    def page_source(self):
        return self.driver.page_source

    def quit(self):
        self.driver.quit()
        self.hasQuit = True

    @staticmethod
    def get_driver(application_drivers_dictionary, session_key):
        try:
            driver = application_drivers_dictionary[session_key]
            if not driver.isAlive():
                driver = WebdriverThread()
                driver.start()
                application_drivers_dictionary[session_key] = driver
        except KeyError:
            driver = WebdriverThread()
            driver.start()
            application_drivers_dictionary[session_key] = driver

        return driver
