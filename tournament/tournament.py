#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament


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
    """Remove all the player records from the database.
    (Also remove all the match records from the database.)"""
    deleteMatches()
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


def playerStandings(return_draws=False):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Args:
      return_draws: set True to also return number of draws (default = False)

    Returns:
      A list of tuples, each of which contains the following:
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        draws: the number of matches the player has drawn
               (only returned if return_draws = True)
    """
    db = connect()
    c = db.cursor()
    if not return_draws:
        c.execute(
            """
            SELECT id, name, wins, games from standings;
            """
        )
    else:
        c.execute(
            """
            SELECT * FROM standings;
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
        VALUES (0, %s, %s, %s);
        """, (winner, loser, is_draw)
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

    db = connect()
    c = db.cursor()
    c.execute(
        """
        SELECT * FROM pairings;
        """
    )
    rows = c.fetchall()
    db.commit()
    db.close()
    return rows
