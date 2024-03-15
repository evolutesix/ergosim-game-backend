# Ergosim API

## Documentation

- [Poetry](https://python-poetry.org/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Pydantic](https://docs.pydantic.dev/latest/)

## Useful commands

### Serve API locally

```sh
.venv/bin/flask --app 'ergosim.backend.api.main' --debug run
```

### Testing

Testing is performed using `pytest` with the tests interspersed with the rest of the code files. This organization 
makes sense in a project intended to follow domain-driven design principles.

```shell
pytest .
pytest domain
pytest api
```

#### Hexagonal Architecture

External dependencies are abstracted away using adapters. An example of this is the `UserAccountCollectionInterface` 
implemented with both an in-memory and a SQLAlchemy adapter. This allows for the domain to be tested in isolation from
external dependencies.

### Typechecking (MyPy)

```shell
mypy .
mypy domain
mypy api
```