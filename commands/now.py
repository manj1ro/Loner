import discord
from discord.ext import commands
from discord import app_commands
from config import global_state
from config.embeds import create_now_playing_embed

@commands.hybrid_command(name='now', description='Shows the currently playing track')
async def now(ctx: commands.Context):
    """Shows the currently playing track"""
    current_track = global_state.current_track
    if current_track:
        await ctx.send(embed=create_now_playing_embed(current_track))
    else:
        await ctx.send("No track is currently playing.")

def setup(bot):
    bot.add_command(now)

