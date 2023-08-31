import discord
from discord.ext import commands
import json
from typing import Literal
from utils.classes import emojis
import sqlite3
"""
1 Year Anniversary
"""
VISION_EMOJIS = {
        "Unknown": "⚠️ Couldn't be Identified. DM DerUSBstick to fix this ⚠️",
        "Anemo": f"{emojis.anemo}",
        "Pyro": f"{emojis.pyro}",
        "Hydro": f"{emojis.hydro}",
        "Electro": f"{emojis.electro}",
        "Cryo": f"{emojis.cryo}",
        "Geo": f"{emojis.geo}",
        "Dendro": f"{emojis.dendro}"
        }
ADVANCED_INFOS = {
        "0": "✅ Correct Answer",
        "1": "❌ Incorrect Answer",
        "2": f"{emojis.IttoBonk} Vote Dismissed", 
        "3": f"{emojis.IttoConfused} Vote not present"
        }
async def check_dup(poll, list):
    a = []
    dismiss = []
    for reaction in list[f"{poll}"]["reactions"]:
        if list[f"{poll}"][f"{reaction}"]["users"] != 0:
            for user in list[f"{poll}"][f"{reaction}"]["users"]:
                if user in a:
                    dismiss.append(user)
                a.append(user)
    return dismiss
async def check_answers(USER):
    data2 = await read_file("anniversary")
    data = await read_file("anniversary_polls")
    data3 = {}
    reacted = False
    for POLL in data["polls"]:
        ANSWER = data2["questions"][f"{POLL}"]["answer"]
        ANSWER = ANSWER.replace("a", "1\ufe0f\u20e3")
        ANSWER = ANSWER.replace("b", "2\ufe0f\u20e3")
        ANSWER = ANSWER.replace("c", "3\ufe0f\u20e3")
        ANSWER = ANSWER.replace("d", "4\ufe0f\u20e3")
        dismiss = await check_dup(POLL, data)
        if USER in dismiss:
            data3[f"{POLL}"] = "2"
        else:
            for REACTION in data[f"{POLL}"]["reactions"]:
                if data[f"{POLL}"][f"{REACTION}"]["users"] != 0:
                    if USER in data[f"{POLL}"][f"{REACTION}"]["users"] and reacted == False:
                        # print(REACTION, ANSWER)
                        if REACTION == ANSWER:
                            data3[f"{POLL}"] = 0
                        else:
                            data3[f"{POLL}"] = 1
                        reacted = True
            if reacted == False:
                data3[f"{POLL}"] = 3
            reacted = False
    return data3
async def read_file(file):
    with open(f"./data/{file}.json") as f:
        data = json.load(f)
    return data

"""
2-Year Anniversary
"""
DB_PATH_2Year = "../2year.db"

def check_entry_existence_year2(userid: int):
    DB = sqlite3.connect(DB_PATH_2Year)
    cursor = DB.cursor()
    result = cursor.execute(f"SELECT USERID FROM USER_DATA WHERE USERID = {userid}").fetchone()
    cursor.close()
    DB.close()
    return result



class stats_(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

class year1(discord.app_commands.Group):
    ...

year1_commands = year1(name="year1", description="Anniversary Stats")

@year1_commands.command(description="Get your Stats for the first anniversary")
async def stats(interaction: discord.Interaction, advanced: Literal["True", "False"], user: discord.User=None):
    user = interaction.user if user == None else user
    stats = await read_file("stats")
    desc = ""
    text = ""
    if user.id not in stats["1-year-anniversary"]["participants"]:
        return await interaction.response.send_message(f"{user.name} did not participate in the 1-Year Anniversary. There are no stats for your ID.")
    desc = f"{user.name} participated for the following Visions:\n\n"
    for VISION in stats["1-year-anniversary"][f"{user.id}"]["team"]:
        emoji = VISION_EMOJIS[f"{VISION}"]
        if VISION != "Unknown":
            desc += f"{emoji} {VISION}\n"
        else:
            desc += f"{emoji}\n"
    polls = stats["1-year-anniversary"][f"{user.id}"]["polls"]
    correct_answers = stats["1-year-anniversary"][f"{user.id}"]["correct_answers"]
    wrong_answers = stats["1-year-anniversary"][f"{user.id}"]["wrong_answers"]
    dismissed_votes = stats["1-year-anniversary"][f"{user.id}"]["dismissed_answers"]
    if advanced == "True":
        percent_correct = (correct_answers/polls)*100
        percent_wrong = (wrong_answers/polls)*100
        percent_dismissed = (dismissed_votes/polls)*100
        desc += f"\nYou voted in **{polls}/44** Polls. Out of **{polls}** Answers, **{correct_answers} ({round(percent_correct)}%)** were correct and **{wrong_answers} ({round(percent_wrong)}%)** not. Due to voting multiple times on a poll, **{dismissed_votes} ({round(percent_dismissed)}%)** Votes have not been counted."
    else:
        percent_correct = ""
        percent_wrong = ""
        percent_dismissed = ""
        desc += f"\nYou voted in **{polls}/44** Polls. Out of **{polls}** Answers, **{correct_answers}** were correct and **{wrong_answers}** not. Due to voting multiple times on a poll, **{dismissed_votes}** Votes have not been counted."

    first = False
    counter = 0
    embed_number = 0
    embed = discord.Embed(title="1-Year-Anniversary Stats", description=desc, color=0x00bfff)
    if advanced == "True":
        answers = await check_answers(user.id)
        for POLL in answers:
            txt = answers[f"{POLL}"]
            txt = ADVANCED_INFOS[f"{txt}"]
            text += f"{POLL} - {txt}\n"
            counter += 1
            if counter == 11:
                counter = 0
                embed_number += 1
                embed.add_field(name=f"Individual Stats Part {embed_number}", value=text, inline=True)
                text = ""
    embed.set_footer(text=user.name, icon_url=user.avatar)
    await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(stats_(client))