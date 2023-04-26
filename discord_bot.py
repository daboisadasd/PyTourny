import sqlite3
import logging
from keys import bot_token
from discord.ext import commands

# create a connection to the SQLite database
connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

# create the offlineuser, offlinewinners, and offlineuserqueue tables if they don't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS offlineuser
                  (user_id INTEGER PRIMARY KEY, username TEXT)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS offlinewinners
                  (user_id INTEGER PRIMARY KEY, username TEXT, win_count INTEGER)"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS offlineuserqueue
                  (user_id INTEGER PRIMARY KEY, username TEXT)"""
)

# create a logging instance and add a handler that prints all logs at the INFO level and above to the console
logging.basicConfig(level=logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(console_handler)

bot = commands.Bot(command_prefix="/")
offlines_bot_channel_id = (
    1099368104712220713  # replace with the actual ID of the offlines-bot channel
)


# command to add a user to the offline user queue
@bot.slash_command(description="Add a user to the offline user queue")
async def offlinequeue(ctx):
    user_id = ctx.author.id
    username = ctx.author.name

    # check if the user is already in the database
    cursor.execute("SELECT * FROM offlineuserqueue WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result:
        await ctx.send(
            f"{ctx.author.mention}, you are already in the offline user queue!"
        )
        return

    # add the user to the database
    cursor.execute("INSERT INTO offlineuserqueue VALUES (?, ?)", (user_id, username))
    connection.commit()

    await ctx.send(
        f"{ctx.author.mention}, you have been added to the offline user queue!"
    )


# command to pick a winner from the offline user queue
@bot.slash_command(description="Pick a winner from the offline user queue")
async def winner(ctx):
    # get the first user in the queue
    cursor.execute("SELECT * FROM offlineuserqueue ORDER BY user_id")
    result = cursor.fetchone()
    if not result:
        await ctx.send("The offline user queue is empty!")
        return

    # ping the winner and send a message to the offlines-bot channel
    winner_id, winner_name = result
    member = ctx.guild.get_member(winner_id)
    if member:
        await ctx.send(f"{member.mention}, you're up!")
        offlines_bot_channel = bot.get_channel(offlines_bot_channel_id)
        await offlines_bot_channel.send("you're up in lobby!")

    # remove the winner from the queue
    cursor.execute("DELETE FROM offlineuserqueue WHERE user_id=?", (winner_id,))
    connection.commit()


# command to list all available commands
@bot.slash_command(name="help", description="List all available commands")
async def list_commands(ctx):
    command_list = "\n".join([f"/{c.name}" for c in bot.commands])
    await ctx.send(f"Here are the available commands:\n{command_list}")


# run the bot
bot.run(bot_token)
