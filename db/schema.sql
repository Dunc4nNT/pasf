CREATE SCHEMA IF NOT EXISTS api AUTHORIZATION pasf;

SET search_path TO api;

-- DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
	id uuid PRIMARY KEY,
	email varchar(255) UNIQUE NOT NULL,
	password varchar(255) NOT NULL,
	username varchar(32) NOT NULL,
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
