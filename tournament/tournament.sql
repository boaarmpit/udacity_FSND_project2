-- Table definitions for the tournament project.

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