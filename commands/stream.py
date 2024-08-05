import discord
from discord.ext import commands
from discord import app_commands
from config import global_state
from config.embeds import create_now_playing_embed, create_added_to_queue_embed
from config.ytdl import YTDLSource
from config.play_next import play_next
import asyncio

@commands.hybrid_command(name='stream', description='Streams from a URL (same as yt, but doesn\'t predownload)')
async def stream(ctx: commands.Context, *, url: str):
    """Streams from a URL (same as yt, but doesn't predownload)"""
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return
    elif ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("You are not in the same voice channel as the bot.")
        return

    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(url, loop=ctx.bot.loop, stream=True)
            track_info = {'title': player.title, 'requester': ctx.author.name, 'url': url}

            if ctx.voice_client.is_playing() or global_state.music_queue:
                global_state.music_queue.append(track_info)
                await ctx.send(embed=create_added_to_queue_embed(track_info))
            else:
                global_state.current_track = track_info
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop).result())
                await ctx.send(embed=create_now_playing_embed(global_state.current_track))

        except commands.CommandInvokeError as e:
            await ctx.send(f'An error occurred: {str(e)}')

def setup(bot):
    bot.add_command(stream)

