import os
import json
import sqlite3
import time
from enum import Enum

global storage
global storage_type

class StorageType(Enum):
    DEV = 1
    RELEASE = 2

def get_db_path(storage_type):
    if storage_type == StorageType.DEV:
        path = ':memory:'
    else:
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, '../minesweeper.sqlite3')
    
    return path

def get_db_connection(connection_string):
    
    conn = sqlite3.connect(connection_string)
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

def get_difficulty_list(connection_string):
    
    conn = get_db_connection(connection_string)

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
    
    conn.close()

    return results
def add_high_score(connection_string, difficulty, name, seconds, date):

    conn = get_db_connection(connection_string)

    sql = '''
    SELECT 
        difficulty_id
        , name
    FROM
        difficulty
    WHERE
        name = ?
    LIMIT 1
    '''
    c = conn.cursor()
    c.execute(sql, (difficulty, )) # trailing comma ensure interpreted as a tuple
    row = c.fetchone()
    difficulty_id = row[0]

    sql = '''
    INSERT INTO high_scores(difficulty_id, name, seconds, date)
    VALUES (?, ?, ?, ?)
    '''
    parameters = (difficulty_id, name, seconds, date.strftime('%Y-%m-%dT%H:%M:%S'))
    c = conn.cursor()
    c.execute(sql, parameters)



def get_high_scores(connection_string, difficulty, max_rows):

    conn = get_db_connection(connection_string)

    sql = '''
    SELECT
        d.name as difficulty
        , hs.name
        , hs.seconds
        , hs.date
    FROM 
        high_scores hs
        INNER JOIN difficulty d ON hs.difficulty_id = d.difficulty_id
    WHERE
        d.name = ?
    ORDER BY
        hs.seconds ASC
    LIMIT ''' + str(max_rows) + ';'
    
    print(sql)
    c = conn.cursor()
    c.execute(sql, (difficulty, ))
    rows = c.fetchall()
    results = []
    for row in rows:
        data = {}
        data['difficulty'] = row[0]
        data['name'] = row[1]
        data['seconds'] = row[2]
        data['date'] = time.strptime(row[3], '%Y-%m-%dT%H:%M:%S')
        results.append(data)

    conn.close()
    
    return results

def load_settings(type):

    global storage
    global storage_type
    storage = {}
    storage_type = type

    connection_string = get_db_path(storage_type)
    difficulty = get_difficulty_list(connection_string)

    path = os.path.dirname(os.path.realpath(__file__))   
    file_path = os.path.join(path, '../settings.json')     
    f = open(file_path, 'rt')
    storage = json.loads(f.read())
    storage['difficulty'] = difficulty
    if not 'default_difficulty' in storage:
        storage['default_difficulty'] = difficulty[0]
    f.close()

def save_settings(type):
    global storage
    global storage_type
    storage_type = type
    save_data = {}
    save_data["high_score_count"] = storage["high_score_count"]
    save_data["default_difficulty"] = storage["default_difficulty"]

    path = os.path.dirname(os.path.realpath(__file__))   
    file_path = os.path.join(path, '../settings.json')     
    f = open(file_path, 'wt')
    f.write(json.dumps(save_data))
    f.close()
