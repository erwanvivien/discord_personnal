import discord
import os

import discord_utils as disc


async def map(self, message, args):
    pass


async def unmap(self, message, args):
    pass


async def mappings(self, message, args):
    pass


async def define(self, message, args):
    pass


async def help(self, message, args):
    await message.channel.send(embed=disc.HELP_EMBED)


async def send(self, message, args):
    pass


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
