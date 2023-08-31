import discord
from discord.ext import commands
import sqlite3
from typing import Literal
from utils.classes import DATABASE_DIRECTORY

convert_type = {
    "LEVEL": 2,
    "BALANCE": 3,
    "COUNTING": 6
}

def get_user_name(self, USERID):
    try:
        return self.client.get_user(USERID).name
    except:
        return "None"

def get_leaderboard(self, type: str):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    data = cursor.execute(f"SELECT * FROM USERS ORDER BY {type.upper()} DESC")
    embed = discord.Embed(title=f"{type} Leaderboard")
    msg = '```md\nRank. | Score   | User \n======================================\n'
    i = 0
    space = " "
    no_space = ""
    for x in data:
        i += 1
        USER = str(get_user_name(self, x[0])).replace("_", "")
        USER_DATA = x[convert_type[type.upper()]]
        msg += f"{i}. {space if len(str(i)) < 2 else no_space}  | {USER_DATA}{space*(8-len(str(USER_DATA)))}| {USER}\n"
        #print(x[0], x[convert_type[type.upper()]])
        if i == 10:
            break
    msg += "```"
    embed = discord.Embed(title=f"{type} Leaderboard", description=msg) 
    return embed

class leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
    @discord.app_commands.command()
    async def leaderboard(self, interaction, leaderboard: Literal["Level", "Balance", "Counting"]):
        leaderboard_embed = get_leaderboard(self, leaderboard)
        leaderboard_embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=leaderboard_embed)

async def setup(client):
    await client.add_cog(leaderboard(client))