import discord
from discord.ext import commands
import json
from typing import Literal
import datetime, time
from cogs.level_system import get_level

class ApplicationModal_Event(discord.ui.Modal, title="Event Manager Applications"):
    age_input = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What's your age?",
        min_length=2,
        max_length=2,
        required=True,
        placeholder="You need to be atleast 13 to apply"
    )
    timezone = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What's your Timezone?",
        max_length=25,
        required=True
    )
    previous_experience = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Previous Experience and hosted Events",
        min_length=30,
        max_length=500,
        required=True
    )
    strength_and_weakness = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Strengths and Weaknesses",
        min_length=60,
        max_length=500
    )
    qualifications = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="What qualifies you for this position?",
        min_length=60,
        max_length=500
    )
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Event Manager Application by {interaction.user}", description=f"What's your Age?\n```{self.age_input}```\n\nWhat's your Timezone?\n```{self.timezone}```\n\nPrevious Experience and hosted Events\n```{self.previous_experience}```\n\nStrengths and Weaknesses\n```{self.strength_and_weakness}```\n\nWhat qualifies you for this position?\n```{self.qualifications}```")
        embed.set_footer(text=f"{interaction.user.id}")
        embed.timestamp = datetime.datetime.now()
        channel = interaction.client.get_channel(985385287314206730)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Your application has been submitted {self.user.name}", ephemeral=True)

    # async def on_error(self, interaction: discord.Interaction, error : Exception):
    #     print(error)
class ApplicationModal_Mod(discord.ui.Modal, title="Moderator Applications"):
    age_input = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What's your age?",
        min_length=2,
        max_length=2,
        required=True,
        placeholder="You need to be atleast 13 to apply"
    )
    timezone = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What's your Timezone?",
        max_length=25,
        required=True
    )
    previous_experience = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Previous Experience and Incidents",
        min_length=30,
        max_length=500,
        required=True
    )
    strength_and_weakness = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Strengths and Weaknesses",
        min_length=60,
        max_length=500
    )
    qualifications = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="What qualifies you for this position?",
        min_length=60,
        max_length=500
    )
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Moderator Application by {interaction.user}", description=f"What's your Age?\n```{self.age_input}```\n\nWhat's your Timezone?\n```{self.timezone}```\n\nPrevious Experience and hosted Events\n```{self.previous_experience}```\n\nStrengths and Weaknesses\n```{self.strength_and_weakness}```\n\nWhat qualifies you for this position?\n```{self.qualifications}```")
        embed.set_footer(text=f"{interaction.user.id}")
        embed.timestamp = datetime.datetime.now()
        channel = interaction.client.get_channel(985385287314206730)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Your application has been submitted {self.user.name}", ephemeral=True)

    # async def on_error(self, interaction: discord.Interaction, error : Exception):
    #     print(error)
class ApplicationModal_Admin(discord.ui.Modal, title="Admin Applications"):
    age_input = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What's your age?",
        min_length=2,
        max_length=2,
        required=True,
        placeholder="You need to be atleast 13 to apply"
    )
    timezone = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What's your Timezone?",
        max_length=25,
        required=True
    )
    previous_experience = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Previous Experience and Incidents",
        min_length=30,
        max_length=500,
        required=True
    )
    strength_and_weakness = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Strengths and Weaknesses",
        min_length=60,
        max_length=500
    )
    qualifications = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="What qualifies you for this position?",
        min_length=60,
        max_length=500
    )
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Admin Application by {interaction.user}", description=f"What's your Age?\n```{self.age_input}```\n\nWhat's your Timezone?\n```{self.timezone}```\n\nPrevious Experience and hosted Events\n```{self.previous_experience}```\n\nStrengths and Weaknesses\n```{self.strength_and_weakness}```\n\nWhat qualifies you for this position?\n```{self.qualifications}```")
        embed.set_footer(text=f"{interaction.user.id}")
        embed.timestamp = datetime.datetime.now()
        channel = interaction.client.get_channel(985385287314206730)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Your application has been submitted {self.user.name}", ephemeral=True)

    # async def on_error(self, interaction: discord.Interaction, error : Exception):
    #     print(error)

class requirements():
    def event_mananger(user: discord.Member) -> bool:
        #return True
        level = get_level(user.id)
        if level[0] < 5:
            return False
        if datetime.datetime.fromisoformat(f"{user.created_at}").timestamp() > time.time()-31104000: #1 Year
            return False
        return True
        if datetime.datetime.fromisoformat(f"{user.joined_at}").timestamp() > time.time()-2592000: #1 Month
            return False
        return True
    def moderator(user: discord.Member) -> bool:
        #return True
        level = get_level(user.id)
        if level[0] < 5:
            return False
        if datetime.datetime.fromisoformat(f"{user.created_at}").timestamp() > time.time()-62208000: #2 Years
            return False
        return True
        if datetime.datetime.fromisoformat(f"{user.joined_at}").timestamp() > time.time()-7776000: #3 Months
            return False
        return True
    def admin(user: discord.Member) -> bool:
        #return True
        level = get_level(user.id)
        if level[0] < 20:
            return False
        if datetime.datetime.fromisoformat(f"{user.created_at}").timestamp() > time.time()-93312000: #3 Years
            return False
        return True
        if datetime.datetime.fromisoformat(f"{user.joined_at}").timestamp() > time.time()-15552000: #6 Months
            return False
        return True

class annivesary(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if isinstance(interaction.type, type(discord.InteractionType.component)) and interaction.command == None:
            if interaction.data["custom_id"] == "application_Event":
                if not requirements.event_mananger(interaction.user):
                    return await interaction.response.send_message("You don't meet all requirements", ephemeral=True)
                application_modal = ApplicationModal_Event()
                application_modal.user = interaction.user
                await interaction.response.send_modal(application_modal)
            elif interaction.data["custom_id"] == "application_Moderator":
                if not requirements.moderator(interaction.user):
                    return await interaction.response.send_message("You don't meet all requirements", ephemeral=True)
                application_modal = ApplicationModal_Mod()
                application_modal.user = interaction.user
                await interaction.response.send_modal(application_modal)
            elif interaction.data["custom_id"] == "application_Admin":
                if not requirements.admin(interaction.user):
                    return await interaction.response.send_message("You don't meet all requirements", ephemeral=True)
                application_modal = ApplicationModal_Admin()
                application_modal.user = interaction.user
                await interaction.response.send_modal(application_modal)
    # @discord.app_commands.command()
    # async def apply(self, interaction: discord.Interaction):
    #     application_modal = ApplicationModal()
    #     application_modal.user = interaction.user
    #     await interaction.response.send_modal(application_modal)
    
async def setup(client):
    await client.add_cog(annivesary(client))