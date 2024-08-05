import discord
from discord.ext import commands
from discord import app_commands
from config.embeds import create_added_to_queue_embed, create_now_playing_embed
from config.ytdl import YTDLSource
from config.play_next import play_next
import asyncio
from config import global_state

@commands.hybrid_command(name='play', description='Plays a file from a URL or keyword with optional audio effects')
@app_commands.choices(effect=[
    app_commands.Choice(name="Bassboost", value="bassboost"),
    app_commands.Choice(name="Slow", value="slow"),
    app_commands.Choice(name="Fast", value="fast"),
    app_commands.Choice(name="Bassboost and Slow", value="bassboost+slow"),
    app_commands.Choice(name="Bassboost and Fast", value="bassboost+fast")
])
async def play(ctx: commands.Context, query: str, effect: app_commands.Choice[str] = None):
    """Plays a file from a URL or keyword and applies optional audio effects"""
    music_queue = global_state.music_queue
    current_track = global_state.current_track

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
            effect_value = effect.value if effect else None
            player = await YTDLSource.from_url(query, loop=ctx.bot.loop, stream=True, effect=effect_value)
            track_info = {'title': player.title, 'requester': ctx.author.name, 'url': query}

            if ctx.voice_client.is_playing() or music_queue:
                music_queue.append(track_info)
                await ctx.send(embed=create_added_to_queue_embed(track_info))
            else:
                current_track = track_info
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop).result())
                await ctx.send(embed=create_now_playing_embed(current_track))

        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

    global_state.music_queue = music_queue
    global_state.current_track = current_track

def setup(bot):
    bot.add_command(play)
