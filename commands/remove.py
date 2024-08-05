import discord
from discord.ext import commands
from discord import app_commands
from config import global_state

class RemoveDropdown(discord.ui.Select):
    def __init__(self, ctx):
        music_queue = global_state.music_queue
        options = [
            discord.SelectOption(label=f"{idx+1}. {track['title']}", description=f"Requested by {track['requester']}")
            for idx, track in enumerate(music_queue)
        ]
        super().__init__(placeholder="Select a track to remove...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        music_queue = global_state.music_queue
        idx = int(self.values[0].split(".")[0]) - 1
        removed_track = music_queue.pop(idx)
        await interaction.response.send_message(f"Removed **{removed_track['title']}** from the queue.")
        global_state.music_queue = music_queue

class RemoveView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(RemoveDropdown(ctx))

@commands.hybrid_command(name='remove', description='Removes a track from the queue')
async def remove(ctx: commands.Context):
    """Removes a track from the queue"""
    if ctx.voice_client is None or ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("You are not in the same voice channel as the bot.")
        return

    music_queue = global_state.music_queue
    if len(music_queue) == 0:
        await ctx.send("The queue is empty.")
    else:
        await ctx.send("Select a track to remove from the queue:", view=RemoveView(ctx))

def setup(bot):
    bot.add_command(remove)

