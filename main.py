import discord
from discord.ext import tasks, commands
import sqlite3
import time
import django
import twitchAPI
import bs4
import logging
import logging.handlers
import os
import datetime
import keys

# log debug to console
logging.basicConfig(level=logging.DEBUG)

# connect to sqlite3 db
sqlite3.connect("pyTourney.sqlite")

# Login to discord api
bot = commands.Bot(
    command_prefix=[
        "$",
    ],
    intents=discord.Intents.all(),
)

# check for existing logfile and rename if true
now = datetime.datetime.now()
logfile = "discord.log"
logfilebak = f"{logfile}.{now.month}-{now.day}-{now.hour}-{now.minute}"
log_encoding = "utf-8"
loghandler_mode = "w"
loglevel = logging.DEBUG

if os.path.exists(logfile):
    print(f"discord.log exists, renaming existing logfile to {logfilebak}")
    os.rename(logfile, logfilebak)

# enable logging
loghandler = logging.FileHandler(
    filename=logfile, encoding=log_encoding, mode=loghandler_mode
)
logger = logging.getLogger("discord")
logger.setLevel(loglevel)
loghandler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(loghandler)


# discord.utils.setup_logging(handler=loghandler, level=loglevel, root=True)


# tell you when bot is ready to start work
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# listen for keywords and respond
@bot.event
async def on_message(message):
    print(f"{message.channel.name},{message.author.name},{message.content}")

    if message.author == bot.user:
        return

    if message.channel.name == "offlines-bot":
        return

    if message.content.startswith("$hello"):
        await message.channel.send(f"Hello {message.author.name}!")

    if message.content.startswith("$test"):
        await message.channel.send(f"are you testing me {message.author.name}!")

    if message.content.startswith("$dead"):
        await message.channel.send(f"you died {message.author.name}!")

    if not message.content == "$hello" "$dead":
        await message.channel.send(
            f"Hello {message.author.name}! Only the following commands can be used in this channel. $hello $dead"
        )


@bot.slash_command()
async def test(ctx):
    await ctx.respond(embed=discord.Embed(title="Test worked"))


# tells the bot to run
bot.run(keys.bot_token)
