from event_explorer.database.connection import connect


connection = None


def _connect(**connection_kwargs):
    """Establishing connection as a module level variable so a new connection is not
    established for each query. Optionally, accepts keyword arugments that are passed to
    psycopg2.connect. Any keyword args take precedence over environmental variables and
    defaults."""
    global connection
    if not connection:
        connection = connect(**connection_kwargs)


def load_attendee(attendee, event_id, source, **connection_kwargs):
    """Loads an attendee into the database to be served to the front end.

    Parameters
    ----------
    attendee : Attendee
        The attendee to load into the database
    event_id : str
        The event id for the event the attendee has attended
    """
    _connect(**connection_kwargs)
    values = (
        event_id,
        source,
        attendee.get_first_name(),
        attendee.get_last_name(),
        attendee.get_email(),
    )
    sql = """
    INSERT INTO event_explorer.attendees
    (event_id, source, first_name, last_name, email)
    VALUES
    (%s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    connection.commit()


def load_event(event, **connection_kwargs):
    """Loads an event into the database to be served to the front end.

    Parameters
    ----------
    event : Event
        The event to load into the database
    """
    _connect(**connection_kwargs)
    values = (
        event.get_id(),
        event.get_name(),
        event.get_time(),
        event.get_description(),
        event.get_source(),
    )
    sql = """
    INSERT INTO event_explorer.events
    (id, name, start_time, description, source)
    VALUES
    (%s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    connection.commit()


def delete_event(event_id, source, **connection_kwargs):
    """Deletes an event from the event table

    Parameters
    ----------
    event_id : str
        The id for the event to delete
    source : str
        The source for the event to delete
    """
    _connect(**connection_kwargs)
    sql = f"""
        DELETE FROM event_explorer.events
        WHERE id = '{event_id}'
        AND source = '{source}'
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()


def delete_event_attendees(event_id, source, **connection_kwargs):
    """Deletes attendees for the specified event

    Parameters
    ----------
    event_id : str
        The id for the event to delete
    source : str
        The source for the event to delete
    """
    _connect(**connection_kwargs)
    sql = f"""
        DELETE FROM event_explorer.attendees
        WHERE event_id = '{event_id}'
        AND source = '{source}'
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()


def load_event_data(event, **connection_kwargs):
    """Loads an event and attendees into the database

    event : event_explorer.external_service.base.Event
        The entry to load into the database
    """
    event_id, source = event.get_id(), event.get_source()
    delete_event(event_id, source, **connection_kwargs)
    delete_event_attendees(event_id, source, **connection_kwargs)
    load_event(event, **connection_kwargs)

    for attendee in event.get_attendees():
        load_attendee(attendee, event_id, source, **connection_kwargs)
