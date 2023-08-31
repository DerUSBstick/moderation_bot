import json, sys
from discord.ext import commands, tasks
from urllib import request
from traceback import print_exception

YOUTUBE_CHANNEL_ID = "SECRET_ID"
YOUTUBE_API_TOKEN = "TOKEN"
YOUTUBE_COUNTER_CHANNEL_ID = 980034765501636608

class ytapi(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.subscriber_counter.start()
    @tasks.loop(minutes=5)
    async def subscriber_counter(self):
        data = request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={YOUTUBE_CHANNEL_ID}&key={YOUTUBE_API_TOKEN}").read()
        subs = json.loads(data)['items'][0]['statistics']['subscriberCount']
        channel_counter = await self.client.fetch_channel(YOUTUBE_COUNTER_CHANNEL_ID)
        await channel_counter.edit(name=f"{subs[0:3]}K Subs")
async def setup(client):
    await client.add_cog(ytapi(client))