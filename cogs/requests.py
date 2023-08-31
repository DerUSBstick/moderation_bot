import discord
from discord.ext import commands
import json
import sqlite3
from utils.classes import DATABASE_DIRECTORY, GUILD

EMBED_IMAGES_DENIED = 958047463179169842
PHOTO_PERMISSIONS = 995108752040656929
LOG_CHANNEL = 1076977135610232942
REQUESTS_CHANNEL = 996112049602035832

class requests(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == REQUESTS_CHANNEL and not message.author.bot:
            if message.content.lower() == "photos":
                await photos_request(self, message.author, message.channel)
            else:
                await nickname_request(self, message.author, message.channel, message.content)
            await message.delete()
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.command == None:
            if interaction.data["custom_id"].startswith("requests."):
                CUSTOM_ID = interaction.data["custom_id"]
                await handle_request(self, CUSTOM_ID.split("."), interaction.user.id)
                await interaction.response.send_message("Interaction has been handled!", ephemeral=True)
        #await interaction.response.send_message(f"Data: {interaction.data}\nExtras: {interaction.extras}\nTrigger: {interaction.user}\nClient: {interaction.client.user}")

async def send_success_message(self):
    channel = self.client.get_channel(REQUESTS_CHANNEL)
    await channel.send("Your Request has been send to Staff for Approval", delete_after=7)

async def handle_request(self, DATA, MODERATORID):
    ACTION = DATA[3]
    STATUS = DATA[2]
    CASEID = DATA[1]
    update_database_entry(CASEID, MODERATORID, STATUS)
    DB_DATA = get_database_entry(CASEID)
    if STATUS == "approve":
        if ACTION == "photos":
            await add_role(self, DB_DATA[1])
        if ACTION == "nickname":
            await edit_nickname(self, DB_DATA[1], DB_DATA[5])
    elif STATUS == "blacklist":
        blacklist_user(DB_DATA[1])
    if STATUS != "ignore":
        try:
            await inform_user(self, DB_DATA[1], STATUS)
        except:
            pass
    await update_message(self, CASEID)

async def update_message(self, CASEID):
    DATA = get_database_entry(CASEID)
    CHANNEL = self.client.get_guild(GUILD).get_channel(1076977135610232942)
    MESSAGE = await CHANNEL.fetch_message(DATA[3])
    USER = self.client.get_user(DATA[1])
    embed = discord.Embed()
    if DATA[4] == "photos":
        embed = discord.Embed(description=f"{USER} ({USER.id} {USER.mention})\nStatus: ``{DATA[6]}``")
    elif DATA[4] == "nickname":
        embed = discord.Embed(description=f"{USER} ({USER.id} {USER.mention})\nNickname: {DATA[5]}\nStatus: ``{DATA[6]}``")
    embed.set_footer(text=f"ID: {str(CASEID).zfill(3)}")
    view = get_buttons(CASEID, True, DATA[4])
    await MESSAGE.edit(embed=embed, view=view)
    return DATA
async def nickname_request(self, USER: discord.User, CHANNEL, NICKNAME):
    if check_blacklist(USER):
        return await CHANNEL.send("You can't request a new nickname", delete_after=5)
    if len(NICKNAME) > 32:
        return await CHANNEL.send("Your Nickname can't be longer than 32 Characters", delete_after=5)
    CASEID = create_database_entry(USER.id, "nickname", NICKNAME)
    view = get_buttons(CASEID, False, "nickname")
    embed = discord.Embed(description=f"{USER} ({USER.id} {USER.mention})\nNickname: {NICKNAME}\nStatus: ``waiting for response``")
    embed.set_footer(text=f"ID: {str(CASEID).zfill(3)}")
    log_channel = CHANNEL.guild.get_channel(LOG_CHANNEL)
    message = await log_channel.send("Nickname Request", view=view, embed=embed)
    update_message_id(message.id, CASEID)
    await send_success_message(self)
async def photos_request(self, USER: discord.User, CHANNEL):
    if check_photos_eligibility(self, USER):
        return await CHANNEL.send("You can't request Permissions to send photos", delete_after=5)
    CASEID = create_database_entry(USER.id, "photos")
    view = get_buttons(CASEID, False, "photos")
    embed = discord.Embed(description=f"{USER} ({USER.id} {USER.mention})\nStatus: ``waiting for response``")
    embed.set_footer(text=f"ID: {str(CASEID).zfill(3)}")
    log_channel = CHANNEL.guild.get_channel(LOG_CHANNEL)
    message = await log_channel.send("Photo Permissions Request", view=view, embed=embed)
    update_message_id(message.id, CASEID)
    await send_success_message(self)

def get_buttons(CASEID, DISABLED, ACTION):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label="Approve", disabled=DISABLED, custom_id=f"requests.{CASEID}.approve.{ACTION}"))
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.red, label="Deny", disabled=DISABLED, custom_id=f"requests.{CASEID}.deny.{ACTION}"))
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="Ignore", disabled=DISABLED, custom_id=f"requests.{CASEID}.ignore.{ACTION}"))
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.gray, label="Blacklist", disabled=DISABLED, custom_id=f"requests.{CASEID}.blacklist.{ACTION}"))
    return view
def create_database_entry(USERID, ACTION, NICKNAME=None):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    CURRENT_ID = int(cursor.execute('SELECT SETTING FROM CONFIG WHERE MODULE IS "REQUESTS"').fetchone()[0])
    cursor.execute("UPDATE CONFIG SET SETTING = ? WHERE MODULE = ?", (f"{CURRENT_ID+1}", "REQUESTS"))
    if ACTION == "photos":
        cursor.execute("INSERT INTO REQUESTS(CASEID, USERID, ACTION, STATUS) VALUES(?,?,?,?)", (CURRENT_ID, USERID, ACTION, "waiting"))
    elif ACTION == "nickname":
        cursor.execute("INSERT INTO REQUESTS(CASEID, USERID, ACTION, NICKNAME, STATUS) VALUES(?,?,?,?,?)", (CURRENT_ID, USERID, ACTION, NICKNAME, "waiting"))
    cursor.close()
    db.commit()
    db.close()
    return CURRENT_ID
def update_database_entry(CASEID, MODERATORID, STATUS):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    cursor.execute("UPDATE REQUESTS SET MODERATORID = ? WHERE CASEID = ?", (MODERATORID, CASEID))
    cursor.execute("UPDATE REQUESTS SET STATUS = ? WHERE CASEID = ?", (STATUS, CASEID))
    cursor.close()
    db.commit()
    db.close()
def get_database_entry(CASEID):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM REQUESTS WHERE CASEID = {CASEID}")
    DATA = cursor.fetchone()
    cursor.close()
    db.close()
    return DATA
def update_message_id(MESSAGEID, CASEID):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    cursor.execute("UPDATE REQUESTS SET MESSAGEID = ? WHERE CASEID = ?", (MESSAGEID, CASEID))
    cursor.close()
    db.commit()
    db.close()
def check_photos_eligibility(self, USER):
    if check_blacklist(USER) or check_permission_denied(self, USER):
        return True
    return False
def check_permission_denied(self, USER):
    guild = get_guild(self)
    role = guild.get_role(EMBED_IMAGES_DENIED)
    if role in USER.roles:
        return True
    return False
def check_blacklist(USER):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    blacklist_state = cursor.execute(f"SELECT REQUESTS_BL FROM USERS WHERE USER_ID = {USER.id}").fetchone()
    cursor.close()
    db.close()
    if blacklist_state == None:
        create_main_database_entry(USER.id)
        return False
    if blacklist_state[0] == "False":
        return False
    return True
def create_main_database_entry(USERID):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    cursor.execute("INSERT INTO USERS(USER_ID, LEVEL, EXP, BALANCE, NOTIFICATIONS, REQUESTS_BL, COUNTING, GLOBAL_BLACKLIST) VALUES(?,?,?,?,?,?,?,?)", (USERID, 1, 1, 1, "SERVER", "False", 0, "False"))
    cursor.close()
    db.commit()
    db.close()
async def edit_nickname(self, USER, NICKNAME):
    guild = get_guild(self)
    USER = await guild.fetch_member(USER)
    await USER.edit(nick=NICKNAME)
async def add_role(self, USER):
    guild = get_guild(self)
    role = guild.get_role(995108752040656929)
    USER = await guild.fetch_member(USER)
    await USER.add_roles(role)
def blacklist_user(USERID):
    db = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = db.cursor()
    cursor.execute("UPDATE USERS SET REQUESTS_BL = ? WHERE USER_ID = ?", (1, USERID))
    cursor.close()
    db.commit()
    db.close()
async def inform_user(self, USERID, STATUS):
    guild = get_guild(self)
    USER = await guild.fetch_member(USERID)
    await USER.send(f"Your Request Status has been updated: {STATUS}")
def get_guild(self):
    return self.client.get_guild(GUILD)

async def setup(client):
    await client.add_cog(requests(client))