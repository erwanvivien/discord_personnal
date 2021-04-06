import discord
import os

import requests
import datetime as date

import discord_utils as disc
import database as db


async def map(self, message, args):
    guild_id = message.guild.id
    if not args:
        return

    nb_mappings = len(db.mappings_get(guild_id))
    if nb_mappings > 5 and db.guild_premium(guild_id) <= date.datetime.now().timestamp():
        return await disc.error_message(message, title="Too many mappings", desc="It seems that your premium subscription has expired\n" +
                                        "Please visit ... if you want to have unlimited mappings")

    bind_to = args[0].lower()

    msg = await disc.send_message(message, title="Starting to download", desc="")

    folder = f"assets/{guild_id}"
    if not os.path.exists(folder):  # Creates the dir for the said guild
        os.mkdir(folder)

    # attach_id = message.attachments[0].id # Unsued ID
    attach_name = message.attachments[0].filename
    attach_url = message.attachments[0].url

    extension = attach_name.split('.')[-1]
    response = requests.get(attach_url)
    filename = f"{folder}/{bind_to}.{extension}"

    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    db.mappings_set(guild_id, bind_to, filename)
    await disc.edit_message(msg, title="Success !", desc=f"The file {attach_name} has been bound to {bind_to}.{extension}")


async def unmap(self, message, args):
    guild_id = message.guild.id
    if not args:
        return

    name = args[0].lower()

    res = db.mappings_get(guild_id)
    mappings = {e[0]: e[1] for e in res}
    if not name in mappings:
        return await disc.send_message(message, title="Error 😱", desc=f"{name} was not a valid mapping")

    db.mappings_rm(guild_id, name)
    await disc.send_message(message, title="Success !", desc=f"You have successfully unmapped {name}")


async def mappings(self, message, args):
    guild_id = message.guild.id
    mappings = db.mappings_get(guild_id)
    mappings_text = "\n".join(
        [f"`{e[0]}`" + (f": {e[2]}" if e[2] else "") for e in mappings])

    await disc.send_message(message, title="Your mappings", desc=mappings_text)


async def define(self, message, args):
    guild_id = message.guild.id
    if not args or len(args) <= 1:
        return

    name = args[0]
    definition = " ".join(args[1:])

    db.mappings_def(guild_id, name, definition)
    await disc.send_message(message, title="Definition set", desc=f"The mapping {name} has been defined to `{definition}`")


async def help(self, message, args):
    await message.channel.send(embed=disc.HELP_EMBED)


async def send(self, message, args):
    guild_id = message.guild.id
    if not args:
        return

    send = args[0]

    res = db.mappings_get(guild_id)
    mappings = {e[0]: e[1] for e in res}
    if not send in mappings:
        return

    path = mappings[send]
    await disc.send_file(message, path)


async def upgrade(self, message, args):
    pass

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
}
