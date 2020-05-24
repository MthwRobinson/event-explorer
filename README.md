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

## Adding New Requirements

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

## Linting

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

## Tests

To run the unit tests for the Python backend, make sure `requirements/test.txt` are
installed and run the following command:

```
make test
```
