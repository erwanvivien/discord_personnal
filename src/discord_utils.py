import discord
import random

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see `!!help` for further information"
HOWTO_URL = "https://github.com/erwanvivien/discord_personnal"
ICON_URL = "https://raw.githubusercontent.com/erwanvivien/discord_personnal/master/assets/cri-logo.png"

BOT_COLOR = discord.Colour(0x7445ed)
ERROR_COLOR = discord.Colour(0xd11733)
WARN_COLOR = discord.Colour(0xe8a617)
VALID_COLOR = discord.Colour(0x55da50)

REPORT_CHANN_ID = 828710516318797924

HELP_EMBED = discord.Embed(title="Help", url="https://github.com/erwanvivien/discord_personnal",
                           description="**How to use the bot:**")

HELP_EMBED.add_field(name="• Mappings", value='''- [`!!map <mapping-name>`](https://github.com/erwanvivien/discord_personnal#mappings): It maps the file sent to the mapping-name. ⚠️ This needs an attached file
- [`!!define <mapping-name> any desc ...`](https://github.com/erwanvivien/discord_personnal#mappings): It adds a description to the said mapping
- [`!!mappings`](https://github.com/erwanvivien/discord_personnal#mappings): Displays all mappings
- [`!!<mapping-name>`](https://github.com/erwanvivien/discord_personnal#mappings): Sends back the file mapped''', inline=False)
HELP_EMBED.add_field(
    name="• Help", value="- [`!!help`](https://github.com/erwanvivien/discord_personnal#help): Displays this message", inline=False)
HELP_EMBED.set_thumbnail(url=ICON_URL)


def author_name(author, discriminator=True) -> str:
    """Get nick from msg author (discord) if exists

    Arguments:
        author {discordAuthor} -- The author of a message
        discriminator {bool} -- If we want the discriminator or not

    Returns:
        [str] -- The author's name
    """

    if not discriminator:
        return author.display_name
    return f"{author.name}#{author.discriminator}"


def create_embed(title, desc, colour=BOT_COLOR, url=HOWTO_URL, icon_url="", footer_url=ICON_URL, footer_text="Personnal"):
    """Creates a discord embed

    Returns:
        [discordEmbed] -- The embed
    """

    embed = discord.Embed(title=title,
                          description=desc,
                          colour=colour,
                          url=url)

    if icon_url:
        embed.set_thumbnail(url=icon_url)
    if footer_url or footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_url)

    return embed


async def error_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL,
                        icon_url="", footer_url=ICON_URL, footer_text="Personnal"):
    """Sends error message to discord (red)
    """
    return await message.channel.send(embed=create_embed(title, desc, ERROR_COLOR, url, icon_url, footer_url, footer_text))


async def send_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL,
                       icon_url="", footer_url=ICON_URL, footer_text="Personnal"):
    """Sends message to discord (bot_color)
    """

    return await message.channel.send(embed=create_embed(title, desc, BOT_COLOR, url, icon_url, footer_url, footer_text))


async def send_file(message, filename, content=""):
    """Sends file to discord
    """

    return await message.channel.send(content, file=discord.File(filename))


async def edit_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL,
                       icon_url="", footer_url=ICON_URL, footer_text="Personnal"):
    """Edits a message
    """
    return await message.edit(embed=create_embed(title, desc, BOT_COLOR, url, icon_url, footer_url, footer_text))


async def report(client, title, desc):
    report_channel = client.get_channel(REPORT_CHANN_ID)
    embed = create_embed(
        title, f"Reported message was :\n```{desc}```")
    await report_channel.send("<@289145021922279425>\n", embed=embed)
