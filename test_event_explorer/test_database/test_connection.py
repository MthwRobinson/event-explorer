import os

import psycopg2
import pytest

import event_explorer.database.connection as connection


def test_connection_works_with_env(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: "test_host")
    monkeypatch.setattr(psycopg2, "connect", lambda user, host, dbname: host)
    assert connection.connect() == "test_host"


def test_connetion_raises_error_with_no_env(monkeypatch):
    monkeypatch.setattr(os.environ, "get", lambda *args, **kwargs: None)
    monkeypatch.setattr(psycopg2, "connect", lambda user, host, dbname: host)
    with pytest.raises(ValueError):
        connection.connect()
