import discord
from discord.ext import commands
from discord import app_commands
from config import global_state

@commands.hybrid_command(name='stop', description='Stops and disconnects the bot from voice')
async def stop(ctx: commands.Context):
    """Stops and disconnects the bot from voice"""
    if ctx.voice_client is None or ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("You are not in the same voice channel as the bot.")
        return

    await ctx.voice_client.disconnect()
    global_state.current_track = None
    await ctx.send("Disconnected from the voice channel.")

def setup(bot):
    bot.add_command(stop)

