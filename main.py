import subprocess
import sys
import asyncio
import importlib
import pkgutil
import logging

logging.basicConfig(level=logging.INFO)

subprocess.check_call([sys.executable, "dependencies.py"])

import discord
from discord.ext import commands
from config import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, description='Music bot', intents=intents)

async def load_extensions():
    event_package = 'events'
    logging.info(f'Loading events from: {event_package}')
    for _, module_name, _ in pkgutil.iter_modules([event_package]):
        logging.info(f'Loading event module: {module_name}')
        module = importlib.import_module(f'{event_package}.{module_name}')
        if hasattr(module, 'setup'):
            module.setup(bot)
        else:
            logging.warning(f'Module {module_name} does not have a setup function')

    command_package = 'commands'
    logging.info(f'Loading commands from: {command_package}')
    for _, module_name, _ in pkgutil.iter_modules([command_package]):
        logging.info(f'Loading command module: {module_name}')
        module = importlib.import_module(f'{command_package}.{module_name}')
        if hasattr(module, 'setup'):
            module.setup(bot)
        else:
            logging.warning(f'Module {module_name} does not have a setup function')

async def sync_commands():
    try:
        await bot.tree.sync()
        logging.info("Slash commands synced globally.")
    except Exception as e:
        logging.error(f"Failed to sync commands: {e}")

@bot.event
async def on_ready():
    logging.info(f'Connected')
    await sync_commands()

# Main function
async def main():
    try:
        await load_extensions()  # Load extensions and commands
        await bot.start(config.DISCORD_TOKEN)  # Start the bot
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
