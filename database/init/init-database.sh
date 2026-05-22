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
           VALUES ('testuser3', 'test3@suer.de', 'chatter', '62e9ae03a4410b4a3d1a47a46757c2977fdd5be664d683cc256a06a02d688a2a');
    INSERT INTO chatuser (username, email, role, hashed_password)
           VALUES ('testuser4', 'test4@suer.de', 'chatter', 'b68ae55024cf27f2a02ab53c14dd19219b453e7e015164c6dcfca294dc0c5512');
EOSQL

