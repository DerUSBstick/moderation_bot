from datetime import datetime
from random import choice
from discord import Member
import sqlite3

DATABASE_DIRECTORY = "../db.db"

GENSHIN_REDEEM_CODE_URL = "https://genshin.hoyoverse.com/en/gift?code="

GUILD = 854733975197188108


BOT_OWNER_ID = 585834029484343298
class emojis:
    boosts_message_emoji = "<:boosts_message:1072808800022700122>"
    primo = "<:Primogem:1072863040313229313>"
    mora = "<:Mora:1072863146835976232>"
    mystic_ore = "<:Mystic_Ore:1072863208248987659>"
    heros_wit = "<:Heros_Wit:1072863244424847360>"
    status_online = "<:status_online:1075855191485726771>"
    status_idle = "<:status_idle:1075855217947574442>"
    status_dnd = "<:status_dnd:1075855246397542420>"
    status_offline = "<:status_offline:1075855280367227073>"
    status_streaming = "<:status_streaming:1075855328345870428>"
    status_informations = "<a:bot_informations:1094310710068125788>"
    anemo = "<:element_anemo:1081651596372492288>"
    cryo = "<:element_cryo:1081651687632150588>"
    dendro = "<:element_dendro:1081651659450626161>"
    electro = "<:element_electro:1081651629536854067>"
    geo = "<:element_geo:1081651712911233074>"
    hydro = "<:element_hydro:1081651570749489194>"
    pyro = "<:element_pyro:1081651535714463864>"
    number_one = "<:number_one:1082658236118880376>"
    number_two = "<:number_two:1082658237389738087>"
    number_three = "<:number_three:1082658233728110622>"
    number_four = "<:number_four:1082658221908570143>"
    IttoBonk = "<:IttoBonk:1098492933734420570>"
    IttoConfused = "<:IttoConfused:1098492754662805524>"

class functions:
    #Converts a Unix timestamp into a Human Readable Time
    def parse_duration(self, timestamp: int):
        minutes, seconds = divmod(timestamp, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            if days > 1:
                duration.append('{} days'.format(days))
            else:
                duration.append('{} day'.format(days))
        if hours > 0:
            if hours > 1:
                duration.append('{} hours'.format(hours))
            else:
                duration.append('{} hour'.format(hours))
        if minutes > 0:
            if minutes > 1:
                duration.append('{} minutes'.format(minutes))
            else:
                duration.append('{} minute'.format(minutes))
        if seconds > 0:
            if seconds > 1:
                duration.append('{} seconds'.format(seconds))
            else:
                duration.append('{} second'.format(seconds))
        else:
            duration.append('-')

        return ', '.join(duration)
    async def convert_to_date(self, time):
        time = str(time).split(".")[0].replace("-", "/")
        result = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
        return result