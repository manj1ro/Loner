import discord
from discord.ext import commands
from config.embeds import create_help_embed

@commands.hybrid_command(name='bot-help', description='Shows this help message')
async def Help_command(ctx: commands.Context):
    """Shows this help message"""
    embed = create_help_embed(ctx.bot)
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(Help_command)
