-- Variables for script

-- Application user (non-admin user)
\set db_user 'musketeers'

-- Database name
\set database_name 'musketeers'

-- Schema name (in database
\set db_schema 'musketeers'

DROP DATABASE IF EXISTS :database_name;
DROP ROLE IF EXISTS :db_user;

CREATE ROLE :db_user
    WITH
    LOGIN
    ENCRYPTED PASSWORD :'db_user';

CREATE DATABASE :database_name
    WITH
    OWNER = :db_user;
