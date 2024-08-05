import discord
from config.embeds import create_now_playing_embed
from config.ytdl import YTDLSource
from config import global_state
import asyncio

async def play_next(ctx):
    """Plays the next song in the queue."""
    music_queue = global_state.music_queue

    if music_queue:
        next_song = music_queue.pop(0)
        global_state.current_song = next_song

        try:
            player = await YTDLSource.from_url(next_song['url'], loop=ctx.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop))

            try:
                await ctx.send(embed=create_now_playing_embed(global_state.current_song))
            except discord.errors.NotFound:
                await ctx.channel.send(embed=create_now_playing_embed(global_state.current_song))

        except Exception as e:
            try:
                await ctx.send(f"An error occurred while trying to play the next song: {str(e)}")
            except discord.errors.NotFound:
                await ctx.channel.send(f"An error occurred while trying to play the next song: {str(e)}")
    else:
        global_state.current_song = None
        await ctx.send("The queue is empty.")
