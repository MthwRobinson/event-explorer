# Fiddler Analytics Event Explorer
[![coverage report](https://gitlab.com/fiddler-analytics/event-explorer/badges/master/coverage.svg)](https://gitlab.com/fiddler-analytics/event-explorer/commits/master)


## Getting started
To install the Python app, run the following command:

```
make pip-install
```

To install the database tables, you'll need to add the URI of the RDS database as an
environmental variable called `FIDDLER_RDS` and install `psql` using the following
commmand:

```
sudo apt-get install postgresql postgresql-contrib
```

Once `psql` is installed, you can set up the database tables using the following
command:

```
make setup-db
```

### Adding New Requirements

To introduce new Python requirements, add them to the appropriate `.in` file in the
`requirements` folder and then run:

```
make pip-compile
```

The new requirements will be pinned in the `requirements/*.txt` files. After adding a
new requirement, make sure to install dependencies again with

```
make pip-install
```

### Linting

Linting for the JavaScript UI uses `prettier` and linting for the Python backend uses
`black`. After editing code, you can check to make sure your changes conform to the
project's style standards by running

```
make lint
```

If the linting job fails, you can correct stylistic errors by running

```
make tidy
```

Note, linting runs during the CI/CD build as part of the test job.

### Tests

To run the unit tests for the Python backend, make sure `requirements/test.txt` are
installed and run the following command:

```
make test
```

## Using the Python Package

### Connecting to the database

The Python package includes a utility for connecting to the RDS database. The utility
assumes you have the RDS URI stored as an environmental variable, so you'll want
something similar to the following in `$HOME/.bashrc`:

```bash
export FIDDLER_RDS=<fiddler-rds-uri>
export RDS_USER=<db-username>
```

You should replace `<fiddler-rds-uri>` with the actual URI and `<db-username>` with your Postgre username.
You can get the RDS URI from Matt if you need it.
if you don't have it already. You'll also need to set up a `.pgpass` in your home
directory with the following contents. Run `chmod 0600 ~/.pgpass` to ensure the file has
the correct security permissions, otherwise authentication will fail:

```
<fiddler-rds-uri>:5432:<fiddler-rds-user>:<fiddler-rds-pass>
```

Once you have all that set up, and assuming you have the Python package installed, you
can connect to the database with the following Python code:

```python
from event_explorer.database.connection import connect

connection = connect()
```

Optionally, you can also pass in any keyword argument that is accepted by `psycopg2`.
Keyword arguments take precedence over both environmental variables and defaults. For
example:

```python
import getpass

from event_explorer.database.connection import connect

user = "matt"
password = getpass.getpass() # Masked input for password
host = "super-awesome-rds-uri"

connection = connect(user=user, password=password, host=host)
```

### Using APIs for External Services

API calls in Event Explorer implemented wrappers around the `requests.Session` class
that automatically apply authenticate to the API and apply the base url for the API.
Credentials are read in from the following environmental variables. To use a given API,
you'll need to export these environmental variable prior to running Python.

- `EVENTBRITE_TOKEN`
- `ZOOM_API_KEY`
- `ZOOM_API_SECRET`

Once integrated into the UI, the `ExternalServices` class for APIs will also support an
OAUTH2 workflow. To use a given API, you can use a workflow similar to the following:

```python
import os
from event_explorer.external_services.zoom import Zoom

# Only required if you don't have these set in your environment.
# For security purpose, DO NOT hard code these in a script.
os.environ["ZOOM_API_KEY"] = "my_api_key"
os.environ["ZOOM_API_SECRET"] = "my_api_secret"

zoom = Zoom()
response = zoom.get("/users") # Pulls a list of users for your account
users = response.json()
```

Each external service also has its own events and attendees subclasses. You can
instantiate these classes using a dictionary or an event id. If instantiating from a
dictionary, the input is the event dictionary returned by the API call. The following
code shows how to instantiate the same Zoom event using both options:

```python
from event_explorer.external_services.zoom import ZoomEvent

zoom_event = ZoomEvent.from_dict({
  "uuid": "mlghmfghlBBB",
  "id": 11111,
  "host_id": "abckjdfhsdkjf",
  "topic": "Zoom Meeting",
  "type": 2,
  "start_time": "2019-08-16T02:00:00Z",
  "duration": 30,
  "timezone": "America/Los_Angeles",
  "created_at": "2019-08-16T01:13:12Z",
  "join_url": "https://zoom.us/j/11111"
})

same_zoom_event = ZoomEvent.from_id("mlghmfgh1BBB")
```

After instantiating the event, you can use the class methods to retrieve event metadata.
For example, `zoom_event.get_id()` will return the event id and
`zoom_event.get_attendees()` will return the attendees. If you retrieve the attendees,
the result will be a list of `ZoomAttendee` objects. An equivalent workflow holds for
other external services.

Note, for the above to work, you'll need the appropriate API token environmental
variables set (see above for details).

### Loading events into the database

Each external service has a helper method for loading events retrieved from the API into
the database. For this to work, you'll need a `.pgpass` file setup with your database
credentials, and the database URI set in the `FIDDLER_RDS` environmental variables. You
can load events and attendees into the database using the following workflow:

```python
from event_explorer.external_services.zoom import load_zoom

load_zoom(user_id="jabber@parrots.com", max_events=20)
```

Any database connection args you include will be passed through to the `connect`
function. To run the load process with settings other than the default (or what's stored
in your environment), use the following workflow:

```python
import getpass

from event_explorer.external_services.zoom import load_zoom

user = "matt"
password = getpass.getpass() # Masked input for password

load_zoom(user_id="jabber@parrots.com", max_events=20, user=user, password=password)
```

Each external service has its own load function. Do note, not all load functions have
the same parameters. For example, `load_zoom` can take a user id, but `load_eventbrite`
does not. Run `load_zoom?` from an iPython session or look in the code to see what
options are available.

Note, for the above to work, you'll need the appropriate API token environmental
variables set (see above for details).

### Loading events to CSV files

Alternatively, you can load events to pandas dataframes or CSV usings the Python API or
the CLI. To load events to CSVs, use the following workflow:

```python
from event_explorer.external_services.zoom import load_zoom

events, attendees = load_zoom(user_id="jabber@parrots.com", target="dataframe", max_events=20)
```

In the output, `events` will be a CSV with the summary info for all of the events, and
`attendees` will be a dictionary that contains the events for each individual event.


To write the output to CSV files, use the following CLI command from the terminal:
```
event_explorer events-to-csv --directory <result-directory> \
                             --source <source> \
                             --max-events <max-events>
```

For example, you can do
```
event_explorer events-to-csv --directory /home/matt/data \
                             --source eventbrite \
                             --max-events 50
```

That would write create a CSV file called `/home/matt/data/eventbrite.csv` with the
summary info for the first 50 events. A file with attendee data for each individual
event would appear in `/home/matt/data/eventbrite`.
