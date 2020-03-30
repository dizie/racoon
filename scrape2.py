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


def country_url(country, metric):
    country = country.replace(" ", "-").lower()
    if metric == "population":
        return "https://www.worldometers.info/world-population/{}-population/".format(country)
    else:
        if country == "new-zealand":
            return "not-supported"
        else:
            return "https://www.worldometers.info/coronavirus/country/{}".format(country)


def country_pop(country, DEBUG=True):
    url = country_url(country, "population")
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
        time.sleep(5)

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
            print(titles)
            print(counts)
            #print(values)
        # build the relevant data set
        stats = {titles[0].get_text().lstrip(): counts[1].get_text()}

        return stats

    except IndexError:
        return False


def country_stat(country, DEBUG=True):
    url = country_url(country, "infected")
    if url == "not-supported":
        stats = {"place-holder": "552"}
        return stats
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
        time.sleep(5)

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
            print(titles)
            print(counts)
        # build the relevant data set
        stats = {titles[0].get_text().replace(':', ''): counts[0].get_text().rstrip(),
                 titles[1].get_text().replace(':', ''): counts[1].get_text(),
                 titles[2].get_text().replace(':', ''): counts[2].get_text()}

        return stats

    except IndexError:
        return False


def country_data(country, DEBUG=False):
    population = country_pop(country, DEBUG)
    stats = country_stat(country, DEBUG)
    p_keys = list(population.keys())
    s_keys = list(stats.keys())

    values = {"pop": population[p_keys[0]],
              "cases": stats[s_keys[0]]}

    return values


if __name__ == "__main__":
    # s = scraper()
    # print(s)
    # wc = world_pop()
    # print(wc)
    print(country_data("New Zealand"))
