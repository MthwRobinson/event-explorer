# Fiddler Analytics Event Explorer
[![coverage report](https://gitlab.com/fiddler-analytics/event-explorer/badges/master/coverage.svg)](https://gitlab.com/fiddler-analytics/event-explorer/commits/master)


## Getting started

To install the UI, run the following from the root directory of the project:

```
make install-ui
```

After installing the UI dependency, you can run the UI in development mode using the
following command:

```
make start-ui
```

To install the Python backend, run the following command:

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
```

You should replace `<fiddler-rds-uri>` with the actual URI, which you can get by asking Matt
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
