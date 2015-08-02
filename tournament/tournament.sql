-- Table definitions for the tournament project:

CREATE TABLE players (
    id serial       primary key,
    name            text
    );

CREATE TABLE matches (
    match_id serial primary key,
    winner_id       integer references players(id),
    loser_id        integer references players(id),
    is_draw         boolean
    );

-- Create view for matches combined with winning and losing players (to be able to query their names directly)
CREATE VIEW matches_players AS
    SELECT *
    FROM matches
    RIGHT JOIN players ON players.id = matches.winner_id
    OR players.id = matches.loser_id;

-- Create view to get standings of all players based on their wins and draws
-- Has columns id, name, wins, games, draws
CREATE VIEW standings AS
    SELECT matches_players.id,
       matches_players.name,
       COUNT(matches_players.id = matches_players.winner_id
             AND matches_players.is_draw = FALSE OR NULL) AS wins,
       COUNT(matches_players.match_id) AS games,
       COUNT(matches_players.is_draw = TRUE OR NULL) AS draws
    FROM matches_players
    GROUP BY matches_players.id,
             matches_players.name
    ORDER BY wins DESC, draws DESC;

-- Create view to pair off players based on their standings (above)
-- Has columns id1, name1, id2, name2
-- Does not return final player if there is an odd number of players
CREATE VIEW pairings AS
    SELECT player1.id AS id1,
           player1.name AS name1,
           player2.id AS id2,
           player2.name AS name2
    FROM
      (SELECT t.*,
              row_number() over ()
       FROM
         (SELECT id,
                 name,
                 row_number() over () AS rnum
          FROM standings) t
       WHERE t.rnum%2=1) player1 -- Odd ranked players
    JOIN
      (SELECT t.*,
              row_number() over ()
       FROM
         (SELECT id,
                 name,
                 row_number() over () AS rnum
          FROM standings) t
       WHERE t.rnum%2=0) player2 -- Even ranked players
       ON player1.row_number=player2.row_number;