import discord
from discord import app_commands, Embed, ButtonStyle
from discord.ext import commands
from typing import Literal
import asyncio
from utils.classes import GENSHIN_REDEEM_CODE_URL, BOT_OWNER_ID, emojis

SPECIAL_PROGRAM_DISCORD_CHANNEL_ID = 1064625936638672998
SPECIAL_PROGRAM_EMBED_THUMBNAIL = "https://media.discordapp.net/attachments/886599665989079070/1136691440483831928/Emblem_Unknown.png?width=320&height=320"

async def get_application_status(client: discord.Client) -> list:
    channel = client.get_channel(1095233396386582608)
    i = 0
    messages = [
       ["Admin", 1098628888172695704],
       ["Moderator", 1098628889321934868],
       ["Event", 1098628890366316574]
       ]
    for application in messages:
        message = await channel.fetch_message(application[1])
        component_status = message.components[0].children[0].disabled
        application.append(component_status)
        i += 1
    return messages

async def get_buttons(client: discord.Client, disabled: bool) -> discord.ui.View:
    application_status = await get_application_status(client)
    view = discord.ui.View()
    for application in application_status:
        id = application[0].replace(" ", "_")
        view.add_item(discord.ui.Button(label=application[0], style=discord.ButtonStyle.red if application[2] else discord.ButtonStyle.green, disabled=disabled, custom_id=f"dev_config_applications_{id}"))
    return view

class dev(commands.Cog):
    def __init__(self, client):
        self.client = client
    @discord.app_commands.command()
    async def config(self, interaction: discord.Interaction, config: Literal["Applications"]):
        access = [585834029484343298, 611133795743170563]
        if interaction.user.id not in access:
            return await interaction.response.send_message("You can't use this command!")
        view = await get_buttons(self.client, False)
        await interaction.response.send_message(view=view)
        await asyncio.sleep(60)
        view = await get_buttons(self.client, True)
        await interaction.edit_original_response(view=view)
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if isinstance(interaction.type, type(discord.InteractionType.component)) and interaction.command == None:
            if interaction.data["custom_id"].startswith("dev_config_applications_"):
                access = [585834029484343298, 611133795743170563]
                if interaction.user.id not in access:
                    return await interaction.response.send_message("You can't use this command")
                await interaction.response.defer(thinking=True)
                role = interaction.data["custom_id"].split("_")[3]
                application_data = await get_application_status(self.client)
                for data in application_data:
                    if data[0] == role:
                        message = await self.client.get_channel(1095233396386582608).fetch_message(data[1])
                        view = discord.ui.View()
                        view.add_item(discord.ui.Button(label="Apply", custom_id=f"application_{role}", disabled=not data[2]))
                        await message.edit(view=view)
                buttons = await get_buttons(self.client, False)
                await interaction.message.edit(view=buttons)
                await interaction.followup.send("Interaction has been handled")
    @discord.app_commands.command()
    async def special_program(self, interaction, everyone_ping: Literal["True", "False"], channel: discord.TextChannel, image_url: str, version: str, code1: str, code2: str, code3: str):
        if interaction.user.id != BOT_OWNER_ID:
            return interaction.response.send_message("You can't use this command!")
        #channel = self.client.get_channel(SPECIAL_PROGRAM_DISCORD_CHANNEL_ID)
        embed = Embed(
            color=0x1fff00,
            title=f"{version} Special Program Codes",
            description=f"[{code1}]({GENSHIN_REDEEM_CODE_URL}{code1}) 100 {emojis.primo} & 10 {emojis.mystic_ore}\n[{code2}]({GENSHIN_REDEEM_CODE_URL}{code2}) 100 {emojis.primo} & 5 {emojis.heros_wit}\n[{code3}]({GENSHIN_REDEEM_CODE_URL}{code3}) 100 {emojis.primo} & 50,000 {emojis.mora}"
        )
        embed.set_thumbnail(url=SPECIAL_PROGRAM_EMBED_THUMBNAIL)
        embed.set_image(url=image_url)
        embed.set_footer(text=f"{interaction.user.name}", icon_url=f"{interaction.user.avatar}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(style=ButtonStyle.url, label=f"{code1}", url=f"{GENSHIN_REDEEM_CODE_URL}{code1}"))
        view.add_item(discord.ui.Button(style=ButtonStyle.url, label=f"{code2}", url=f"{GENSHIN_REDEEM_CODE_URL}{code2}"))
        view.add_item(discord.ui.Button(style=ButtonStyle.url, label=f"{code3}", url=f"{GENSHIN_REDEEM_CODE_URL}{code3}"))
        await channel.send(
            content="@everyone" if everyone_ping == "True" else "everyone",
            embed=embed,
            view=view
        )
        await interaction.response.send_message("Successfully created Special Program Codes Embed")
async def setup(client):
    await client.add_cog(dev(client))