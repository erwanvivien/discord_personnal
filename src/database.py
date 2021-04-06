import sqlite3
from sqlite3 import Error

DB_PATH = "database.db"


def create():
    # Contains
    sql_create_user = """CREATE TABLE IF NOT EXISTS guild 
    (
        id integer PRIMARY KEY,
        premium INTEGER
    ); """
    exec(sql_create_user)


def exec(sql, args=None):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if args:
        res = cur.execute(sql, args).fetchall()
    else:
        res = cur.execute(sql).fetchall()

    if conn:
        conn.commit()
        conn.close()

    return res
