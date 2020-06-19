import os
import psycopg2


def connect(**kwargs):
    """Connects to the database using the following order of precedence:
        1. Keyword arguments passed to the function
        2. Settings available in environmental variables
        3. Default values

    Accepts any keyword argument that can be passed to psycopg2.connect"""
    connection_kwargs = dict()

    host = kwargs.get("host", os.environ.get("FIDDLER_RDS", None))
    if not host:
        raise ValueError("FIDDLER_RDS environmental variable is not defined.")
    connection_kwargs["host"] = host

    rds_user = kwargs.get("user", os.environ.get("RDS_USER", "master"))
    connection_kwargs["user"] = rds_user

    dbname = kwargs.get("dbname", "event_explorer")
    connection_kwargs["dbname"] = dbname

    password = kwargs.get("password", None)
    if password:
        connection_kwargs["password"] = password

    return psycopg2.connect(**connection_kwargs)
