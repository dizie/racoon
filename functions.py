from selenium import webdriver
from bs4 import BeautifulSoup
import time


class WebDriver:
    def __init__(self, url, timeout):
        self.driver = webdriver.PhantomJS()
        self.url = url
        self.timeout = timeout

    def get_url(self):
        self.driver.get(self.url)
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(self.timeout)
        payload = self.driver.page_source
        self.driver.quit()

        soup = BeautifulSoup(payload, 'html.parser').find_all('div', {"id": "maincounter-wrap"})

        return soup
