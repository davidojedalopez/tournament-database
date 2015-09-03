--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Delete the database if it was previously created
DROP DATABASE IF EXISTS tournament;
-- Create the database for the tournament
CREATE DATABASE tournament;
-- Connect to the tournament database
\c tournament;

-- Create the players table with a serial ID and a name
CREATE TABLE players (id serial PRIMARY KEY,
						name text);

-- Create the matches table with a serial ID, three foreign keys representing the players ID's
-- and the winner ID, and a draw column with 1 indicating a draw
CREATE TABLE matches (id serial PRIMARY KEY,						
						player1_id integer references players(id),
						player2_id integer references players(id),
						winner_id integer NULL references players(id),
						draw integer NULL);


