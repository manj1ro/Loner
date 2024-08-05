import discord
from datetime import datetime, timedelta
from config import config

cooldowns = {}

async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        content = message.content.strip().lower()
        if content == '!invite':
            if message.author.id in cooldowns:
                last_used = cooldowns[message.author.id]
                if datetime.now() - last_used < timedelta(hours=1):
                    remaining_time = timedelta(hours=1) - (datetime.now() - last_used)
                    await message.channel.send(f"Please wait {remaining_time} before using this command again.")
                    return
            cooldowns[message.author.id] = datetime.now()
            await send_invite_embed(message.channel)
    await bot.process_commands(message)

async def send_invite_embed(channel):
    embed = discord.Embed(
        title="Invite Me!",
        description="Click the button below to invite me to your server.",
        color=discord.Color.blue()
    )
    button = discord.ui.Button(label="Add Bot", url=config.INVITE_URL, style=discord.ButtonStyle.primary)
    view = discord.ui.View()
    view.add_item(button)
    await channel.send(embed=embed, view=view)

def setup(bot_instance):
    global bot
    bot = bot_instance
    bot.add_listener(on_message)
