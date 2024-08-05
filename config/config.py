import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = commands.when_mentioned_or("!")
INVITE_URL = os.getenv('INVITE_URL')


