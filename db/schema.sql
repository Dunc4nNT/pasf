-- CREATE SCHEMA IF NOT EXISTS api AUTHORIZATION pasf;

-- SET search_path TO api;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pasf;

-- DROP TABLE IF EXISTS users CASCADE;

-- CREATE TABLE IF NOT EXISTS users (
-- 	id uuid PRIMARY KEY,
-- 	username varchar(32) UNIQUE NOT NULL,
-- 	displayname varchar(32) NOT NULL,
-- 	password varchar(255) NOT NULL,
-- 	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
-- );

-- DROP TABLE IF EXISTS decks CASCADE;

CREATE TABLE IF NOT EXISTS decks (
	id uuid PRIMARY KEY,
-- 	owner_id uuid NOT NULL
-- 		REFERENCES users (id)
-- 		ON UPDATE CASCADE
-- 		ON DELETE CASCADE,
	name varchar(32) NOT NULL,
-- 	CONSTRAINT user_deck_unique
-- 		UNIQUE (owner_id, name)
	CONSTRAINT deck_unique
		UNIQUE (name)
);

-- DROP TABLE IF EXISTS cards CASCADE;

CREATE TABLE IF NOT EXISTS cards (
	id uuid PRIMARY KEY,
	name varchar(32),
	front_content varchar(2048) NOT NULL,
	back_content varchar(2048) NOT NULL
);

-- DROP TABLE IF EXISTS deck_cards;

CREATE TABLE IF NOT EXISTS deck_cards (
	id uuid PRIMARY KEY,
	deck_id uuid NOT NULL
		REFERENCES decks (id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	card_id uuid NOT NULL
		REFERENCES cards (id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT deck_card_unique
		UNIQUE (deck_id, card_id)
);

-- DROP TABLE IF EXISTS tags CASCADE;

CREATE TABLE IF NOT EXISTS tags (
	id uuid PRIMARY KEY,
	name varchar(32),
	CONSTRAINT name_unique
		UNIQUE (name)
);

-- DROP TABLE IF EXISTS card_tags;

CREATE TABLE IF NOT EXISTS card_tags(
	id uuid PRIMARY KEY,
	card_id uuid NOT NULL
		REFERENCES cards (id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	tag_id uuid NOT NULL
		REFERENCES tags (id)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);
