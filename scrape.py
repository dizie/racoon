# import libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import warnings

DEMO_URL = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61'


def scraper(url=DEMO_URL):
    # Ignore warnings about PhantomJS depreciation
    warnings.filterwarnings('ignore')

    # specify the url
    print(url)
    # run firefox webdriver from executable path of your choice
    # driver = webdriver.Firefox()
    # Run PhantomJS headless browser
    driver = webdriver.PhantomJS()

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
    values = soup.find_all('text')
    # build the relevant data set
    stats = {values[0].get_text(): values[1].get_text(),
             values[2].get_text(): values[3].get_text(),
             values[4].get_text(): values[5].get_text()}

    return stats


if __name__ == "__main__":
    s = scraper()
    print(s)

