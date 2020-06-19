import datetime

import event_explorer.database.utilities as utilities


class MockCursor:
    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    def execute(self, *args, **kwargs):
        pass


class MockConnection:
    def cursor(self):
        return MockCursor()

    def commit(self):
        pass


class MockAttendee:
    def get_id(self):
        return "8675309"

    def get_first_name(self):
        return "Chester"

    def get_last_name(self):
        return "Robinson"

    def get_email(self):
        return "chester.robinson@dogs.com"


def test_load_attendee(monkeypatch):
    monkeypatch.setattr(utilities, "connect", lambda **kwargs: MockConnection())
    utilities.load_attendee(MockAttendee(), event_id="12345", source="Fake Source")


class MockEvent:
    def get_id(self):
        return "12345"

    def get_name(self):
        return "Big Dog Party!"

    def get_source(self):
        return "Dogs.com"

    def get_time(self):
        return datetime.datetime(2020, 1, 10, 3, 20)

    def get_description(self):
        return "Where dogs go to dog!"

    def get_attendees(self):
        return []


def test_load_event(monkeypatch):
    monkeypatch.setattr(utilities, "connect", lambda **kwargs: MockConnection())
    utilities.load_event(MockEvent())


def test_delete_event(monkeypatch):
    monkeypatch.setattr(utilities, "connect", lambda **kwargs: MockConnection())
    utilities.delete_event("12345", "Fake Source")


def test_delete_event_attendees(monkeypatch):
    monkeypatch.setattr(utilities, "connect", lambda **kwargs: MockConnection())
    utilities.delete_event_attendees("12345", "Fake Source")


def test_load_event_data(monkeypatch):
    monkeypatch.setattr(utilities, "connect", lambda **kwargs: MockConnection())
    utilities.load_event_data(MockEvent())
