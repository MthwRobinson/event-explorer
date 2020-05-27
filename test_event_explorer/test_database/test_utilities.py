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
    monkeypatch.setattr(utilities, "connect", lambda: MockConnection())
    utilities.load_attendee(MockAttendee(), event_id="12345")
