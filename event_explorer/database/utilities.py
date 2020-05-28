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


def load_event(event):
    """Loads an event into the database to be served to the front end.

    Parameters
    ----------
    event : Event
        The event to load into the database
    """
    _connect()
    values = (
        event.get_id(),
        event.get_name(),
        event.get_time(),
        event.get_description(),
        event.get_source(),
    )
    sql = """
    INSERT INTO event_explorer.events
    (id, name, description, start_time, source)
    VALUES
    (%s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    connection.commit()


def delete_event(event_id):
    """Deletes an event from the event table

    Parameters
    ----------
    event_id : str
        The id for the event to delete
    """
    sql = f"""
        DELETE FROM event_explorer.events
        WHERE id = "{event_id}"
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()


def delete_event_attendees(event_id):
    """Deletes attendees for the specified event

    Parameters
    ----------
    event_id : str
        The id for the event to delete
    """
    sql = f"""
        DELETE FROM event_explorer.attendees
        WHERE event_id = "{event_id}"
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
