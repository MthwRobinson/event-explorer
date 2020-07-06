import datetime
from dateutil import tz
import os
import time

import jwt

from event_explorer.database.utilities import load_event_data
from event_explorer.external_services.base import (
    Attendee,
    Event,
    ExternalService,
    get,
    events_to_dataframe,
    attendees_to_dataframe,
)


class Zoom(ExternalService):
    base_url = "https://api.zoom.us/v2"

    def __init__(self):
        super().__init__()
        self._set_header_token()

    def _set_header_token(self):
        key = os.environ.get("ZOOM_API_KEY", None)
        secret = os.environ.get("ZOOM_API_SECRET", None)
        if not all([key, secret]):
            raise ValueError(
                "ZOOM_API_KEY or ZOOM_API_SECRET environmental variable not set"
            )
        token = generate_jwt(key, secret)
        self.headers.update({"Authorization": f"Bearer {token}"})


class ZoomEvent(Event):
    """Class for representing Zoom events that are fetched from the API."""

    source = "Zoom"

    @classmethod
    def from_dict(cls, event):
        return cls(event)

    @classmethod
    def from_id(cls, event_id):
        response = get(f"/meetings/{event_id}", Zoom())
        return cls(response.json())

    def get_id(self):
        return self.event["uuid"]

    def get_name(self):
        return self.event["topic"]

    def get_time(self):
        time = self.event["start_time"]
        from_zone = tz.gettz("UTC")
        time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        time = time.replace(tzinfo=from_zone)

        to_zone = tz.gettz(self.event["timezone"])
        return time.astimezone(to_zone)

    def get_description(self):
        return self.event.get("agenda")

    def get_attendees(self):
        if self.attendees is None:
            event_id = self.get_id()
            response = get(f"/meetings/{event_id}/registrants", Zoom())
            self.attendees = [
                ZoomAttendee.from_dict(attendee)
                for attendee in response.json()["registrants"]
            ]
        return self.attendees


class ZoomAttendee(Attendee):
    """Class for representing attendees of Zoom events."""

    source = "Zoom"

    @classmethod
    def from_dict(cls, attendee):
        return cls(attendee)

    def get_first_name(self):
        return self.attendee.get("first_name", None)

    def get_last_name(self):
        return self.attendee.get("last_name", None)

    def get_email(self):
        return self.attendee.get("email", None)


def generate_jwt(key, secret):
    """Generates a JSON web token, which is used to authorize requests
    to the Zoom API:

    Parameters
    ----------
    key : str
        The Zoom API key for the account
    secret : str
        The Zoom API secret for the account

    Returns
    -------
    token : str
        The token to use in API requests
    """
    header = {"alg": "HS256", "typ": "JWT"}

    payload = {"iss": key, "exp": int(time.time() + 3600)}

    token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
    return token.decode("utf-8")


def load_zoom(user_id="me", max_events=500, target="database", **connection_kwargs):
    """Loads Zoom events into the RDS database.

    Parameters
    ----------
    user_id : str
        The user id of the account that organized the meetings
    max_events : int
        The maximum number of events to load into the database
    target : str
        "database" or "dataframe". If "dataframe", the results do not write to the
        database. Instead, they are written to dataframes so they can be stored as CSVs.
    """
    if target not in ["database", "dataframe"]:
        raise ValueError("The target must be 'database' or 'dataframe'.")
    events = list()
    attendees = dict()
    zoom = Zoom()
    response = zoom.get(f"/users/{user_id}/meetings")
    pages = response.json().get("page_count")
    count = 0
    for page_number in reversed(range(1, pages + 1)):
        response = zoom.get(f"/users/{user_id}/meetings?page_number={page_number}")
        meetings = response.json()["meetings"]
        for item in reversed(meetings):
            print(f"Loading event number {count+1}/{max_events}")
            meeting = ZoomEvent.from_dict(item)
            if target == "database":
                load_event_data(meeting, **connection_kwargs)
            else:
                events.append(meeting)
                key = f"{meeting.get_source()}-{meeting.get_id()}-{meeting.get_name()}"
                attendees[key] = attendees_to_dataframe(meeting.get_attendees())
            count += 1
            if count >= max_events:
                break

    return events_to_dataframe(events), attendees


def list_zoom_users():
    """Lists all of the users for the Zoom account.

    Returns
    -------
    users : list(dict)
        A list of all the users for the account.
    """
    zoom = Zoom()
    response = zoom.get("/users")
    return response.json()["users"]
