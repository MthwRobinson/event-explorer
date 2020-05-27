from event_explorer.database.connection import connect


connection = None


def _connect():
    """Establishing connection as a module level variable so a new connection is not
    established for each query."""
    global connection
    connection = connect()


def load_attendee(attendee, event_id):
    """Loads an attendee into the database to be served to the front end.

    Parameters
    ----------
    attendee : Attendee
        The attendee to load into the database
    event_id : str
        The event id for the event the attendee has attended
    """
    _connect()
    values = (
        event_id,
        attendee.get_first_name(),
        attendee.get_last_name(),
        attendee.get_email(),
    )
    sql = """
    INSERT INTO event_explorer.attendees
    (event_id, first_name, last_name, email)
    VALUES
    (%s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    connection.commit()
