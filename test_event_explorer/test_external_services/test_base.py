import pytest
import requests

import event_explorer.external_services.base as base


def test_external_service():
    base.Session.request = lambda self, method, url, *args, **kwargs: url
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


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def test_get_url_returns_response_with_200():
    base.Session.request = lambda self, method, url, *args, **kwargs: MockResponse(200)
    external_service = base.ExternalService()
    external_service.base_url = "https://api.dogs.com"
    response = base.get("/bones", external_service)
    assert response.status_code == 200


def test_get_url_raises_with_bad_status_code():
    base.Session.request = lambda self, method, url, *args, **kwargs: MockResponse(500)
    external_service = base.ExternalService()
    external_service.base_url = "https://api.dogs.com"
    with pytest.raises(ValueError):
        response = base.get("/bones", external_service)
