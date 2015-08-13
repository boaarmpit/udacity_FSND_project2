#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament


import psycopg2


def connect():
    """Connect to the PostgreSQL database.
    Returns a database connection and a cursor."""
    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    return db, cursor


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    query = """
    TRUNCATE matches;
    ALTER SEQUENCE matches_match_id_seq RESTART WITH 1;
    """
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database.
    (Also remove all the match records from the database.)"""
    db, c = connect()
    query = """
    TRUNCATE players CASCADE;
    ALTER SEQUENCE players_id_seq RESTART WITH 1;
    """
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    query ="""
    SELECT COUNT (*) FROM players;
    """
    c.execute(query)
    no_of_players = int(c.fetchone()[0])
    db.close()
    return no_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    is be handled by the SQL database schema, not the Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    query = """
    INSERT INTO players (name) VALUES (%s);
    """
    params = (name,)
    c.execute(query, params)
    db.commit()
    db.close()


def playerStandings(return_draws=False):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list is the player in first place,
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
    db, c = connect()
    if not return_draws:
        query = """
        SELECT id, name, wins, games from standings;
        """
    else:
        query = """
        SELECT * FROM standings;
        """
    c.execute(query)
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
    db, c = connect()
    query = """
    INSERT INTO matches (winner_id, loser_id, is_draw)
    VALUES (%s, %s, %s);
    """
    params = (winner, loser, is_draw)
    c.execute(query, params)
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

    db, c = connect()
    query = """
    SELECT * FROM pairings;
    """
    c.execute(query)
    rows = c.fetchall()
    db.commit()
    db.close()
    return rows
