import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import time
import sqlite3
from utils.classes import functions, DATABASE_DIRECTORY


def get_database_latency():
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    start_time = time.time()
    cursor.execute("SELECT * FROM USERS")
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    return latency


start = time.time()
class general(commands.Cog):
    def __init__(self, client):
        self.client = client
    @discord.app_commands.command()
    async def ping(self, interaction):
        db_latency = get_database_latency()
        delay = round(self.client.latency*1000, 4)
        await interaction.response.send_message(f"Bot Latency {delay}ms\nDatabase Latency {db_latency}ms")
    @discord.app_commands.command()
    async def uptime(self, interaction):
        online_since = functions.parse_duration(self.client, round(time.time() - start))
        await interaction.response.send_message(f"Uptime: {online_since}")
    @discord.app_commands.command()
    async def join_number(self, interaction: discord.Interaction):
        guild = self.client.get_guild(854733975197188108)
        members = list(guild.members)
        members.sort(key=lambda m: m.joined_at)
        i = 1
        for member in members:
            if not member.bot:
                if member.id == interaction.user.id:
                    break
                i += 1
        await interaction.response.send_message(f"You are in position {i} out of {len(members)}.")

async def setup(client):
    await client.add_cog(general(client))