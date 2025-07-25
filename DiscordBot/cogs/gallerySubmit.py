import discord
from discord import app_commands, Attachment, Interaction
from discord.ext import commands
import sqlite3
import datetime
import os
import aiohttp
import uuid

DB_PATH = "gallery.db"
IMAGE_FOLDER = "gallery_images"

class GalleryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_db()
        os.makedirs(IMAGE_FOLDER, exist_ok=True)

    def init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                title TEXT NOT NULL,
                image_path TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )''')
            conn.commit()

    @app_commands.command(name="submit", description="Submit a VRChat image to the community gallery.")
    @app_commands.describe(
        title="Title of your image",
        image="Attach your VRChat image here"
    )
    async def submit_photo(self, interaction: Interaction, title: str, image: Attachment):
        if not image.content_type or not image.content_type.startswith("image/"):
            await interaction.response.send_message("Only image files are allowed!", ephemeral=True)
            return

        user = str(interaction.user)
        timestamp = datetime.datetime.utcnow().isoformat()

        async with aiohttp.ClientSession() as session:
            async with session.get(image.url) as resp:
                if resp.status != 200:
                    await interaction.response.send_message("Failed to download the image.", ephemeral=True)
                    return
                image_bytes = await resp.read()

        # Generate a unique filename and save the image
        ext = os.path.splitext(image.filename)[-1] or ".png"
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(IMAGE_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO submissions (user, title, image_path, timestamp) VALUES (?, ?, ?, ?)",
                      (user, title, filepath, timestamp))
            conn.commit()

        await interaction.response.send_message(
            f"✅ Image submitted by **{user}**!\nTitle: **{title}**"
        )

async def setup(bot):
    await bot.add_cog(GalleryCog(bot))