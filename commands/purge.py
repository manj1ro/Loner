import discord
from discord.ext import commands
from discord import app_commands
import asyncio

@commands.hybrid_command(name='purge', description='Deletes a specified number of messages from the channel')
@commands.has_permissions(manage_messages=True)
@app_commands.describe(amount="The number of messages to delete")
async def purge(ctx: commands.Context, amount: int):
    """Deletes a specified number of messages from the channel"""
    await ctx.defer()  # Deferring the response to avoid interaction timeout

    if amount < 1:
        await ctx.send("The number of messages to delete must be greater than 0.", delete_after=5)
        return

    try:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)} messages deleted.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("I do not have permission to delete messages.", delete_after=5)
    except discord.NotFound:
        await ctx.send("Some messages to delete were not found.", delete_after=5)
    except discord.HTTPException as e:
        if e.status == 429:  # Rate limit handling
            retry_after = int(e.headers.get('Retry-After', 1))
            await ctx.send(f"Rate limited. Retrying in {retry_after} seconds.", delete_after=5)
            await asyncio.sleep(retry_after)
            await purge(ctx, amount)  # Retry the command
        else:
            await ctx.send(f"Failed to delete messages: {str(e)}", delete_after=5)
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {str(e)}", delete_after=5)

def setup(bot):
    bot.add_command(purge)

