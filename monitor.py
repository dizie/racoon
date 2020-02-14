from scrape import scraper
import time
import logging

URL = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61'
DEBUG = False
WAIT_TIME = 44

LOG_LEVEL = logging.INFO

if DEBUG is True:
    LOG_LEVEL = logging.DEBUG

LOG_PATH = '/tmp/racoon.log'

logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=LOG_PATH,
                    level=LOG_LEVEL)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)


def main():
    cases = None
    casualties = None
    recoveries = None

    while True:
        if DEBUG is True:
            print("Going for another run")

        results = scraper(URL, DEBUG)
        if results is False:
            logger.error("An error occurred retrieving stats from {}. Trying again in {}".format(URL, WAIT_TIME))
        else:
            try:
                r_cases = int(results["Total Confirmed"].replace(',', ''))
                r_casualties = int(results["Total Deaths"].replace(',', ''))
                r_recoveries = int(results["Total Recovered"].replace(',', ''))

                fatal_rate = "{0:.2f}%".format(r_casualties / r_cases * 100, 2)
                recover_rate = "{0:.2f}%".format(r_recoveries / r_cases * 100, 2)
                active_cases = f'{r_cases - r_casualties - r_recoveries:,}'

                results["Active Cases"] = active_cases
                results["Fatality Rate"] = fatal_rate
                results["Recovery Rate"] = recover_rate

                logger.info(results)

                if cases is None:
                    cases = r_cases
                    casualties = r_casualties
                    recoveries = r_recoveries

                if cases != r_cases:
                    if cases < r_cases:
                        diff = r_cases - cases
                        cases = r_cases
                        logger.info("Confirmed cases have risen by: {}. Count now stands at: {}".format(diff, cases))
                    elif cases > r_cases:
                        diff = cases - r_cases
                        cases = r_cases
                        logger.info("Confirmed cases have decreased by: {}. Count now stands at: {}".format(diff, cases))

                if casualties != r_casualties:
                    if casualties < r_casualties:
                        diff = r_casualties - casualties
                        casualties = r_casualties
                        logger.info("Fatal cases have risen by: {}. Count now stands at: {}. Rate: {}".format(diff, casualties, fatal_rate))
                    elif casualties > r_casualties:
                        diff = casualties - r_casualties
                        casualties = r_casualties
                        logger.info("Fatal cases have decreased by: {}. Count now stands at: {}. Rate: {}".format(diff, casualties,fatal_rate))

                if recoveries != r_recoveries:
                    if recoveries < r_recoveries:
                        diff = r_recoveries - recoveries
                        recoveries = r_recoveries
                        logger.info("Recovery cases have risen by: {}. Count now stands at: {}. Rate: {}".format(diff, recoveries, recover_rate))
                    if recoveries > r_recoveries:
                        diff = recoveries - r_recoveries
                        recoveries = r_recoveries
                        logger.info("Recovery cases have decreased by: {}. Count now stands at: {}. Rate: {}".format(diff, recoveries, recover_rate))
            except KeyError:
                logger.error("Key error in data. Trying again in {}. Data: {}".format(WAIT_TIME, results))
                pass

        time.sleep(WAIT_TIME)


if __name__ == "__main__":
    main()
