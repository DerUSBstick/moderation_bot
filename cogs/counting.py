import discord
from discord.ext import commands
import json
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import asyncio
import datetime

async def convert_to_date(time):
    time = time.split(".")[0].replace("-", "/")
    result = datetime.datetime.strptime(time, "%Y/%m/%d %H:%M:%S") + datetime.timedelta(seconds=1)
    return result

async def counting_message(message):
    with open("./data/counting.json") as f:
        counting = json.load(f)
    if message.webhook_id == None:
        if message.content != str(counting["current_count"]):
            return await message.delete()
        counting["current_count"] += 1
        if message.author.id in counting["users"]:
            counting[f"{message.author.id}"] += 1
        else:
            counting["users"].append(message.author.id)
            counting[f"{message.author.id}"] = 1
        await counting_webhook(message.author.name, message.author.avatar_url, counting["current_count"] - 1)
        if counting["webhook"]["last"] < 3:
            counting["webhook"]["last"] += 1
        else:
            counting["webhook"]["last"] = 1
        counting["recovery"] = {
            "last_message": f"{message.created_at}",
            "user": message.author.id
        }
        await message.delete()
        with open("./data/counting.json", "w+") as f:
            json.dump(counting, f, indent=4)

async def counting_webhook(USERNAME, USER_AVATAR_URL, NUMBER):
    with open("./data/counting.json") as f:
        data = json.load(f)
    last = data["webhook"]["last"]
    webhook = data["webhook"][f"{last}"]
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(f'{webhook}', adapter=AsyncWebhookAdapter(session))
        await webhook.send(content=f"{NUMBER}", username=USERNAME, avatar_url=USER_AVATAR_URL)
        await session.close()

class counting(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 981634202049069106:
            await counting_message(message)
def setup(client):
    client.add_cog(counting(client))