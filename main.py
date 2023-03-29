import discord
from discord import app_commands
from discord.ext import commands, tasks

import json, requests


with open("config.json") as f:
    config = json.load(f)


bot = commands.Bot(command_prefix="infinity!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    change_status.start()

    # try:
    #     synced = await bot.tree.sync()
    #     print(f"Synced {len(synced)} command(s)")
    # except Exception as e:
    #     print(f"{e}")

@tasks.loop(seconds=30)
async def change_status():
    await bot.wait_until_ready()

    req = requests.get(config["api"])
    response = json.loads(req.text)["player"]
    # guild = bot.get_guild(863866118677987349)
    if response != -1:
        text = f"🟢 {response} Players!"
    else:
        text = f"🔴 Offline!"
    activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run(config["token"])