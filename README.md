# Fiddler Analytics Event Explorer

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
