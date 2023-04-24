import json

import discord
from discord import app_commands
from discord.ext import commands

# Load Config
with open("config.json") as f:
    config = json.load(f)

choices = []
for i in range(len(config["factions"])):
    choices.append(app_commands.Choice(name=config["factions"][i]["name"], value=i))

class Faction(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    @app_commands.command(name="give", description="Give role to a user")
    @app_commands.describe(user="Mention user", faction="Select your faction", role="Select role to give")
    @app_commands.choices(faction=choices)
    async def give(self, interaction: discord.Interaction, user: discord.Member, 
                   faction: app_commands.Choice[int], role: discord.Role):
        moderator = interaction.guild.get_role(config["factions"][faction.value]["moderator"])
        roles = [interaction.guild.get_role(i) for i in config["factions"][faction.value]["roles"]]
        if not (moderator in interaction.user.roles) or not (role in roles) or role in user.roles:
            embed = discord.Embed(title=config["embed_header"], description="You can't give role.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        
        await user.add_roles(role)
        embed = discord.Embed(title=config["embed_header"], 
                              description=f"{user.mention} recived {role.mention} from {interaction.user.mention}")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="take", description="Take role to a user")
    @app_commands.describe(user="Mention user", faction="Select your faction", role="Select role to take")
    @app_commands.choices(faction=choices)
    async def take(self, interaction: discord.Interaction, user: discord.Member, 
                   faction: app_commands.Choice[int], role: discord.Role):
        moderator = interaction.guild.get_role(config["factions"][faction.value]["moderator"])
        roles = [interaction.guild.get_role(i) for i in config["factions"][faction.value]["roles"]]
        if not (moderator in interaction.user.roles) or not (role in roles) or not (role in user.roles):
            embed = discord.Embed(title=config["embed_header"], description="You can't take role.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        
        
        await user.remove_roles(role)
        embed = discord.Embed(title=config["embed_header"], 
                              description=f"{interaction.user.mention} revoked {role.mention} from {user.mention}")
        await interaction.response.send_message(embed=embed)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Faction(bot))
