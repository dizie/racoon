from scrape2 import scraper, world_pop
import time
import logging

# URL = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61'
URL = 'https://www.worldometers.info/coronavirus/'
WP_URL = 'https://www.worldometers.info/world-population/'
DEBUG = False
WAIT_TIME = 27

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

        wp = (world_pop(WP_URL, DEBUG))
        results = scraper(URL, DEBUG)
        if results is False:
            logger.error("An error occurred retrieving stats from {}. Trying again in {}".format(URL, WAIT_TIME))
        else:
            try:
                r_keys = list(results.keys())
                r_cases = int(results[r_keys[0]].replace(',', ''))
                r_casualties = int(results[r_keys[1]].replace(',', ''))
                r_recoveries = int(results[r_keys[2]].replace(',', ''))

                clean_fatal_rate = r_casualties / r_cases * 100
                fatal_rate = "{0:.2f}%".format(clean_fatal_rate, 2)
                clean_recov_rate = r_recoveries / r_cases * 100
                recover_rate = "{0:.2f}%".format(clean_recov_rate, 2)
                clean_active_cases = r_cases - r_casualties - r_recoveries
                active_rate = "{0:.2f}%".format(clean_active_cases / r_cases * 100, 2)
                active_cases = f'{clean_active_cases:,}'
                clean_closed_cases = r_cases - clean_active_cases
                closed_rate = "{0:.2f}%".format(clean_closed_cases / r_cases * 100, 2)
                closed_cases = f'{clean_closed_cases:,}'
                closed_fatal_rate = "{0:.2f}%".format(r_casualties / clean_closed_cases * 100, 2)
                closed_recov_rate = "{0:.2f}%".format(r_recoveries / clean_closed_cases * 100, 2)



                results["Fatality Rate"] = fatal_rate
                results["Recovered Rate"] = recover_rate
                results["Active Cases"] = active_cases
                results["Active Cases %"] = active_rate
                results["Closed Cases"] = closed_cases
                results["Closed Cases %"] = closed_rate
                results["Closed Fatality Rate"] = closed_fatal_rate
                results["Closed Recovered Rate"] = closed_recov_rate

                results.update(wp)

                wp_keys = list(wp.keys())
                wp_count = int(wp[wp_keys[0]].replace(',', ''))

                clean_infect_rate = r_cases / wp_count * 100
                infect_rate = "{0:.2f}%".format(clean_infect_rate, 2)

                results["Total Population Infected"] = infect_rate

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
                logger.error("KeyError in data. Trying again in {}. Data: {}".format(WAIT_TIME, results))
                pass
            except ValueError:
                logger.error("ValueError in data. Trying again in {}. Data: {}".format(WAIT_TIME, wp))
                pass

        time.sleep(WAIT_TIME)


if __name__ == "__main__":
    main()
