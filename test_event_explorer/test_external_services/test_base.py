import pytest
import requests

import event_explorer.external_services.base as base


base.Session.request = lambda self, method, url, *args, **kwargs: url


def test_external_service():
    external_service = base.ExternalService()
    external_service.base_url = "https://api.dogs.com"
    assert external_service.get("/bones") == "https://api.dogs.com/bones"


@pytest.mark.parametrize(
    "method",
    [
        base.Event(dict()).get_id,
        base.Event(dict()).get_name,
        base.Event(dict()).get_time,
        base.Event(dict()).get_description,
        base.Event(dict()).get_attendees,
        base.Attendee(dict()).get_first_name,
        base.Attendee(dict()).get_last_name,
        base.Attendee(dict()).get_email,
    ],
)
def test_stub_methods_raise_error(method):
    with pytest.raises(NotImplementedError):
        method()


@pytest.mark.parametrize("cls", [base.Event(dict()), base.Attendee(dict())])
def test_base_classes_return_source(cls):
    cls.source = "Test Source"
    assert cls.get_source() == "Test Source"
