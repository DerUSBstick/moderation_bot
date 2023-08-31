import discord
from discord.ext import commands
import datetime

TEAM_ROLES = [854743362031452170, 855552156807594015, 992510272352821429, 974769105410355311, 974770032993267803]

async def check_if_team_member(self, USERID):
    guild = self.client.get_guild(854733975197188108)
    moderator = guild.get_member(USERID)
    for team_role in TEAM_ROLES:
        team_role = guild.get_role(team_role)
        if team_role in moderator.roles:
            return True
    return False

class moderator(commands.Cog):
    def __init__(self, client):
        self.client = client
    @discord.app_commands.command()
    async def imperms(self, interaction, user: discord.Member, reason: str):
        guild = self.client.get_guild(854733975197188108)
        role = guild.get_role(958047463179169842)
        user = guild.get_member(user.id)
        moderator = guild.get_member(interaction.user.id)
        if not await check_if_team_member(self, interaction.user.id):
            return await interaction.response.send_message("You can't use this command")
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"{user.mention} has been Granted Image Permissions")
        else:
            await user.add_roles(role)
            await interaction.response.send_message(f"Image Permissions have been denied for {user.mention}")
async def setup(client):
    await client.add_cog(moderator(client))