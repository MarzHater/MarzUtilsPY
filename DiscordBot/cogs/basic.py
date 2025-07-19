import discord
import asyncio
from discord.ext import commands
from discord import app_commands, Interaction
from dotenv import load_dotenv
from os import getenv
from utils import text_to_owo

load_dotenv()
MarzID = int(getenv('MARZ_ID'))

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="owo", description="Converts text to owo")
    async def owo(self, interaction: Interaction, text:str ):
        await interaction.response.send_message(text_to_owo(text))

    @app_commands.command(name="cname", description="Lists all current domains and subdomains under Marz's name")
    async def cname(self, interaction: Interaction):
        with open('domainlist.txt') as f:
            content = f.read()
            await interaction.response.send_message(f"```diff\n{content}\n```")

async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))