# import libraries
from functions import WebDriver
import warnings


DEMO_URL = 'https://www.worldometers.info/coronavirus/'
WP_DEMO_URL = 'https://www.worldometers.info/world-population/'

# Ignore warnings about PhantomJS depreciation
warnings.filterwarnings('ignore')

timeout = 5


def scraper(url=DEMO_URL, DEBUG=False):
    if DEBUG is True:
        print(url)
    try:
        values = WebDriver(url, timeout).get_url()
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
    if DEBUG is True:
        print(url)
    try:
        values = WebDriver(url, timeout).get_url()
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
        return "https://www.worldometers.info/coronavirus/country/{}".format(country)


def country_pop(country, DEBUG=True):
    url = country_url(country, "population")
    if DEBUG is True:
        print(url)
    try:
        values = WebDriver(url, timeout).get_url()
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
        stats = {titles[0].get_text().lstrip(): counts[1].get_text()}

        return stats

    except IndexError:
        return False


def country_stat(country, DEBUG=True):
    url = country_url(country, "infected")
    if url == "not-supported":
        stats = {"place-holder": "708"}
        return stats
    if DEBUG is True:
        print(url)

    stats = scraper(url)

    return stats


def country_data(country, DEBUG=False):
    population = country_pop(country, DEBUG)
    stats = country_stat(country, DEBUG)
    p_keys = list(population.keys())
    s_keys = list(stats.keys())

    values = {"pop": population[p_keys[0]],
              "cases": stats[s_keys[0]]}

    return values


if __name__ == "__main__":
    s = scraper()
    print(s)
