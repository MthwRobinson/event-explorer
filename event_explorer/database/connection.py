import os
import psycopg2


def connect():
    host = os.environ.get("FIDDLER_RDS", None)
    if not host:
        raise ValueError("FIDDLER_RDS environmental variable is not defined.")
    return psycopg2.connect(user="master", dbname="event_explorer", host=host)
