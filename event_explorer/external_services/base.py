import pandas as pd
from requests import Session


class ExternalService(Session):
    """Base class for making API calls from across REST APIs."""

    base_url = None

    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.__class__.__name__

    def request(self, method, url, *args, **kwargs):
        url = self._create_url(url)
        return super().request(method, url, *args, **kwargs)

    def _create_url(self, url):
        if not self.base_url:
            raise ValueError("Base URL for the external service has not been set.")
        return f"{self.base_url}{url}"


class Event:
    """Base class for normalizing events from across sources."""

    source = None
    attendees = None

    def __init__(self, event):
        self.event = event

    def get_id(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_source(self):
        return self.source

    def get_time(self):
        raise NotImplementedError

    def get_description(self):
        raise NotImplementedError

    def get_attendees(self):
        raise NotImplementedError


class Attendee:
    """Base class for normalizing attendee information from across sources."""

    source = None

    def __init__(self, attendee):
        self.attendee = attendee

    def get_first_name(self):
        raise NotImplementedError

    def get_last_name(self):
        raise NotImplementedError

    def get_email(self):
        raise NotImplementedError

    def get_source(self):
        return self.source


def get(url, session):
    """Makes a call to the Eventbrite API using.

    Parameters
    ----------
    url : str
        The endpoint to call. Do not include the base url.
    session : request.Session
        The external service to use for the API call

    Returns
    -------
    response : requests.Response
        The response from the Eventbrite API
    """
    response = session.get(url)
    if response.status_code == 200:
        return response
    else:
        status_code = response.status_code
        raise ValueError(f"{session} API failed. Status code: {status_code}")


def events_to_dataframe(events):
    """Converts a list of events into a pandas dataframe

    Parameters
    ----------
    events : list
        A list of events

    Returns
    -------
    events_dataframe : pd.DataFrame
        A dataframe containing the event information
    """
    columns = ["id", "name", "source", "time", "description"]
    data = {column: list() for column in columns}
    for event in events:
        data["id"].append(event.get_id())
        data["name"].append(event.get_name())
        data["source"].append(event.get_source())
        data["time"].append(event.get_time())
        data["description"].append(event.get_description())
    return pd.DataFrame(data)


def attendees_to_dataframe(attendees):
    """Converts a list of attendees into a pandas dataframe

    Parameters
    ----------
    attendees : list
        A list of attendees

    Returns
    -------
    attendees_dataframe : pd.DataFrame
        A dataframe containing the attendee information
    """
    columns = ["first_name", "last_name", "email", "source"]
    data = {column: list() for column in columns}
    for attendee in attendees:
        data["first_name"].append(attendee.get_first_name())
        data["last_name"].append(attendee.get_last_name())
        data["email"].append(attendee.get_email())
        data["source"].append(attendee.get_source())
    return pd.DataFrame(data)
