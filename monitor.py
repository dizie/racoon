from scrape import scraper
import time

URL = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61'
DEBUG = False


def main():
    cases = None
    casualties = None
    recoveries = None

    while True:
        if DEBUG is True:
            print("Going for another run")

        results = scraper(URL, DEBUG)
        print(results)
        r_cases = results["Total Confirmed"].replace(',', '')
        r_casualties = int(results["Total Deaths"].replace(',', ''))
        r_recoveries = results["Total Recovered"].replace(',', '')

        if cases is None:
            cases = r_cases
            casualties = r_casualties
            recoveries = r_recoveries

        if cases != r_cases:
            if cases < r_cases:
                diff = r_cases - cases
                cases = r_cases
                print("Confirmed cases have risen by: {}. Count now stands at: {}".format(diff, cases))
            elif cases > r_cases:
                diff = cases - r_cases
                cases = r_cases
                print("Confirmed cases have decreased by: {}. Count now stands at: {}".format(diff, cases))

        if casualties != r_casualties:
            if casualties < r_casualties:
                diff = r_casualties - casualties
                casualties = r_casualties
                print("Fatal cases have risen by: {}. Count now stands at: {}".format(diff, casualties))
            elif casualties > r_casualties:
                diff = casualties - r_casualties
                casualties = r_casualties
                print("Fatal cases have decreased by: {}. Count now stands at: {}".format(diff, casualties))

        if recoveries != r_recoveries:
            if recoveries < r_recoveries:
                diff = r_recoveries - recoveries
                recoveries = r_recoveries
                print("Recovery cases have risen by: {}. Count now stands at: {}".format(diff, recoveries))
            if recoveries > r_recoveries:
                diff = recoveries - r_recoveries
                recoveries = r_recoveries
                print("Recovery cases have decreased by: {}. Count now stands at: {}".format(diff, recoveries))

        time.sleep(60)


if __name__ == "__main__":
    main()
