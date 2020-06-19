import os

import psycopg2
import pytest

import event_explorer.database.connection as connection


def test_connection_works_with_env(monkeypatch):
    current_environ = dict(os.environ)
    os.environ["FIDDLER_RDS"] = "test_host"
    os.environ["RDS_USER"] = "test_user"

    monkeypatch.setattr(psycopg2, "connect", lambda user, dbname, host: (user, host))
    assert connection.connect() == ("test_user", "test_host")

    del os.environ["FIDDLER_RDS"]
    del os.environ["RDS_USER"]

    for variable, value in current_environ.items():
        os.environ[variable] = value


def test_connection_works_with_defaults(monkeypatch):
    current_environ = dict(os.environ)
    os.environ["FIDDLER_RDS"] = "test_host"
    if "RDS_USER" in os.environ:
        del os.environ["RDS_USER"]

    monkeypatch.setattr(psycopg2, "connect", lambda user, dbname, host: (user, host))
    assert connection.connect() == ("master", "test_host")

    del os.environ["FIDDLER_RDS"]

    for variable, value in current_environ.items():
        os.environ[variable] = value


def test_connection_passes_kwargs(monkeypatch):
    current_environ = dict(os.environ)

    monkeypatch.setattr(
        psycopg2,
        "connect",
        lambda **kwargs: (kwargs.get("user"), kwargs.get("password")),
    )
    assert connection.connect(user="tiki", password="jabber") == ("tiki", "jabber")

    del os.environ["FIDDLER_RDS"]

    for variable, value in current_environ.items():
        os.environ[variable] = value


def test_connection_raises_error_with_no_env(monkeypatch):
    fiddler_rds = os.environ.get("FIDDLER_RDS")
    if fiddler_rds:
        del os.environ["FIDDLER_RDS"]

    monkeypatch.setattr(psycopg2, "connect", lambda user, host, dbname: host)
    with pytest.raises(ValueError):
        connection.connect()

    if fiddler_rds:
        os.environ["FIDDLER_RDS"] = fiddler_rds
