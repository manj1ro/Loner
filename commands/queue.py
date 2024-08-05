import discord
from discord.ext import commands
from config import global_state
from config.embeds import create_queue_embed

@commands.hybrid_command(name='queue', description='Shows the current music queue')
async def queue(ctx: commands.Context):
    """Shows the current music queue"""
    music_queue = global_state.music_queue
    if len(music_queue) == 0:
        await ctx.send("The queue is empty.")
    else:
        embed = create_queue_embed(music_queue)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(queue)
