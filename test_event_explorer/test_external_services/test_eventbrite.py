import datetime
import os

import pytest

import event_explorer.external_services.eventbrite as eventbrite_service


class MockResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = 200

    def json(self):
        return self.response


TEST_EVENT = {
    "id": "12345",
    "name": {"text": "Dogs.com Info Session"},
    "description": {"text": "Where dogs go to dog!"},
    "start": {"local": "2020-04-11T03:04:00"},
}


TEST_ATTENDEES = {
    "attendees": [
        {
            "profile": {
                "first_name": "Tiki",
                "last_name": "Robinson",
                "email": "tiki@robinson.io",
            }
        }
    ]
}


def test_eventbrite_gets_token_from_eviron(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "TEST_TOKEN")
    eventbrite = eventbrite_service.Eventbrite()
    assert eventbrite.headers["Authorization"] == "Bearer TEST_TOKEN"


def test_eventbrite_raises_error_with_no_token(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: None)
    with pytest.raises(ValueError):
        eventbrite = eventbrite_service.Eventbrite()


def test_eventbrite_loads_from_dict():
    event = eventbrite_service.EventbriteEvent.from_dict(TEST_EVENT)
    assert (
        event.get_id(),
        event.get_name(),
        event.get_time(),
        event.get_description(),
    ) == (
        TEST_EVENT["id"],
        TEST_EVENT["name"]["text"],
        datetime.datetime(2020, 4, 11, 3, 4),
        TEST_EVENT["description"]["text"],
    )


def test_eventbrite_loads_from_id(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "TEST_TOKEN")
    monkeypatch.setattr(
        eventbrite_service, "get", lambda url, session: MockResponse(TEST_EVENT)
    )
    event = eventbrite_service.EventbriteEvent.from_id("12345")
    assert (
        event.get_id(),
        event.get_name(),
        event.get_time(),
        event.get_description(),
    ) == (
        TEST_EVENT["id"],
        TEST_EVENT["name"]["text"],
        datetime.datetime(2020, 4, 11, 3, 4),
        TEST_EVENT["description"]["text"],
    )


def test_eventbrite_event_loads_attendees(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "TEST_TOKEN")
    monkeypatch.setattr(
        eventbrite_service, "get", lambda url, session: MockResponse(TEST_ATTENDEES)
    )
    event = eventbrite_service.EventbriteEvent.from_dict(TEST_EVENT)
    attendees = event.get_attendees()
    assert (
        attendees[0].get_first_name(),
        attendees[0].get_last_name(),
        attendees[0].get_email(),
    ) == ("Tiki", "Robinson", "tiki@robinson.io")


def test_load_eventbrite(monkeypatch):
    def mock_get(url):
        if "attendees" in url:
            response = {"attendees": TEST_ATTENDEES}
        else:
            response = {
                "events": [TEST_EVENT, TEST_EVENT, TEST_EVENT],
                "pagination": {
                    "continuation": "abc",
                    "has_more_items": "continuation" not in url,
                },
            }
        return MockResponse(response)

    eventbrite_service.Eventbrite.__init__ = lambda self: None
    eventbrite_service.Eventbrite.get = lambda self, url: mock_get(url)

    monkeypatch.setattr(eventbrite_service, "load_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        eventbrite_service, "delete_event", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        eventbrite_service, "load_attendee", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        eventbrite_service, "delete_event_attendees", lambda *args, **kwargs: None
    )
    eventbrite_service.load_eventbrite()
