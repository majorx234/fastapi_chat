#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';
    CREATE DATABASE $DATABASE_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $DATABASE_USER;
    \c $DATABASE_NAME $POSTGRES_USER
    GRANT ALL ON SCHEMA public TO $DATABASE_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$DATABASE_USER" --dbname "$DATABASE_NAME" <<-EOSQL
    CREATE TABLE chatuser
           (id SERIAL PRIMARY KEY,
            username varchar(255),
            email varchar(255) UNIQUE,
            role varchar(20) NOT NULL,
            hashed_password varchar(255) NOT NULL);
    INSERT INTO chatuser (username, email, role, hashed_password)
           VALUES ('testuser1', 'test1@suer.de', 'chatter', 'ACDC');
    INSERT INTO chatuser (username, email, role, hashed_password)
           VALUES ('testuser2', 'test2@suer.de', 'chatter', '1337');
    INSERT INTO chatuser (username, email, role, hashed_password)
           VALUES ('testuser3', 'test3@suer.de', 'chatter', '8b9e5afb166d410f5b7c30ce7d7f9a205e2132dd696ec57ad746feabb4d60cdc');
EOSQL

