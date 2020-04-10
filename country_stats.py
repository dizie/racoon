from scrape import country_data

DEBUG = False


def get_value(values):
    population = int(values["pop"].replace(',', ''))
    cases = int(values["cases"].replace(',', ''))
    values["percent"] = "{0:.2f}%".format(cases / population * 100, 2)

    return values


def main():
    countries = ["Australia", "Canada", "New Zealand", "US"]

    for c in countries:
        stats = country_data(c)
        stats = get_value(stats)

        print(c, "=",  stats["cases"], "/", stats["pop"], "({})".format(stats["percent"]))


if __name__ == "__main__":
    main()
