import discord

def create_now_playing_embed(track):
    embed = discord.Embed(title="Now Playing", description=f"[{track['title']}]({track['url']})", color=discord.Color.green())
    embed.add_field(name="Requested by", value=track['requester'])
    return embed

def create_added_to_queue_embed(track):
    embed = discord.Embed(title="Added to Queue", description=f"[{track['title']}]({track['url']})", color=discord.Color.blue())
    embed.add_field(name="Requested by", value=track['requester'])
    return embed

def create_queue_embed(queue):
    embed = discord.Embed(title="Music Queue", color=discord.Color.blue())
    for idx, track in enumerate(queue):
        embed.add_field(name=f"{idx+1}. {track['title']}", value=f"Requested by {track['requester']}", inline=False)
    return embed

def create_help_embed(bot):
    embed = discord.Embed(title="Help", description="List of available commands", color=discord.Color.gold())
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.description or "No description available", inline=False)
    return embed

