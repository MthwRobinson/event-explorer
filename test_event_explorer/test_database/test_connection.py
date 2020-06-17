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


def test_connection_raises_error_with_no_env(monkeypatch):
    fiddler_rds = os.environ.get("FIDDLER_RDS")
    if fiddler_rds:
        del os.environ["FIDDLER_RDS"]

    monkeypatch.setattr(psycopg2, "connect", lambda user, host, dbname: host)
    with pytest.raises(ValueError):
        connection.connect()

    if fiddler_rds:
        os.environ["FIDDLER_RDS"] = fiddler_rds
