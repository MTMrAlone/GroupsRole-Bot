import discord
from discord.ext import commands, tasks
from discord import app_commands

import json, group


with open("config.json") as f:
    config = json.load(f)


bot = commands.Bot(command_prefix="infinity!", intents=discord.Intents.all())


@bot.event
async def setup_hook():
    print("Cogs loaded!")
    await group.setup(bot)


@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    server_status.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"{e}")


@tasks.loop(seconds=30)
async def server_status():
    await bot.wait_until_ready()

    guild = bot.get_guild(config["guild"]).member_count
    text = f"{guild} Members!"
    activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run(config["token"])