import discord, sqlite3
from discord.ext import commands, tasks
import time
import sys
import datetime
from utils.classes import functions, emojis, DATABASE_DIRECTORY
from traceback import print_exception

async def edit_embed(self, MESSAGE_CONTENT):
    embed = discord.Embed(title="Status", description=MESSAGE_CONTENT, color=0x0062ff, timestamp=datetime.datetime.now())
    guild = self.client.get_guild(854733975197188108)
    channel = guild.get_channel(965523098885582848)
    message = await channel.fetch_message(965674314462552064)
    await message.edit(embed=embed, content="")


def validate_data(data):
    return data[0], data[1], data[2], data[3], data[4]
class status(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.bot_status.start()
        self.discord_status.start()
    @tasks.loop(minutes=1)
    async def discord_status(self):
        await self.client.change_presence(activity=discord.Game(name="V1.9.8"))
    @tasks.loop(seconds=20)
    async def bot_status(self):
        db = sqlite3.connect(DATABASE_DIRECTORY)
        cursor = db.cursor()
        data = cursor.execute("SELECT * FROM BOT_STATUS").fetchall()
        bots:list = ["Alhaitham", "Diluc", "Kaeya", "Tartaglia", "Zhongli"]
        msg = ""
        for bot in data:
            status, name, id, channel, downtime = validate_data(bot)
            #channel = self.client.get_channel(channel)
            bot_status = self.client.get_guild(854733975197188108).get_member(id).raw_status
            if bot_status == "online":
                if status == 0:
                    cursor.execute(f'UPDATE BOT_STATUS SET STATUS = ? WHERE BOT_NAME = ?', (1, name))
                cursor.execute(f'UPDATE BOT_STATUS SET DOWN_SINCE = ? WHERE BOT_NAME = ?', (round(time.time()), name))
                msg += f"{name}\n{emojis.status_informations} Online {emojis.status_online}\n{emojis.status_informations} <#{channel}>\n\n"
            elif bot_status == "offline":
                if status == 1:
                    cursor.execute(f'UPDATE BOT_STATUS SET STATUS = ? WHERE BOT_NAME = ?', (0, name))
                down_time = functions.parse_duration(self.client, round(time.time() - downtime))
                msg += f"{name}\n{emojis.status_informations} {down_time} {emojis.status_offline}\n{emojis.status_informations} <#{channel}>\n\n"
        db.commit()
        cursor.close()
        db.close()
        await edit_embed(self, msg)
async def setup(client):
    await client.add_cog(status(client))