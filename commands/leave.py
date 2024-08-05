import discord
from discord.ext import commands

@commands.hybrid_command(name='leave', description='Leaves the voice channel')
async def leave(ctx: commands.Context):
    """Leaves the voice channel"""
    if ctx.voice_client is None:
        await ctx.send("I am not connected to any voice channel.")
        return
    
    if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("You are not in the same voice channel as the bot.")
        return
    
    await ctx.voice_client.disconnect()
    await ctx.send("Disconnected from the voice channel.")

def setup(bot):
    bot.add_command(leave)
