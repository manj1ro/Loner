import discord
from discord.ext import commands
from config.play_next import play_next
from config import global_state

@commands.hybrid_command(name='skip', description='Skips the current track')
async def skip(ctx: commands.Context):
    """Skips the current track"""
    music_queue = global_state.music_queue

    if ctx.voice_client is None:
        await ctx.send("Not connected to a voice channel.")
        return

    if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("You are not in the same voice channel as the bot.")
        return

    if not ctx.voice_client.is_playing():
        await ctx.send("Not playing any music right now.")
        return

    try:
        ctx.voice_client.stop()  # This will trigger the after function to call play_next

        if music_queue:
            next_track = music_queue[0]
            await ctx.send(f"Skipped the current track. Now playing: {next_track['title']}")
        else:
            await ctx.send("Skipped the current track. The queue is empty.")
            global_state.current_track = None

    except Exception as e:
        try:
            await ctx.send(f"An error occurred while trying to skip the track: {str(e)}")
        except discord.errors.NotFound:
            await ctx.channel.send(f"An error occurred while trying to skip the track: {str(e)}")

    global_state.music_queue = music_queue

def setup(bot):
    bot.add_command(skip)

