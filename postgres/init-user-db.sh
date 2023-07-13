#!/bin/bash
set -e

# A dedicated database for the project is created as well as a non-super user for
# the API service with all privileges to work with this db.
# (Based on https://github.com/docker-library/docs/blob/master/postgres/README.md#initialization-scripts)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER $POSTGRES_API_USER WITH PASSWORD '$POSTGRES_API_PASSWORD';
	CREATE DATABASE $POSTGRES_API_DB;
	GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_API_DB TO $POSTGRES_API_USER;
EOSQL

# Since PostgreSQL 15, we need to explicitly grant public schema privileges
# for the API user to allow table creation
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_API_DB" <<-EOSQL
	GRANT ALL ON SCHEMA public TO $POSTGRES_API_USER;
EOSQL