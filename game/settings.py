import os
import json
import sqlite3
import time
from enum import Enum

class storage(Enum):
    DEV = 1
    RELEASE = 2

def get_db_path(type):
    if type == storage.DEV:
        path = ':memory:'
    else:
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, '../minesweeper.sqlite3')
    
    return path

def get_db_connection(type):
    
    conn = sqlite3.connect(get_db_path(type))
    c = conn.cursor()
    sql = '''
    SELECT 
        COUNT(name) 
    FROM 
        sqlite_master 
    WHERE 
        type=\'table\' 
        AND name=?;
    '''
    c.execute(sql, ['difficulty'])    

    if c.fetchone()[0] == 0:
        # We do not have a difficulty table, please generate it.
        sql = '''
        CREATE TABLE difficulty(
            difficulty_id INTEGER PRIMARY KEY
            , name TEXT NOT NULL
            , width INTEGER
            , height INTEGER
            , num_bombs INTEGER);
        '''
        c.execute(sql)
        conn.commit()

        # now insert the default difficulty information.
        sql = 'INSERT INTO difficulty(name, width, height, num_bombs) VALUES(?,?,?,?)'
        c.executemany(sql, [
            ('Easy', 10, 10, 15,)
            , ('Medium', 20, 30, 100,)
            , ('Hard', 35, 35, 250,)])
        conn.commit()
    
    sql = '''
    SELECT 
        COUNT(name) 
    FROM 
        sqlite_master 
    WHERE 
        type=\'table\' 
        AND name=?;
    '''
    c.execute(sql, ['high_scores'])
    if c.fetchone()[0] == 0:
        # We do not have a high_scores table, please generate it.
        sql = '''
        CREATE TABLE high_scores(
            high_scores_id INTEGER PRIMARY KEY
            , difficulty_id INTEGER
            , name TEXT NOT NULL
            , seconds INTEGER
            , date TEXT
            , FOREIGN KEY(difficulty_id) REFERENCES difficulty(difficulty_id)
        );
        '''
        c.execute(sql)
        conn.commit()

        # Empty high scores table on initialize is just fine.

    return conn

def get_difficulty_list(conn):
    sql = '''
    SELECT
        difficulty_id
        , name
        , width
        , height
        , num_bombs
    FROM
        difficulty
    ORDER BY
        difficulty_id;
    '''
    c = conn.cursor()
    c.execute(sql)
    results = []
    for row in c:
        data = {}
        data['difficulty_id'] = row[0]
        data['name'] = row[1]
        data['width'] = row[2]
        data['height'] = row[3]
        data['bombs'] = row[4]
        results.append(data)
    
    return results
    
def get_high_scores(conn, difficulty, max_rows):
    sql = '''
    SELECT
        TOP ''' + str(max_rows) + '''
        d.name as difficulty
        , hs.name
        , hs.seconds
        , hs.date
    FROM 
        high_scores hs
        INNER JOIN difficulty d ON hs.difficulty_id = d.difficulty_id
    WHERE
        d.name = ?;
    ORDER BY
        hs.seconds ASC
    '''
    c = conn.cursor()
    c.execute(sql)
    results = []
    for row in c:
        data = {}
        data['difficulty'] = row[0]
        data['name'] = row[1]
        data['seconds'] = row[2]
        data['date'] = time.strptime(row[3], '%Y-%m-%dT%H:%M:%S')
        results.append(data)
    
    return results

conn = get_db_connection(storage.RELEASE)
difficulty = get_difficulty_list(conn)
conn.close()
print(difficulty)

path = os.path.dirname(os.path.realpath(__file__))   
file_path = os.path.join(path, '../settings.json')     
f = open(file_path, 'rt')
settings = json.loads(f.read())
f.close()
