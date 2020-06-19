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
    real_token = os.environ.get("ZOOM_API_SECRET", None)
    os.environ["ZOOM_API_SECRET"] = "TEST_TOKEN"

    real_key = os.environ.get("ZOOM_API_KEY")
    os.environ["ZOOM_API_KEY"] = "TEST_KEY"

    zoom = zoom_service.Zoom()
    assert zoom.headers["Authorization"].startswith("Bearer")

    if real_token:
        os.environ["ZOOM_API_SECRET"] = real_token
    if real_key:
        os.environ["ZOOM_API_KEY"] = real_key


def test_zoom_raises_error_with_no_token(monkeypatch):
    real_token = os.environ.get("ZOOM_API_SECRET", None)
    if "ZOOM_API_SECRET" in os.environ:
        del os.environ["ZOOM_API_SECRET"]

    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: None)
    with pytest.raises(ValueError):
        zoom = zoom_service.Zoom()

    if real_token:
        os.environ["ZOOM_API_SECRET"] = real_token


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
    real_token = os.environ.get("ZOOM_API_SECRET", None)
    os.environ["ZOOM_API_SECRET"] = "TEST_TOKEN"

    real_key = os.environ.get("ZOOM_API_KEY")
    os.environ["ZOOM_API_KEY"] = "TEST_KEY"

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

    if real_token:
        os.environ["ZOOM_API_SECRET"] = real_token
    if real_key:
        os.environ["ZOOM_API_KEY"] = real_key


def test_zoom_event_loads_attendees(monkeypatch):
    real_token = os.environ.get("ZOOM_API_SECRET", None)
    os.environ["ZOOM_API_SECRET"] = "TEST_TOKEN"

    real_key = os.environ.get("ZOOM_API_KEY")
    os.environ["ZOOM_API_KEY"] = "TEST_KEY"

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

    if real_token:
        os.environ["ZOOM_API_SECRET"] = real_token
    if real_key:
        os.environ["ZOOM_API_KEY"] = real_key


def test_load_zoom(monkeypatch):
    def mock_get(url):
        if "registrants" in url:
            response = TEST_ATTENDEES
        else:
            response = {
                "meetings": [TEST_EVENT, TEST_EVENT, TEST_EVENT, TEST_EVENT],
                "page_count": 1,
                "page_number": 1,
            }
        return MockResponse(response)

    zoom_service.Zoom.__init__ = lambda self: None
    zoom_service.Zoom.get = lambda self, url: mock_get(url)

    monkeypatch.setattr(zoom_service, "load_event_data", lambda *args, **kwargs: None)
    zoom_service.load_zoom()


def test_list_users(monkeypatch):
    def mock_get(url):
        response = {
            "page_count": 1,
            "page_number": 1,
            "page_size": 30,
            "total_records": 1,
            "users": [
                {
                    "first_name": "Tiki",
                    "last_name": "Parrot",
                    "email": "tiki@parrots.ai",
                    "status": "active",
                }
            ],
        }
        return MockResponse(response)

    zoom_service.Zoom.__init__ = lambda self: None
    zoom_service.Zoom.get = lambda self, url: mock_get(url)

    users = zoom_service.list_zoom_users()
    assert users == [
        {
            "first_name": "Tiki",
            "last_name": "Parrot",
            "email": "tiki@parrots.ai",
            "status": "active",
        }
    ]
