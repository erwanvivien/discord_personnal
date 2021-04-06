import discord
import os

import discord_utils as disc


async def map(self, message, args):
    if not message.attachments:
        return await disc.error_message(message, desc="Please provide a file as attachement")
    if not args:
        return await disc.error_message(message, desc="Please provide a name to this file")

    bind_to = args[0]

    if bind_to == '--force':
        return await disc.error_message(message, desc="Please provide a name different from --force")
    if bind_to in CMD_MAP and not "--force" in args:
        return await disc.error_message(message, title="This mapping already exists", desc="pass --force to overwrite this file")

    msg = await disc.send_message(message, title="Starting to download", desc="")
    return


async def unmap(self, message, args):
    if not args:
        return await disc.error_message(message, desc="Please provide a valid mapping to delete")

    mapping = args[0]
    if not mapping in CMD_MAP:
        return await disc.error_message(message, desc="Please provide a valid mapping to delete")

    return


async def mappings(self, message, args):
    pass
    # msg = ""
    # for k, v in CMD_MAP.items():
    #     msg += f"`{k}`: {v[CMD_INDEX_DESC]}\n"

    # await disc.send_message(message, title="Mappings", desc=msg)


async def define(self, message, args):
    if not args:
        return await disc.error_message(message, desc="Please provide a mapping to define")

    if not args[0] in CMD_MAP:
        return await disc.error_message(message, desc="Please provide a mapping that exist")
    if len(args) <= 1:
        return await disc.error_message(message, desc="Please provide a message for this mapping")


async def help(self, message, args):
    await message.channel.send(embed=disc.HELP_EMBED)
