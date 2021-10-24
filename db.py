import sqlite3
import time

import config

SCHEMA_FILE = 'schema.sql'
REQ_COMMITS = ['INSERT', 'UPDATE']

# standard functions
def _db_query(sql_query:str, list_data=None):
    con = sqlite3.connect(SCHEMA_FILE)
    cur = con.cursor()
    
    if list_data is not None:
        cur.execute(sql_query, list_data)
    else:
        cur.execute(sql_query)
    
    try:
        if "SELECT" in sql_query:
            response = cur.fetchall()
        elif [req in sql_query for req in REQ_COMMITS]:
            response = con.commit()
    except Exception:
        con.rollback()
    
    con.close()
    return response

# accounts table

def add_user(unique_id:str, email:str, username:str, picture):
    _db_query(
        'INSERT INTO Accounts (UniqueId, Email, Username, LastLogin, Picture) VALUES (?,?,?,?,?)', 
        (unique_id, email, username, int(time.time()), picture)
    )

def update_user_lastlogin(unique_id:str):
    _db_query(
        'UPDATE Accounts SET LastLogin=? WHERE UniqueId=?',
        (int(time.time()), unique_id)
    )

def lookup_user(unique_id:str) -> list:
    response = _db_query(
            'SELECT * FROM Accounts WHERE UniqueId=?', 
            (unique_id,)
        )

    return response

def user_list() -> list:
    response = _db_query('SELECT * FROM Accounts')
    
    return response

# games table

def supported_games() -> list:
    response = _db_query('SELECT * FROM Games')
    
    return response

def lookup_developer_games(developer) -> list:
    response = _db_query(
                    'SELECT * FROM Games WHERE Developer=?', 
                    (developer,)
                )
    return response

def does_game_exist(name: str) -> list:
    response = _db_query(
                    'SELECT * FROM Games WHERE Title=?', 
                    (name,)
                )
    return response

if __name__ == "__main__":
    print(supported_games())