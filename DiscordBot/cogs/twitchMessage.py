import discord
import aiohttp
import asyncio
import datetime
from discord.ext import tasks, commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
class TwitchAnnouncer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(getenv('ANNOUNCEMENTS_ID'))
        self.twitch_username = getenv('TWITCH_USERNAME')
        self.client_id = getenv('TWITCH_CLIENT_ID')
        self.client_secret = getenv('TWITCH_CLIENT_SECRET')

        self.access_token = None
        self.twitch_user_id = None
        self.is_live = False

        bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.get_access_token()
        await self.get_user_id()
        self.twitch_checker.start()


    async def get_access_token(self):
        async with aiohttp.ClientSession() as session:
            url = 'https://id.twitch.tv/oauth2/token'
            params = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            async with session.post(url, params=params) as resp:
                data = await resp.json()
                self.access_token = data['access_token']

    async def get_user_id(self):
        async with aiohttp.ClientSession() as session:
            url = f'https://api.twitch.tv/helix/users?login={self.twitch_username}'
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {self.access_token}'
            }
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                self.twitch_user_id = data['data'][0]['id']

    async def check_stream_status(self):
        async with aiohttp.ClientSession() as session:
            url = f'https://api.twitch.tv/helix/streams?user_id={self.twitch_user_id}'
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {self.access_token}'
            }
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                if data['data']:
                    stream = data['data'][0]
                    if not self.is_live:
                        self.is_live = True
                        await self.announce_stream(stream)
                else:
                    self.is_live = False

    async def announce_stream(self, stream):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("Announcement channel not found.")
            return

        title = stream['title']
        game_name = stream.get('game_name', 'Unknown Game')
        url = f"https://twitch.tv/{self.twitch_username}"
        thumbnail_url = stream['thumbnail_url'].replace("{width}", "1280").replace("{height}", "720")

        embed = discord.Embed(
            title=f"{self.twitch_username} is now live!",
            description=f"**{title}**\nPlaying: {game_name}\n\n[Watch here]({url})",
            color=discord.Color.purple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=thumbnail_url)

        await channel.send(embed=embed)

        await channel.send(f"<@&{1396962248144064652}> We are live!") #Hardcoded Role ID to ping, can change here!

    @tasks.loop(seconds=60)
    async def twitch_checker(self):
        await self.check_stream_status()

    @twitch_checker.before_loop
    async def before_twitch_checker(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(TwitchAnnouncer(bot))