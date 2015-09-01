#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import time

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    database_connection = connect()
    cursor = database_connection.cursor()
    query = "DELETE FROM matches"
    cursor.execute(query)
    database_connection.commit()
    database_connection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    database_connection = connect()
    cursor = database_connection.cursor()
    query = "DELETE FROM players"
    cursor.execute(query)
    database_connection.commit()
    database_connection.close()

def countPlayers():
    """Returns the number of players currently registered."""
    database_connection = connect()
    cursor = database_connection.cursor()
    query = "SELECT count(*) FROM players"
    cursor.execute(query)
    player_count = cursor.fetchone()
    database_connection.close()
    return player_count[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    database_connection = connect()
    cursor = database_connection.cursor()
    query = "INSERT INTO players (name) VALUES ((%s))"
    cursor.execute(query, (name,))
    database_connection.commit()
    database_connection.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    database_connection = connect()
    cursor = database_connection.cursor()
    query = """
        SELECT
            p.id,
            p.name,
            sum(case when p.id = m.winner_id then 1 else 0 end) wins,
            count(m.id) matches_played            
        FROM
            players p
        LEFT OUTER JOIN 
            matches m 
        ON
            p.id = m.player1_id
        OR
            p.id = m.player2_id
        GROUP BY
            p.id,
            p.name
        ORDER BY 
            wins
        DESC
    """
    cursor.execute(query)
    player_standings = []
    for row in cursor.fetchall():
        player_standings.append(row)
    database_connection.close()
    return player_standings

def checkSkippedRound():
    database_connection = connect()
    cursor = database_connection.cursor()
    query = "SELECT id FROM players ORDER BY id LIMIT 1"
    cursor.execute(query)
    player_id = cursor.fetchone()[0]     
    query = "INSERT INTO matches (winner_id) VALUES ({0})".format(player_id)
    cursor.execute(query)
    database_connection.commit()        
    database_connection.close()
    return player_id

def reportMatch(winner, loser, draw=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    database_connection = connect()
    cursor = database_connection.cursor()
    query = "INSERT INTO matches (player1_id, player2_id, winner_id) VALUES ({0}, {1}, {2})".format(winner, loser, winner)        
    cursor.execute(query)
    database_connection.commit()
    database_connection.close()
 
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
    pairs_list = []
    temp_list = []
    player_standings_list = playerStandings()
    for i in range(0, len(player_standings_list)):
        temp_list.append(player_standings_list[i][:2])
        if(i%2 != 0):            
            pairs_list.append(temp_list[0]+temp_list[1])
            temp_list = []
    return pairs_list


