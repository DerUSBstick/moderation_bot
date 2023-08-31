import random, sys
from traceback import print_exception
from discord.ext import commands

WELCOME_MESSAGES:list = [
                "{m} joined the party.",
                "Glad you're here, {m}",
                "{m} just joined. Everyone, look busy!",
                "A wild {m} has appeared.",
                "Brace yourselves. {m} just joined the server.",
                "{m} just slid into the server.",
                "It's a bird! It's a plane! Nevermind, it's just {m}",
                "Never gonna give {m} up. Never gonna let {m} down.",
                "Hey! Listen! {m} has joined!",
                "We've been expecting you {m}.",
                "Welcome, {m}. We hope you brought pizza.",
                "Heyo, {m} deserve a warming welcome!",
                "{m} is here finally so bring the pizza over everyone!",
                "{m}! Thank you for coming!",
                "{m} has come on to the stage, give them some applause."
                ]
WELCOME_MESSAGE_CHANNEL_ID = 854733975977197568
WELCOME_SERVER_ID = 854733975197188108

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == WELCOME_SERVER_ID:
            channel = self.client.get_channel(WELCOME_MESSAGE_CHANNEL_ID)
            response = random.choice(WELCOME_MESSAGES).replace("{m}", f"{member.mention}")
            await channel.send(response)
async def setup(client):
    await client.add_cog(welcome(client))