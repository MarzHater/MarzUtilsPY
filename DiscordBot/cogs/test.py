import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
MarzID = int(getenv('MARZ_ID'))

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="test", description="Check if the bot works.")
    async def test(self, interaction: discord.Interaction):
        if interaction.user.id == MarzID:
            await interaction.response.send_message("Yes the bot works you dumbass")
        else:
            await interaction.response.send_message("You do not have permission to run this command")

async def setup(bot: commands.Bot):
    await bot.add_cog(Test(bot))