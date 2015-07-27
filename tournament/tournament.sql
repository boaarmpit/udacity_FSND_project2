-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE players (
    id serial       primary key,
    name            text
    );

CREATE TABLE matches (
    match_id serial primary key,
    tournament_id   integer,
    player1_id      integer references players(id),
    player2_id      integer references players(id),
    result          integer
    );

CREATE VIEW matches_players AS
    SELECT *
    FROM matches
    RIGHT JOIN players ON players.id = matches.winner_id
    OR players.id = matches.loser_id;