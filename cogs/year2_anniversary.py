import discord
from discord.ext import commands, tasks
import sqlite3, json
import time, datetime, numpy
import logging
import os
import math
from typing import Literal

custom_events_logger = logging.getLogger('2 Year')
custom_events_logger.setLevel(logging.INFO)
custom_events_logger.addHandler(logging.FileHandler('../2year.log'))
custom_events_logger.addFilter(lambda record: record.name == '2 Year')

def log_custom_event(message):
    custom_events_logger.info(message)
VISIONS = ["Pyro", "Hydro", "Anemo", "Electro", "Dendro", "Cryo", "Geo"]
NUMBERS = ["one", "two", "three", "four"]
DB_PATH = "../2year.db"
POLLS_CHANNEL = 1081649659518390303

UNTIL_CLOSE = 82800
UNTIL_EVALUATION = 84600

CONTRIBUTORS = [311194546753110027, 579482865788649504, 699932326909575258, 313346783222693888, 481058521434292235, 900836824778440785, 512788515814375429, 900836824778440785]

VISION_EMOJIS = {
        "Anemo": "<:element_anemo:1081651596372492288>",
        "Pyro": "<:element_pyro:1081651535714463864>",
        "Hydro": "<:element_hydro:1081651570749489194>",
        "Electro": "<:element_electro:1081651629536854067>",
        "Cryo": "<:element_cryo:1081651687632150588>",
        "Geo": "<:element_geo:1081651712911233074>",
        "Dendro": "<:element_dendro:1081651659450626161>"
        }
NUMBER_EMOJIS = [
    "<:transparent1:1112803677380558908>",
    "<:transparent2:1112804429662531594>",
    "<:transparent3:1112804532435550279>",
    "<:transparent4:1112804624299212892>"
    ]
ADVANCED_INFOS = {
        "0": "✅ Correct Answer",
        "1": "❌ Incorrect Answer",
        "2": "<:IttoBonk:918262650796912641> Vote Dismissed", 
        "3": "<:IttoConfused:920453295615643658> Vote not present"
        }

def get_log_file_size():
    sizes = ["B", "KB", "MB", "GB", "TB"]
    file_size = os.path.getsize("../2year_logs.json")
    if file_size == 0:
        return "0B"
    i = int(math.floor(math.log(file_size, 1024)))
    size = file_size / math.pow(1024, i)
    return "{:.2f} {}".format(size, sizes[i])

class year2(discord.app_commands.Group):
    ...

year2_commands = year2(name="year2", description="Anniversary Stats")

def get_user_name(client: discord.Client, USERID: int):
    try:
        return client.get_user(USERID).name
    except:
        return "None"

def get_leaderboard_year2(interaction: discord.Interaction) -> discord.Embed:
    db = sqlite3.connect("../2year.db")
    cursor = db.cursor()
    data = cursor.execute(f"SELECT * FROM USER_DATA ORDER BY OVERALL_RANK_BY_SCORE ASC")
    msg = '```md\nRank. | Score   | User \n======================================\n'
    i = 0
    user_rank = None
    score = None
    space = " "
    no_space = ""
    for x in data:
        if x[0] == interaction.user.id:
            user_rank = x[46]
            score = x[47]
        if x[46] == None:
            continue
        i += 1
        # print(x)
        # print(x[46])
        USER = str(get_user_name(interaction.client, x[0])).replace("_", "")
        USER_DATA = x[47]
        if i <= 10:
            msg += f"{i}. {space if len(str(i)) < 2 else no_space}  | {USER_DATA}{space*(8-len(str(USER_DATA)))}| {USER}\n"
        #print(x[0], x[convert_type[type.upper()]])
    msg += "```"
    embed = discord.Embed(title=f"2-Year-Anniversary Leaderboard", description=msg)
    embed.set_footer(text=f"You are ranked {user_rank} with a score of {score}")
    return embed

@year2_commands.command(description="Get the Leaderboard of the second anniversary")
async def leaderboard(interaction: discord.Interaction):
    embed = get_leaderboard_year2(interaction)
    return await interaction.response.send_message(embed=embed)

def get_question_data(QUESTIONID):
    correct = "<:correct:1132999449287852156>"
    incorrect = "<:incorrect:1132999712753070202>"
    with open("../2year.json") as f:
        data = json.load(f)
    if QUESTIONID not in data["polls"]:
        return None
    answer_a = data[f"{QUESTIONID}"]["a"]
    answer_b = data[f"{QUESTIONID}"]["b"]
    answer_c = data[f"{QUESTIONID}"]["c"]
    answer_d = data[f"{QUESTIONID}"]["d"]
    solution = data[f"{QUESTIONID}"]["solution"]
    category = data[f"{QUESTIONID}"]["type"]
    difficulty = data[f"{QUESTIONID}"]["difficulty"]
    point_text = "1 Point" if difficulty == "Easy" else "3 Points" if difficulty == "Medium" else "5 Points"
    embed_color = 0x00ff17 if difficulty == "Easy" else 0xffff00 if difficulty == "Medium" else 0xff0000
    embed = discord.Embed(color=embed_color, title=data[f"{QUESTIONID}"]["question"], description=f"{correct if 'A' in solution else incorrect} {answer_a}\n{correct if 'B' in solution else incorrect} {answer_b}\n{correct if 'C' in solution else incorrect} {answer_c}\n{correct if 'D' in solution else incorrect} {answer_d}")
    embed.set_footer(text=f"{difficulty} ꞏ {point_text} ꞏ {category} ꞏ ID {QUESTIONID}")
    return embed
    

@year2_commands.command(description="View Informations about certain Polls")
async def question(interaction: discord.Interaction, question: int):
    question_data = get_question_data(question)
    if question_data == None:
        return await interaction.response.send_message("Invalid Question")
    return await interaction.response.send_message(embed=question_data)

@year2_commands.command(description="View Results")
async def results(interaction: discord.Interaction):
    file = discord.File('./images/year2_results.png')  
    embed = discord.Embed(title="2-Year Anniversary Results")
    embed.set_image(url='attachment://year2_results.png')
    await interaction.response.send_message(file = file, embed=embed)

def check_entry_existence_year2(userid: int):
    DB = sqlite3.connect("../2year.db")
    cursor = DB.cursor()
    result = cursor.execute(f"SELECT USERID FROM USER_DATA WHERE USERID = {userid}").fetchone()
    cursor.close()
    DB.close()
    return result

@year2_commands.command(description="View Event Stats for yourself")
async def stats(interaction: discord.Interaction, question_type: Literal["General", "Diluc"]=None, difficulty: Literal["Easy", "Medium", "Hard"]=None):
    user = interaction.user
    if check_entry_existence_year2(user.id) == None:
        return await interaction.response.send_message("You didn't participate in the second anniversary!")
    with open("../2year.json") as f:
        anniversary_data = json.load(f)
    db = sqlite3.connect("../2year.db")
    cursor = db.cursor()
    msg = ""
    vision = cursor.execute(f"SELECT VISION FROM USER_DATA WHERE USERID = {user.id}").fetchone()[0]
    vision_emoji = VISION_EMOJIS[f"{vision}"]
    embed = discord.Embed(title="2-Year Anniversary Stats", description=f"{vision_emoji} **{vision}**")
    embed.set_footer(text=f"Difficulty: {difficulty} ꞏ Type: {question_type}")
    for x in range(1, 45):
        if anniversary_data[f"{x}"]["type"] == question_type or question_type == None:
            if anniversary_data[f"{x}"]["difficulty"] == difficulty or difficulty == None:
                msg += f"**POLL ID {x}**\n"
                poll_data = cursor.execute(f"SELECT POLL_{x} FROM USER_DATA WHERE USERID = {user.id}").fetchone()[0]
                if poll_data == None:
                    msg += f"<:nv:1133001080989569105>"
                elif poll_data in anniversary_data[f"{x}"]["solution"]:
                    msg += f"<:c:1132999449287852156>"
                else:
                    msg += f"<:i:1132999712753070202>"
                msg += "<:D:1133007350194765824>" if anniversary_data[f"{x}"]["type"] == "Diluc" else "<:g:1133007185538977793>"
                msg += "\n"
                if x in [15, 30] or x == 44:
                    embed.add_field(name="᲼᲼", value=msg)
                    msg = ""
    if msg != "":
        embed.add_field(name="᲼᲼", value=msg)
    return await interaction.response.send_message(embed=embed)

class anniversary2(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

async def setup(client):
    await client.add_cog(anniversary2(client))