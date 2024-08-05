import discord
from discord.ext import commands
from discord import app_commands

@commands.hybrid_command(name='volume', description='Changes the player\'s volume')
async def volume(ctx: commands.Context, volume: int):
    """Changes the player's volume"""
    if ctx.voice_client is None or ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("You are not in the same voice channel as the bot.")
        return

    if volume <= 0:
        await ctx.send("Volume must be a positive number greater than 0.")
        return

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

def setup(bot):
    bot.add_command(volume)

