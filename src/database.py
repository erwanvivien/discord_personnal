import sqlite3
from sqlite3 import Error

import datetime as date

DB_PATH = "db/database.db"


def create() -> None:
    """Will init / start the database, needed at every python start
    """

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


def guild_get_all() -> list:
    """Returns all guilds

    Returns:
        [list] -- Returns a list of all the guilds' id
    """
    sql = "SELECT guilds.id FROM guilds"

    res = exec(sql)
    return res


def guild_exists(guild_id: int) -> list:
    """Checks in database if guild already exists

    Arguments:
        guild_id {int} -- The guild ID

    Returns:
        [list] -- Returns a list with one or zero element
    """

    sql = "SELECT * FROM guilds WHERE guilds.id = ?"
    args = [guild_id]

    res = exec(sql, args)
    return res


def guild_insert(guild_id: int) -> None:
    """Inserts the discord server in question.

    Arguments:
        guild_id {int} -- The guild ID
    """

    sql = "INSERT INTO guilds VALUES (?, ?)"
    args = [guild_id, 0]

    exec(sql, args)


def guild_premium(guild_id: int) -> float:
    """Retuns the premium end's date

    Arguments:
        guild_id {int} -- The guild ID

    Returns:
        [float] -- Returns the time as float
    """

    sql = "SELECT guilds.premium FROM guilds WHERE guilds.id = ?"
    args = [guild_id]

    res = exec(sql, args)[0][0]
    return res


def guild_premium_set(guild_id: int, date: date.datetime) -> None:
    """Sets the premium end's date

    Arguments:
        guild_id {int} -- The guild ID
        date {date.datetime} -- The ending time
    """
    sql = "UPDATE guilds SET premium = ? WHERE guilds.id = ?"
    args = [date.timestamp(), guild_id]

    exec(sql, args)


def guild_premium_add(guild_id: int, days: int) -> None:
    """Adds to the premium end's date a specified number of days

    If premium end's date had expired, starts from current

    Arguments:
        guild_id {int} -- The guild ID
        days {int} -- Number of days to add
    """

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
    """Retuns a list of mappings for specified guild

    Arguments:
        guild_id {int} -- The guild ID

    Returns:
        [list[tuple]] -- contains elements in this order: `name, path, definition`
    """

    sql = "SELECT mappings.name, mappings.path, mappings.definition " + \
        "FROM mappings WHERE mappings.discord_id = ?"
    args = [guild_id]

    res = exec(sql, args)
    return res


def mappings_exists(guild_id: int, name: str) -> list:
    """Retuns a list of zero or one mapping for specified guild

    Arguments:
        guild_id {int} -- The guild ID
        name {str} -- The mapping to search

    Returns:
        [list[tuple]] -- contains elements in this order: `name, path, definition`
    """

    sql = "SELECT mappings.name, mappings.path, mappings.definition " + \
        "FROM mappings WHERE mappings.discord_id = ? AND mappings.name = ?"
    args = [guild_id, name]

    res = exec(sql, args)
    return res


def mappings_set(guild_id: int, name: str, path: str, definition: str = "") -> None:
    """Adds a mapping

    Arguments:
        guild_id {int} -- The guild ID
        name {str} -- The mapping's name
        path {str} -- The mapping's path in our architecture
        definition {str, optionnal} -- The mapping's definition
    """

    sql = "INSERT INTO mappings VALUES (?, ?, ?, ?, ?)"
    args = [None, guild_id, name, path, definition]

    res = exec(sql, args)
    return res


def mappings_def(guild_id: int, name: str, definition: str) -> None:
    """Adds definition to the mapping

    Arguments:
        guild_id {int} -- The guild ID
        name {str} -- The mapping's name
        definition {str} -- The mapping's definition
    """

    sql = "UPDATE mappings SET definition = ? WHERE mappings.discord_id = ? AND mappings.name = ?"
    args = [definition, guild_id, name]

    exec(sql, args)


def mappings_rm(guild_id: int, name: str) -> None:
    """Removes a mappings

    Arguments:
        guild_id {int} -- The guild ID
        name {str} -- The mapping's name
    """

    sql = "DELETE FROM mappings WHERE mappings.discord_id = ? AND mappings.name = ?"
    args = [guild_id, name]

    exec(sql, args)


def exec(sql: str, args: list = None) -> list:
    """Execs ANY sql command

    Arguments:
        sql {str} -- The SQL request
        args {list[Any]} -- The arguments if needed

    Returns:
        [list] -- Might be empty, it returns what the request returned.
    """

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
