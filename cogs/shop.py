import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime
from utils.classes import DATABASE_DIRECTORY, emojis

def GetDay():
    return datetime.today().strftime('%d')

async def get_shop():
    embed = discord.Embed(title="Shop")
    msg = ""
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    shop_items = list(cursor.execute("SELECT * FROM SHOP_ITEMS"))
    for item in shop_items:
        msg += f"{item[1]} (ID: **{item[0]}**)\nPrice: {emojis.mora} **{item[2]}** "
        if item[3] == "True":
            msg += f"({item[4]} left)\n\n"
        else:
            msg += "\n\n"
    embed.description = msg
    return embed

class shop(commands.Cog):
    def __init__(self, client):
        self.client = client 
        self.reset_shop.start()
    @tasks.loop(hours=24)
    async def reset_shop(self):
        db = sqlite3.connect(DATABASE_DIRECTORY)
        cursor = db.cursor()
        shop_items = list(cursor.execute("SELECT * FROM SHOP_ITEMS"))
        for item in shop_items:
            if item[3] == "True":
                if item[6] == "monthly" and item[7] == int(GetDay()):
                    cursor.execute("UPDATE SHOP_ITEMS SET QUANTITY = ? WHERE ITEM_ID = ?", (item[5], item[0]))
        cursor.close()
        db.commit()
        db.close()
    @discord.app_commands.command()
    async def shop(self, interaction):
        shop_embed = await get_shop()
        await interaction.response.send_message(embed=shop_embed)
async def setup(client):
    await client.add_cog(shop(client))