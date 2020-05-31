import datetime
from dateutil import tz
import os

import pytest

import event_explorer.external_services.zoom as zoom_service


class MockResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = 200

    def json(self):
        return self.response


TEST_EVENT = {
    "uuid": "12345",
    "topic": "Dogs.com Info Session",
    "start_time": "2020-04-11T03:04:00Z",
    "timezone": "America/New_York",
}


TEST_ATTENDEES = {
    "registrants": [
        {"first_name": "Tiki", "last_name": "Robinson", "email": "tiki@robinson.io",}
    ]
}


def test_zoom_gets_token_from_eviron(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "TEST_TOKEN")
    zoom = zoom_service.Zoom()
    assert zoom.headers["Authorization"].startswith("Bearer")


def test_zoom_raises_error_with_no_token(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: None)
    with pytest.raises(ValueError):
        zoom = zoom_service.Zoom()


def test_zoom_loads_from_dict():
    event = zoom_service.ZoomEvent.from_dict(TEST_EVENT)
    assert (
        event.get_id(),
        event.get_name(),
        event.get_time(),
        event.get_description(),
    ) == (
        TEST_EVENT["uuid"],
        TEST_EVENT["topic"],
        datetime.datetime(2020, 4, 10, 23, 4, tzinfo=tz.gettz("America/New_York")),
        None,
    )


def test_zoom_loads_from_id(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "TEST_TOKEN")
    monkeypatch.setattr(
        zoom_service, "get", lambda url, session: MockResponse(TEST_EVENT)
    )
    event = zoom_service.ZoomEvent.from_id("12345")
    assert (
        event.get_id(),
        event.get_name(),
        event.get_time(),
        event.get_description(),
    ) == (
        TEST_EVENT["uuid"],
        TEST_EVENT["topic"],
        datetime.datetime(2020, 4, 10, 23, 4, tzinfo=tz.gettz("America/New_York")),
        None,
    )


def test_zoom_event_loads_attendees(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "TEST_TOKEN")
    monkeypatch.setattr(
        zoom_service, "get", lambda url, session: MockResponse(TEST_ATTENDEES)
    )
    event = zoom_service.ZoomEvent.from_dict(TEST_EVENT)
    attendees = event.get_attendees()
    assert (
        attendees[0].get_first_name(),
        attendees[0].get_last_name(),
        attendees[0].get_email(),
    ) == ("Tiki", "Robinson", "tiki@robinson.io")
