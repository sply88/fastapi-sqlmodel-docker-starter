# FastAPI with SQLModel and Docker Compose

Example project to illustrate usage of [FastAPI](https://fastapi.tiangolo.com/) 
and [SQLModel](https://sqlmodel.tiangolo.com/) in conjunction with 
[Docker Compose](https://docs.docker.com/compose/).

## Overview

The example application is a simple REST API that allows clients to `GET` `POST` 
`PATCH` and `DELETE` "messages". These are composed of the actual message text 
and a label that is either "unknown", "funny" or "informative". The messages are 
stored in a [PostgreSQL](https://www.postgresql.org/) database.

On the one hand, I hope the examples are helpful and informative for people
studying the above frameworks and technologies.  
On the other hand, this project should provide a skeleton, that can be used as
a starter for (small) real-world projects. 

Topics addressed are
- Example application using FastAPI and SQLModel
- Testing the application
- Assembling multiple services with docker compose
- Configuring these services using environment variables
- Suggested conventions for handling this configuration in the application code to
facilitate code readability and testability


## Development

**Prerequisites**:
The following section assumes that Docker and Docker Compose are installed.
See [here](https://docs.docker.com/engine/install/) for directions.

### Quick Start

Install development requirements via
```
pip install -r requirements.txt
```

and start the development stack via

```
docker compose -f docker-compose.yml -f dev.yml --env-file dev.env up -d
```

Navigate to http://127.0.0.1:8000/docs to explore the interactive API documentation.

Run tests with
```
pytest ./api
```
and code style checks with
```
flake8 ./api
```


Stop the development stack with
```
docker compose -f docker-compose.yml -f dev.yml --env-file dev.env down
```

### Details

#### Docker Compose

There is one directory per service defined in [docker-compose.yml](docker-compose.yml).
The directory [./api](./api) contains all files for the FastAPI application,
especially the source code. The directory [./postgres](./postgres) contains files 
only relevant to the postgresql database, e.g. the script for user initialization.

As illustrated in the previous Quick Start section, any Docker Compose `COMMAND`
(`up`, `build` etc.) is used like this during development:
```
docker compose -f docker-compose.yml -f dev.yml --env-file dev.env COMMAND
```

[docker-compose.yml](docker-compose.yml) contains the base configuration of the
services that is complemented with the configuration in [dev.yml](./dev.yml).
The latter configuration file adjust the basic configuration for development
convenience by:
- Mounting the API source code and running uvicorn with the `--reload` flag.
This way, the effects of code changes are applied immediately and there is no 
need to rebuild the image to test each change during development.
- The postgres service is exposed to the host, so one can easily connect
to the development database with tools such as [pgadmin](https://www.pgadmin.org/)
for debugging, etc.
- An additional database service `postgres-test` is included that will be used
during tests (note the pytest fixture `db_uri` in 
[./api/tests/conftest.py](./api/tests/conftest.py)). The rationale for using 
an extra DB is, that tests expect an empty DB, that might be seeded with specific
data for a given test case.

The configuration of the development environment is completed by [dev.env](dev.env),
which is the only env file kept in version control and should never be used in a
production setting.  
The Docker Compose files (docker-compose.yml, dev.yml) show how the values set 
in the `--env-file` are passed to the service containers as environment variables.

For more information on combining multiple compose files and setting environment 
variables refer to the official docker documentation 
[here](https://docs.docker.com/compose/extends/#multiple-compose-files) and 
[here](https://docs.docker.com/compose/environment-variables/),
respectivey.

#### The FastAPI application

The application source code is located in [api/api](./api/api). The subpackage
`data_management` contains data model definitions as well as CRUD and database
connection utils. The subpackage `routers` contains the actual definition of
the applications HTTP interface.  
The model naming scheme in 
[api/api/data_management/models.py](api/api/data_management/models.py) and usage 
of 
[fastapi's dependency injection mechanism](https://fastapi.tiangolo.com/tutorial/dependencies/)
for database sessions in [api/api/routers/messages.py](api/api/routers/messages.py) 
was inspired by 
[this excellent sqlmodel tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/).

The main entrypoint of the application is [api.main](./api/api/main.py). It 
assembles and sets up the different lower level components.

Finally, [`api.settings.Settings`](./api/api/settings.py) is responsible for
reading any environment configuration using 
[Pydantic Settings Management](https://docs.pydantic.dev/latest/usage/pydantic_settings/).
Note that the attribute names of the `Settings` class are just lower case versions
of the variable names passed to the API container in [docker-compose.yml](docker-compose.yml),
and hence pydantic will load those values automatically from the environment variables.

The application uses the following convention for configuration handling:
`api.settings.Settings` is the only place that reads variables from the environment.
The main entrypoint `api.main` resolves this configuration and passes the required
dependencies to lower level components, e.g. `from .settings import Settings` happens 
only in `api.main` and the `db_uri` is passed down to the class responsible for
establishing database connections.

Separating configuration from the application code in this way, facilitates
testability, and specifically the usage of tools such as 
[pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html)
and [fastapi dependency_overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
It should also improve readability, as developers can easily comprehend how
certain environment settings affect the application without searching the code
base for config classes or `os.getenv` calls.

## Deployment

**WIP**


