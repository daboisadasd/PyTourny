import logging
import sqlite3
import discord
from discord.ext import commands, tasks
import keys
import os
import sys
import django
from django.template.loader import render_to_string
from django.conf import settings
from offline_raids_info_app.models import OfflineUsers, OfflineWinners, OfflineUserQueue

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# set up the Django environment
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "offline_raids_info.settings")
django.setup()

# import models


# create a connection to the SQLite database
connection = sqlite3.connect("offline_users.db")
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
logging.basicConfig(level=logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger("").addHandler(console_handler)

bot = commands.Bot(command_prefix="!")
offlines_bot_channel_id = (
    1099368104712220713  # replace with the actual ID of the offlines-bot channel
)


@bot.command()
async def offlinejoin(ctx):
    user_id = ctx.author.id
    username = ctx.author.name

    # check if the user is already in the database
    if OfflineUsers.objects.filter(user_id=user_id).exists():
        await ctx.send(
            f"{ctx.author.mention}, you are already in the offline user list!"
        )
        return

    # add the user to the database
    OfflineUsers.objects.create(user_id=user_id, username=username)

    await ctx.send(
        f"{ctx.author.mention}, you have been added to the offline user list!"
    )


@bot.command()
async def offlinewinner(ctx):
    user_id = ctx.author.id
    username = ctx.author.name

    # check if the user is already in the database
    winner = OfflineWinners.objects.filter(user_id=user_id).first()
    if winner:
        # increment the win_count field
        winner.win_count += 1
        winner.save()
        await ctx.send(f"{ctx.author.mention}, you have won {winner.win_count} times!")
        return

    # add the user to the database
    OfflineWinners.objects.create(user_id=user_id, username=username, win_count=1)

    await ctx.send(
        f"{ctx.author.mention}, you have been added to the offline winners list!"
    )


@bot.command()
async def offlinequeue(ctx):
    user_id = ctx.author.id
    username = ctx.author.name

    # check if the user is already in the database
    if OfflineUserQueue.objects.filter(user_id=user_id).exists():
        await ctx.send(
            f"{ctx.author.mention}, you are already in the offline user queue!"
        )
        return

    # add the user to the database
    OfflineUserQueue.objects.create(user_id=user_id, username=username)

    await ctx.send(
        f"{ctx.author.mention}, you have been added to the offline user queue!"
    )


@bot.command()
async def winner(ctx):
    # get the first user in the queue
    winner = OfflineUserQueue.objects.order_by("user_id").first()

    if not winner:
        await ctx.send("The offline user queue is empty!")
        return

    # ping the winner and send a message to the offlines-bot channel
    member = ctx.guild.get_member(winner.user_id)
    if member:
        await ctx.send(f"{member.mention}, you're up!")
        offlines_bot_channel = bot.get_channel(offlines_bot_channel_id)
        await offlines_bot_channel.send("you're up in lobby!")

    # remove the winner from the queue
    winner.delete()

    # update the website
    offline_winners = OfflineWinners.objects.order_by("-win_count")
    offline_user_queue = list(OfflineUserQueue.objects.all())
    context = {
        "offline_winners": offline_winners,
        "offline_user_queue": offline_user_queue,
    }
    html = render_to_string("offline_raids_info_app/index.html", context)
    with open(os.path.join(BASE_DIR, "static/index.html"), "w") as f:
        f.write(html)


@tasks.loop(seconds=5)
async def update_website():
    # update the website
    offline_winners = OfflineWinners.objects.order_by("-win_count")
    offline_user_queue = list(OfflineUserQueue.objects.all())
    context = {
        "offline_winners": offline_winners,
        "offline_user_queue": offline_user_queue,
    }
    html = render_to_string("offline_raids_info_app/index.html", context)
    with open(os.path.join(BASE_DIR, "static/index.html"), "w") as f:
        f.write(html)


bot.run(keys.bot_token)
