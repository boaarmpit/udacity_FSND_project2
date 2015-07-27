#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute(
        """
        DELETE FROM matches;
        ALTER SEQUENCE matches_match_id_seq RESTART WITH 1;
        """
    )
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute(
        """
        DELETE FROM players;
        ALTER SEQUENCE players_id_seq RESTART WITH 1;
        """
    )
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute(
        "SELECT COUNT (*) FROM players;"
    )
    no_of_players = int(c.fetchall()[0][0])
    db.close()
    return no_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute(
        """
        INSERT INTO players (name) VALUES (%s);
        """, (name,)
    )
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute(
        """
SELECT matches_players.id,
       matches_players.name,
       COUNT( matches_players.id = matches_players.winner_id
             AND matches_players.is_draw = FALSE
             OR NULL) AS wins,
       --COUNT(matches_players.is_draw = TRUE
       --      OR NULL) AS draws,
       COUNT(matches_players.match_id) AS games
FROM matches_players
GROUP BY matches_players.id,
         matches_players.name
ORDER BY wins DESC;
--,        draws DESC;
        """
    )
    rows = c.fetchall()
    db.commit()
    db.close()

    return rows


def reportMatch(winner, loser, is_draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute(
        """
        INSERT INTO matches (tournament_id, winner_id, loser_id, is_draw)
        VALUES (0,'{0}','{1}',{2});
        """.format(winner, loser, is_draw)
    )
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    parings = []
    for i in range(len(standings) / 2):
        player1 = standings[2 * i]
        player2 = standings[2 * i + 1]
        parings.append([player1[0], player1[1], player2[0], player2[1]])

    return parings


deleteMatches()
deletePlayers()
registerPlayer('Tom')
registerPlayer('Dick')
registerPlayer('Harry')
registerPlayer('Bob')
reportMatch(1, 2)
reportMatch(3, 4)
reportMatch(2, 3, False)
reportMatch(3, 1, True)

playerStandings()
