import os

import click

from event_explorer.external_services.eventbrite import load_eventbrite
from event_explorer.external_services.zoom import load_zoom


LOAD_OPTIONS = {
    "eventbrite": load_eventbrite,
    "zoom": load_zoom,
}


@click.group()
def main():
    """Welcome for the event explorer CLI! Use --help to learn more about a command."""
    pass


@click.command("events-to-csv")
@click.option("--directory")
@click.option("--source")
@click.option("--max-events", type=int, default=500)
def events_to_csv(directory, source, max_events=500):
    """Saves events from the specified source as CSV files in the specified directory.

    Parameters
    ----------
    directory : str
        The directory in which to save the files
    source : str
        The datasource
    max_events : int
        The max number of events to save
    """
    if source not in LOAD_OPTIONS:
        raise ValueError(f"Bad source. Valid sources are: {list(LOAD_OPTIONS.keys())}")

    events, attendees = LOAD_OPTIONS[source](max_events=max_events, target="dataframe")
    filename = os.path.join(directory, f"{source}.csv")
    print(f"Writing to file: {filename}")
    events.to_csv(filename, index=False)

    attendees_directory = os.path.join(directory, source)
    if not os.path.exists(attendees_directory):
        os.mkdir(attendees_directory)

    for key, event_attendees in attendees.items():
        filename = os.path.join(attendees_directory, f"{key.replace('/', '-')}.csv")
        filename = filename.replace(" ", "-").replace("'", "")
        print(f"Writing to file: {filename}")
        event_attendees.to_csv(filename, index=False)


main.add_command(events_to_csv)


if __name__ == "__main__":
    main()
