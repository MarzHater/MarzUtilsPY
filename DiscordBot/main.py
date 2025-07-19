import os
from os import getenv
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

load_dotenv()
token = getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents = intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

async def main():
    async with bot:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.start(token)
asyncio.run(main())