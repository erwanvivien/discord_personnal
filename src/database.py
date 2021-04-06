import sqlite3
from sqlite3 import Error

import datetime as date

DB_PATH = "db/database.db"


def create() -> None:
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


def guild_exists(guild_id: int) -> list:
    sql = "SELECT * FROM guilds WHERE guilds.id = ?"
    args = [guild_id]

    res = exec(sql, args)
    return res


def guild_insert(guild_id: int) -> None:
    # Inserts the discord server in question.
    sql = "INSERT INTO guilds VALUES (?, ?)"
    args = [guild_id, 0]

    exec(sql, args)


def guild_premium(guild_id: int) -> float:
    sql = "SELECT guilds.premium FROM guilds WHERE guilds.id = ? AND guilds.premium <> 0"
    args = [guild_id]

    res = exec(sql, args)[0][0]
    return res


def guild_premium_set(guild_id: int, date: date.datetime) -> None:
    sql = "UPDATE guilds SET premium = ? WHERE guilds.id = ?"
    args = [date.timestamp(), guild_id]

    exec(sql, args)


def guild_premium_add(guild_id: int, days: int) -> None:
    sql = "SELECT guilds.premium FROM guilds WHERE guilds.id = ?"
    args = [guild_id]

    current = exec(sql, args)[0][0]
    if current < date.datetime.now().timestamp():
        current = date.datetime.now().timestamp()

    new_date = current + days * 86_400  # 24 * 60 * 60

    sql = "UPDATE guilds SET premium = ? WHERE guilds.id = ?"
    args = [new_date, guild_id]

    exec(sql, args)


def mappings_get(guild_id: int) -> list:
    sql = "SELECT mappings.name, mappings.path, mappings.definition " + \
        "FROM mappings WHERE mappings.discord_id = ?"
    args = [guild_id]

    res = exec(sql, args)
    return res


def mappings_set(guild_id: int, name: str, path: str, definition: str = "") -> None:
    sql = "INSERT INTO mappings VALUES (?, ?, ?, ?, ?)"
    args = [None, guild_id, name, path, definition]

    res = exec(sql, args)
    return res


def mappings_def(guild_id: int, name: str, definition: str) -> None:
    sql = "UPDATE mappings SET definition = ? WHERE mappings.discord_id = ? AND mappings.name = ?"
    args = [definition, guild_id, name]

    exec(sql, args)


def mappings_rm(guild_id: int, name: str) -> None:
    sql = "DELETE FROM mappings WHERE mappings.discord_id = ? AND mappings.name = ?"
    args = [guild_id, name]

    exec(sql, args)


def exec(sql: str, args: list = None) -> list:
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
