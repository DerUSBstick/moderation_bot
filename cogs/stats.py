import discord
from discord.ext import commands

class stats(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

async def setup(client):
    await client.add_cog(stats(client))