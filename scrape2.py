# import libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import warnings

DEMO_URL = 'https://www.worldometers.info/coronavirus/'
WP_DEMO_URL = 'https://www.worldometers.info/world-population/'


def scraper(url=DEMO_URL, DEBUG=False):
    # specify the url
    if DEBUG is True:
        print(url)

    # Ignore warnings about PhantomJS depreciation
    warnings.filterwarnings('ignore')
    # run firefox webdriver from executable path of your choice
    # driver = webdriver.Firefox()
    # Run PhantomJS headless browser
    driver = webdriver.PhantomJS()

    try:
        # get web page
        driver.get(url)
        # execute script to scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep for 30s
        time.sleep(10)

        # import the page into BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # quit the driver
        driver.quit()
        # find all <text> elements
        values = soup.find_all('div', {"id": "maincounter-wrap"})
        counts = []
        for span in values:
            counts.extend(span.findAll('span'))
        titles = []
        for h1 in values:
            titles.extend(h1.findAll('h1'))
        if DEBUG is True:
            print(titles, counts)
            print(values)
        # build the relevant data set
        stats = {titles[0].get_text().replace(':', ''): counts[0].get_text().rstrip(),
                 titles[1].get_text().replace(':', ''): counts[1].get_text(),
                 titles[2].get_text().replace(':', ''): counts[2].get_text()}

        return stats

    except IndexError:
        return False


def world_pop(url=WP_DEMO_URL, DEBUG=False):
    # specify the url
    if DEBUG is True:
        print(url)

    # Ignore warnings about PhantomJS depreciation
    warnings.filterwarnings('ignore')
    # run firefox webdriver from executable path of your choice
    # driver = webdriver.Firefox()
    # Run PhantomJS headless browser
    driver = webdriver.PhantomJS()

    try:
        # get web page
        driver.get(url)
        # execute script to scroll down the page
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep for 30s
        time.sleep(10)

        # import the page into BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # quit the driver
        driver.quit()
        # find all <text> elements
        values = soup.find_all('div', {"id": "maincounter-wrap"})
        counts = []
        for span in values:
            counts.extend(span.findAll('span'))
        titles = []
        for h1 in values:
            titles.extend(h1.findAll('h1'))
        if DEBUG is True:
            print(titles, counts)
            print(values)
        # build the relevant data set
        stats = {titles[0].get_text().lstrip(): counts[0].get_text()}

        return stats

    except IndexError:
        return False


if __name__ == "__main__":
    # s = scraper()
    # print(s)
    wc = world_pop()
    print(wc)

