import sqlite3
from sqlite3 import Error

DB_PATH = "db/database.db"


def create():
    # Contains a discord guild id
    # and the premium remaining duration or 0 if not
    sql_create_user = """CREATE TABLE IF NOT EXISTS guilds
    (
        id integer PRIMARY KEY,
        premium REAL
    ); """
    exec(sql_create_user)

    # Contains the mapping ID, pretty useless
    # Contains the mapping name
    # Contains the mapping path
    # Contains the mapping definition
    sql_create_mappings = """CREATE TABLE IF NOT EXISTS mappings
    (
        id integer PRIMARY KEY,
        discord_id integer,
        name TEXT,
        path TEXT,
        definition TEXT
    ); """
    exec(sql_create_mappings)


def guild_exists(guild_id):
    sql = "SELECT * FROM guilds WHERE guilds.id = ?"
    args = [guild_id]

    res = exec(sql, args)
    return res


def guild_insert(guild_id):
    # Inserts the discord server in question.
    sql = "INSERT INTO guilds VALUES (?, ?)"
    args = [guild_id, 0]

    exec(sql, args)


def exec(sql, args=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if args:
        res = cur.execute(sql, args).fetchall()
    else:
        res = cur.execute(sql).fetchall()

    if conn:
        conn.commit()
        conn.close()

    return res
