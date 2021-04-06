import discord
from discord.ext import commands
import datetime

import asyncio

import discord_utils as disc
import utils

import commands
import database as db

ERRORS = []
DISC_LNK_DEV = "https://discord.com/api/oauth2/authorize?client_id=819549722422673448&permissions=2147544128&scope=bot%20applications.commands"
DISC_LNK = "https://discord.com/api/oauth2/authorize?client_id=819549623172726824&permissions=2147544128&scope=bot%20applications.commands"

token_file_name = "token_dev"
token = utils.get_content(token_file_name)


class Client(discord.Client):
    async def on_ready(self):
        print(f'[OverCRI] Logged on as {self.user}')
        print(f"invite link: ↓\n{DISC_LNK}")
        print('==============================================================================================')
        print()

        if token_file_name == "token":
            await disc.report(self, "Started", "Started successfully !")

    async def on_message(self, message):
        author_id = message.author.id
        if author_id in utils.BOT_IDS:        # Doesn't do anything if it's a bot message
            return

        split = message.content.split(' ', 1)  # separate command from args
        cmd = split[0].lower()
        args = split[1].split(' ') if len(split) > 1 else []

        if not cmd.startswith("!!"):
            return

        # Get Discord Nick if existant or discord Name
        name = disc.author_name(message.author, False)

        # Runs command if it's a known command
        if cmd != "!!" and cmd in CMDS:
            utils.log("on_message", "Command execution",
                      f"{name} from discord {message.guild.id} issued {cmd} command. <{args}>")

            await CMDS[cmd](self, message, args)
        elif cmd.startswith("!!"):
            args = [cmd[2:]] + args
            utils.log("on_message", "Command execution",
                      f"{name} from discord {message.guild.id} issued !! command. <{args}>")
            await CMDS['!!'](self, message, args)


db.create()  # Will setup the database
client = Client()  # Creates a client


# async def cron():
#     await client.wait_until_ready()
#     while True:
#         try:
#             pass
#         except Exception as e:
#             pass


# Needed for async work
# if token_file_name == "token":
#     client.loop.create_task(cron())

client.run(token)
