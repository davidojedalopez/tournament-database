#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import time
import contextlib

@contextlib.contextmanager
def with_cursor():
    """Creates a connection to the database and a cursor with that connection. 
    It also handles the commit and close operations on the database.
    """
    connection = connect()
    cursor = connection.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches"
    with with_cursor() as cursor:        
        cursor.execute(query)

def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players"
    with with_cursor() as cursor:        
        cursor.execute(query)

def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT count(*) FROM players"
    with with_cursor() as cursor:
        cursor.execute(query)
        player_count = cursor.fetchone()    
    return player_count[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES ((%s))"
    with with_cursor() as cursor:
        cursor.execute(query, (name,))

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
    with with_cursor() as cursor:
        cursor.execute(query)
        player_standings = []
        for row in cursor.fetchall():
            player_standings.append(row)
    return player_standings

def checkSkippedRound():
    """Gives a skipped round to the first registered player only if there are
    an odd number of players registered.
    """
    with with_cursor() as cursor:
        query = "SELECT id FROM players ORDER BY id LIMIT 1"
        cursor.execute(query)
        player_id = cursor.fetchone()[0]     
        query = "INSERT INTO matches (winner_id) VALUES (%s)"
        cursor.execute(query, (player_id,))
    return player_id

def reportMatch(winner, loser, draw=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "INSERT INTO matches (player1_id, player2_id, winner_id) VALUES (%s, %s, %s)"
    with with_cursor() as cursor:     
        cursor.execute(query, (winner, loser, winner,))
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Each player appears exactly once in the pairings. Each player is pairedwith another player with an equal or nearly-equal win record, that is, a player adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs_list = []
    temp_list = []
    # Create a list of the standing players
    player_standings_list = playerStandings()
    # For every player staning in the list
    for i in range(0, len(player_standings_list)):
        # Append to the temporal list only the first two fields,
        # which are the id and name of the player
        temp_list.append(player_standings_list[i][:2])
        # If the temporal list already has two players,
        # append these players to the pairs list and clear
        # the temporal list
        if(i%2 != 0):            
            pairs_list.append(temp_list[0]+temp_list[1])
            temp_list = []
    return pairs_list


