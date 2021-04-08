import discord
import os

import requests
import datetime as date

import discord_utils as disc
import database as db
import utils


async def map(self, message, args):
    """Maps a command, it saves the mapping in the database and the file

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """
    guild_id = message.guild.id
    if not args:
        return await disc.error_message(message, title="Error", desc="No arguments were found")

    if_force = "--force" in args
    if if_force:
        args.remove("--force")

    nb_mappings = len(db.mappings_get(guild_id))
    if nb_mappings >= 5 and db.guild_premium(guild_id) <= date.datetime.now().timestamp():
        return await disc.error_message(message, title="Too many mappings", desc="It seems that your premium subscription has expired\n" +
                                        "Please visit ... if you want to have unlimited mappings")

    bind_to = utils.sanitize(args[0])
    msg = await disc.send_message(message, title="Starting to download", desc="")
    folder = f"assets/{guild_id}"
    if not os.path.exists(folder):  # Creates the dir for the said guild
        os.mkdir(folder)

    if message.attachments:
        # attach_id = message.attachments[0].id # Unsued ID
        attach_name = message.attachments[0].filename
        attach_url = message.attachments[0].url

        extension = attach_name.split('.')[-1]
        response = requests.get(attach_url)

        content = response.content
    else:
        if len(args) <= 1:
            return await disc.edit_message(msg, title="Error", desc="No text nor attachments were found")
        extension = "txt"
        content = str.encode(" ".join(args[1:]))

    filename = f"{folder}/{bind_to}.{extension}"

    file = open(filename, "wb")
    file.write(content)
    file.close()

    db.mappings_set(guild_id, bind_to, filename)
    await disc.edit_message(msg, title="Success !", desc=f"A new mapping has been bound to {bind_to}.{extension}")


async def unmap(self, message, args):
    """Unmaps a command, it removes the file and the mapping in the database

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """
    guild_id = message.guild.id
    if not args:
        return await disc.error_message(message, title="Error", desc="No arguments were found")

    name = utils.sanitize(args[0])
    res = db.mappings_exists(guild_id, name)
    if not res:
        return await disc.send_message(message, title="Error", desc=f"{name} was not a valid mapping")

    db.mappings_rm(guild_id, name)
    await disc.send_message(message, title="Success !", desc=f"You have successfully unmapped {name}")


async def mappings(self, message, args):
    """Displays all the mappings in discord

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """
    guild_id = message.guild.id
    mappings = db.mappings_get(guild_id)
    mappings_text = "\n".join(
        [f"`{e[0]}`" + (f": {e[2]}" if e[2] else "") for e in mappings])

    if not mappings_text:
        mappings_text = "You don't have any mappings for now.\n" +\
            "See `!!help` or `!!map` to add some"

    await disc.send_message(message, title="Your mappings", desc=mappings_text)


async def define(self, message, args):
    """Sets the description to a mapping

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """
    guild_id = message.guild.id
    if not args:
        return await disc.error_message(message, title="Error", desc="No arguments were found")
    if len(args) <= 1:
        return await disc.error_message(message, title="Error", desc="No definition was given")

    name = utils.sanitize(args[0])
    res = db.mappings_exists(guild_id, name)
    if not res:
        return await disc.send_message(message, title="Error", desc=f"{name} was not a valid mapping")

    definition = " ".join(args[1:])

    db.mappings_def(guild_id, name, definition)
    await disc.send_message(message, title="Definition set", desc=f"The mapping {name} has been defined to `{definition}`")


async def help(self, message, args):
    """Displays help message

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """
    await message.channel.send(embed=disc.HELP_EMBED)


async def send(self, message, args):
    """Sends the image / text to discord

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """

    guild_id = message.guild.id
    if not args:
        return

    send = utils.sanitize(args[0])
    res = db.mappings_exists(guild_id, send)
    if not res:
        return

    path = res[0][1]
    if path.split(".")[-1] == "txt":
        await message.channel.send(utils.get_content(path))
    else:
        await disc.send_file(message, path)


async def upgrade(self, message, args):
    """ADMIN COMMAND: Upgrades manually a discord for X more months

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """

    if not args or len(args) < 2:
        return await disc.error_message(message, title="Error", desc="Usage: `GUILD_ID NB_DAYS`")

    if not args[0].isnumeric() or not args[1].isnumeric():
        return await disc.error_message(message, title="Error", desc="Usage: `GUILD_ID NB_DAYS`")

    guild_id = int(args[0])
    day_nb = int(args[1])
    if not db.guild_exists(guild_id):
        return await disc.error_message(message, title="Error", desc="Guild does not exist")

    db.guild_premium_add(guild_id, 31 * day_nb)
    await disc.send_message(message, title="Success", desc=f"Guild {guild_id} has recieved {day_nb} day" + "s" if day_nb > 1 else "" + " !")


async def upgradeall(self, message, args):
    """ADMIN COMMAND: Upgrades manually every discords for X days

    Arguments:
        self {discordClient} -- Needed
        message {discordMessage} -- The actual message that invoked this command
        args {list[str]} -- Everything that is after the command

    Returns:
        None
    """

    if not args or len(args) < 1 or not args[0].isnumeric():
        return await disc.error_message(message, title="Error", desc="Usage: `NB_DAYS`")

    day_nb = int(args[0])

    guilds = db.guild_get_all()
    guilds = [g[0] for g in guilds]
    for g in guilds:
        db.guild_premium_add(g, day_nb)

    await disc.send_message(message, title="Success", desc=f"{len(guilds)} guild" + "s" if len(guilds) > 1 else "" + f" have recieved {day_nb} day" + "s" if day_nb > 1 else "" + " !")


CMDS = {
    "!!map": map,
    "!!unmap": unmap,
    "!!mappings": mappings,

    "!!define": define,

    "!!help": help,
    "!!": send,
}


ADMIN_CMDS = {
    "!!upgrade": upgrade,
    "!!upgradeall": upgradeall,
}
