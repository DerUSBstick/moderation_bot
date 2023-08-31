import discord
from discord.ext import commands
import random
import datetime
import sqlite3
import time
from typing import Literal
from utils.classes import DATABASE_DIRECTORY, emojis

NEW_LEVEL_REQ = {
    '1': 0,
    '2': 375,
    '3': 500,
    '4': 625,
    '5': 725,
    '6': 850,
    '7': 950,   
    '8': 1075,
    '9': 1200,
    '10': 1300,
    '11': 1425,
    '12': 1525,
    '13': 1650,
    '14': 1775,
    '15': 1875,
    '16': 2000,
    '17': 2375,
    '18': 2500,
    '19': 2625,
    '20': 2775,
    '21': 2825,
    '22': 3425,
    '23': 3725,
    '24': 4000,
    '25': 4300,
    '26': 4575,
    '27': 4875,
    '28': 5150,
    '29': 5450,
    '30': 5725,
    '31': 6025,
    '32': 6300,
    '33': 6600,
    '34': 6900,
    '35': 7175,
    '36': 7475,
    '37': 7750,
    '38': 8050,
    '39': 8325,
    '40': 8625,
    '41': 10550,
    '42': 11525,
    '43': 12475,
    '44': 13450,
    '45': 14400,
    '46': 15350,
    '47': 16325,
    '48': 17275,
    '49': 18250,
    '50': 19200,
    '51': 26400,
    '52': 28800,
    '53': 31200,
    '54': 33600,
    '55': 36000,
    '56': 232350,
    '57': 258950,
    '58': 285750,
    '59': 312825,
    '60': 340125
}

LEVELS_AND_XP = {
    '0': 0,
    '1': 100,
    '2': 255,
    '3': 475,
    '4': 770,
    '5': 1150,
    '6': 1625,
    '7': 2205,
    '8': 2900,
    '9': 3720,
    '10': 4675,
    '11': 5775,
    '12': 7030,
    '13': 8450,
    '14': 10045,
    '15': 11825,
    '16': 13800,
    '17': 15980,
    '18': 18375,
    '19': 20995,
    '20': 23850,
    '21': 26950,
    '22': 30305,
    '23': 33925,
    '24': 37820,
    '25': 42000,
    '26': 46475,
    '27': 51255,
    '28': 56350,
    '29': 61770,
    '30': 67525,
    '31': 73625,
    '32': 80080,
    '33': 86900,
    '34': 94095,
    '35': 101675,
    '36': 109650,
    '37': 118030,
    '38': 126825,
    '39': 136045,
    '40': 145700,
    '41': 155800,
    '42': 166355,
    '43': 177375,
    '44': 188870,
    '45': 200850,
    '46': 213325,
    '47': 226305,
    '48': 239800,
    '49': 253820,
    '50': 268375,
    '51': 283475,
    '52': 299130,
    '53': 315350,
    '54': 332145,
    '55': 349525,
    '56': 367500,
    '57': 386080,
    '58': 405275,
    '59': 425095,
    '60': 445550,
    '61': 466650,
    '62': 488405,
    '63': 510825,
    '64': 533920,
    '65': 557700,
    '66': 582175,
    '67': 607355,
    '68': 633250,
    '69': 659870,
    '70': 687225,
    '71': 715325,
    '72': 744180,
    '73': 773800,
    '74': 804195,
    '75': 835375,
    '76': 867350,
    '77': 900130,
    '78': 933725,
    '79': 968145,
    '80': 1003400,
    '81': 1039500,
    '82': 1076455,
    '83': 1114275,
    '84': 1152970,
    '85': 1192550,
    '86': 1233025,
    '87': 1274405,
    '88': 1316700,
    '89': 1359920,
    '90': 1404075,
    '91': 1449175,
    '92': 1495230,
    '93': 1542250,
    '94': 1590245,
    '95': 1639225,
    '96': 1689200,
    '97': 1740180,
    '98': 1792175,
    '99': 1845195,
    '100': 1899250
}

async def check_level_up(self, LEVEL, EXP, CHATMONEY):
    if NEW_LEVEL_REQ[f'{LEVEL+1}'] < EXP:
        return LEVEL+1, EXP-NEW_LEVEL_REQ[f'{LEVEL+1}'], True, CHATMONEY+150
    return LEVEL, EXP, False, CHATMONEY


def get_level(USERID):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    USERDATA = list(cursor.execute(f"SELECT * FROM USERS WHERE USER_ID = {USERID}"))
    cursor.close()
    db.close()
    level, exp = USERDATA[0][2], USERDATA[0][1]
    return level, exp
def get_balance(USERID):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    BALANCE = list(cursor.execute(f"SELECT BALANCE FROM USERS WHERE USER_ID = {USERID}"))[0][0]
    cursor.close()
    db.close()
    return BALANCE

class level_system(commands.Cog):
    def __init__(self, client):
        self.client = client
    @discord.app_commands.command()
    async def level(self, interaction: discord.Interaction):
        LEVEL, EXP = get_level(interaction.user.id)
        next_level_exp = NEW_LEVEL_REQ[f"{int(LEVEL)+1}"]
        percentage = round(int(EXP)/next_level_exp*100, 2)
        embed = discord.Embed(title=f"{interaction.user.display_name} Level", description=f"Level: {LEVEL}\nEXP: {int(EXP)}/{next_level_exp} ({percentage}%)")
        #embed.set_footer(text="Gaining EXP is currently paused.")
        return await interaction.response.send_message(embed=embed)
    @discord.app_commands.command()
    async def balance(self, interaction):
        BALANCE = get_balance(interaction.user.id)
        return await interaction.response.send_message(f"Your Balance is {BALANCE} {emojis.mora}")
    @discord.app_commands.command()
    async def notifications(self, interaction: discord.Interaction, setting: Literal["Server", "DM", "Disabled"]):
        db = sqlite3.connect(DATABASE_DIRECTORY)
        cursor = db.cursor()
        notification_state = cursor.execute(f"SELECT NOTIFICATIONS FROM USERS WHERE USER_ID = {interaction.user.id}").fetchone()
        print(setting, notification_state)
        if notification_state == None:
            return await interaction.response.send_message("Send a message in Chat first to use this command", ephemeral=True)
        cursor.execute(f"UPDATE USERS SET NOTIFICATIONS = '{setting.upper()}' WHERE USER_ID = {interaction.user.id}")
        db.commit()
        cursor.close()
        db.close()
        return await interaction.response.send_message(f"Notification Setting has been changed to {setting}")
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        valid_channels = [1064625936638672998, 854733975977197568, 854733975977197570, 1078707782955573319]
        def _check(m):
            return (m.author == message.author
                    and len(m.content)
                    and (datetime.datetime.now() - m.created_at).seconds < 3)
        if not message.author.bot and message.channel.id in valid_channels:
            #if len(list(filter(lambda m: _check(message), self.client.cached_messages))) <= 1:
                db = sqlite3.connect(DATABASE_DIRECTORY)
                cursor = db.cursor()
                USER_ID = cursor.execute(f"SELECT USER_ID FROM USERS WHERE USER_ID = {message.author.id}").fetchone()
                if USER_ID == None:
                    sq = (f'INSERT INTO USERS(USER_ID, LEVEL, EXP, BALANCE, NOTIFICATIONS, REQUESTS_BL, COUNTING, GLOBAL_BLACKLIST) VALUES(?,?,?,?,?,?,?,?)')
                    va = (message.author.id, 1, 1, 1, "SERVER", "False", 0, "False")
                    cursor.execute(sq, va)
                    db.commit()
                    cursor.close()
                    db.close()
                    return
                balance = cursor.execute(f"SELECT BALANCE FROM USERS WHERE USER_ID = {message.author.id}").fetchone()[0]
                level = cursor.execute(f"SELECT LEVEL FROM USERS WHERE USER_ID = {message.author.id}").fetchone()[0]
                exp = cursor.execute(f"SELECT EXP FROM USERS WHERE USER_ID = {message.author.id}").fetchone()[0]
                notification_state = cursor.execute(f"SELECT NOTIFICATIONS FROM USERS WHERE USER_ID = {message.author.id}").fetchone()[0]
                multiplier = 1
                if time.time() < 1682190000:
                    multiplier = 2
                exp += (random.randint(5,20)*multiplier)
                balance += random.randint(1, 5)
                level, exp, level_up, balance = await check_level_up(self, level, exp, balance)
                cursor.execute(f"UPDATE USERS SET BALANCE = {balance} WHERE USER_ID = {message.author.id}")
                cursor.execute(f"UPDATE USERS SET LEVEL = {level} WHERE USER_ID = {message.author.id}")
                cursor.execute(f"UPDATE USERS SET EXP = {exp} WHERE USER_ID = {message.author.id}")
                db.commit()
                cursor.close()
                db.close()
                if level_up:
                    if notification_state == "SERVER":
                        await message.reply(f"You leveled up to LVL {level}")
                    elif notification_state == "DM":
                        try:
                            await message.author.send(f"You leveled up to LVL {level}")
                        except:
                            pass
async def setup(client):
    await client.add_cog(level_system(client))