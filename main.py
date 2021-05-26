import click

from CSV import CSV
from soup import Soup


@click.command()
@click.option("--source", default="https://nl.wikipedia.org/wiki/Skaten", help="Specifies the source Wikipedia page.")
@click.option("--destination", default="https://nl.wikipedia.org/wiki/Suezkanaal", help="Specifies the destination "
                                                                                        "Wikipedia page.")
@click.option("--max-clicks", default=5,
              help="Specifies the max amount of clicks the program is going to do before exiting. (The more clicks, "
                   "the longer it will search)")
@click.option("--export-csv", default=False, help="Setting this to true will export the data to a CSV")
def calculate_clicks(source, destination, max_clicks, export_csv):
    soup = Soup(source, destination)
    founded_route = soup.calculate_clicks(int(max_clicks))

    if founded_route is not None:
        print("\r" + source + " --> " + "--> ".join(list(map(lambda a: a.text, founded_route))))
        if export_csv:
            print("Writing to CSV file...")
            CSV(founded_route).export()
    else:
        print("No route found...")


if __name__ == "__main__":
    calculate_clicks()
