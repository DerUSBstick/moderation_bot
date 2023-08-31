import discord
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, NoEntryPointError, AutoShardedBot
from typing import Literal
import time, json, sqlite3
import os
import random
import logging
import traceback, sys
from utils.classes import BOT_OWNER_ID, DATABASE_DIRECTORY

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logfile.log'),
    ]
)
#console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

prefix = ">"
intents = discord.Intents(
        presences=True,
		guilds=True,
		members=True,
		messages=True,
		message_content=True
	)

start = time.time()

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
#bot = AutoShardedBot(command_prefix=prefix, case_insensitive=True, intents=intents)
# bot.shard_count = 2

@bot.event
async def on_ready():
    # 2 Year Commands
    from cogs.year2_anniversary import year2_commands
    bot.tree.add_command(year2_commands)
    # 1 Year Commands
    from cogs.year1_anniversary import year1_commands
    bot.tree.add_command(year1_commands)
    
    await load_cogs_on_startup()
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

async def load_cogs_on_startup():
    for filename in os.listdir('./cogs'):
        LOAD_ON_START = ["welcome", "status", "shop", "requests",
                         "moderator", "level_system", "leaderboard",
                         "general", "EvalCMD", "dev",
                         "applications", "year2_anniversary", "year1_anniversary"]
        if filename.endswith('.py') and filename[:-3] in LOAD_ON_START:
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} loaded")
            except Exception as error:
                if isinstance(error, NoEntryPointError):
                    print("Extension has no Setup Function")
                if isinstance(error, ExtensionFailed):
                    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot.run("TOKEN", log_handler=console_handler)