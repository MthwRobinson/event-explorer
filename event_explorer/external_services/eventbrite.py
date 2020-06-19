import datetime
import os

import requests

from event_explorer.database.utilities import load_event_data
from event_explorer.external_services.base import Attendee, Event, ExternalService, get


class Eventbrite(ExternalService):
    base_url = "https://www.eventbriteapi.com/v3"

    def __init__(self):
        super().__init__()
        self._set_header_token()

    def _set_header_token(self):
        token = os.environ.get("EVENTBRITE_TOKEN", None)
        if not token:
            raise ValueError("EVENTBRITE_TOKEN environmental variable not set")
        self.headers.update({"Authorization": f"Bearer {token}"})


class EventbriteEvent(Event):
    """Class for representing Eventbrite events that are fetched from the API."""

    source = "Eventbrite"

    @classmethod
    def from_dict(cls, event):
        return cls(event)

    @classmethod
    def from_id(cls, event_id):
        response = get(f"/events/{event_id}", Eventbrite())
        return cls(response.json())

    def get_id(self):
        return self.event["id"]

    def get_name(self):
        return self.event["name"]["text"]

    def get_time(self):
        time = self.event["start"]["local"]
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

    def get_description(self):
        return self.event["description"]["text"]

    def get_attendees(self):
        if self.attendees is None:
            event_id = self.get_id()
            response = get(f"/events/{event_id}/attendees", Eventbrite())
            self.attendees = [
                EventbriteAttendee.from_dict(attendee)
                for attendee in response.json()["attendees"]
            ]
        return self.attendees


class EventbriteAttendee(Attendee):
    """Class for representing attendees of Eventbrite events."""

    source = "Eventbrite"

    @classmethod
    def from_dict(cls, attendee):
        return cls(attendee)

    def get_first_name(self):
        return self.attendee["profile"].get("first_name", None)

    def get_last_name(self):
        return self.attendee["profile"].get("last_name", None)

    def get_email(self):
        return self.attendee["profile"].get("email", None)


def load_eventbrite(max_events=500, **connection_kwargs):
    """Loads Eventbrite events into the database

    Parameters
    ----------
    max_events : int
        The maximum number of events to load into the database
    """
    eventbrite = Eventbrite()
    response = eventbrite.get("/users/me/events?order_by=start_desc")
    has_more_items = response.json()["pagination"].get("has_more_items", None)
    count = 0
    while count < max_events and has_more_items:
        for item in response.json()["events"]:
            event = EventbriteEvent.from_dict(item)
            load_event_data(event, **connection_kwargs)
            count += 1

        continuation = response.json()["pagination"].get("continuation", None)
        response = eventbrite.get(
            f"/users/me/events?order_by=start_desc&continuation={continuation}"
        )
        has_more_items = response.json()["pagination"].get("has_more_items", None)
