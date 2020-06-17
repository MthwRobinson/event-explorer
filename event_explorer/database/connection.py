import os
import psycopg2


def connect():
    host = os.environ.get("FIDDLER_RDS", None)
    if not host:
        raise ValueError("FIDDLER_RDS environmental variable is not defined.")
    rds_user = os.environ.get("RDS_USER", "master")
    return psycopg2.connect(user=rds_user, dbname="event_explorer", host=host)
