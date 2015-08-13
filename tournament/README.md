## Synopsis

This is a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament uses the Swiss system for pairing up players in each round; players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

It defines the database schema (SQL table definitions), and includes the python code to use it.

This is Project 2 of the [Udacity Full Stack Nano Degree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Motivation

To meet the requirements of the Udacity Full Stack Nano Degree and learn postgreSQL.

## Installation
This module was designed and tested with python 2.7.6 and postgreSQL 9.3.9.  
It requires the following library aside from the Python Standard Libraries:  
*psycopg2*

## Usage

Setup:
<ol><li> Setup the database, table and view definitions with `\i tournament.sql` in psql.  
*Warning, this will delete any existing database named "tournament".* </li>
<li> Use `python tournament_test.py` to test the setup. </li></ol>

The available functions in *tournament.py* are listed below.  

###registerPlayer(name)

Adds a player to the tournament by putting an entry in the database. The database assigns an ID number to the player. Different players may have the same names but will receive different ID numbers.

###countPlayers()

Returns the number of currently registered players.

###deletePlayers()

Deletes all the player records from the database.  (Also deletes all match records from the database.)

###reportMatch(winner, loser, is_draw=False):

Stores the outcome of a single match between two players in the database.  
Setting is_draw to True specifies a draw.

###deleteMatches()

Deletes all the match records from the database.

###playerStandings(return_draws=False)

Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.  
Players with an equal number of wins are sorted by number of draws.  
Setting *return_draws=True* returns (id, name, wins, matches, draws).

###swissPairings()

Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function returns four pairings.  Currently the lowest ranked player will be ignored if there are an odd number of players.

## References
This includes example code from the [Udacity Full Stack Nano Degree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) *Intro to Relational Databases* course.