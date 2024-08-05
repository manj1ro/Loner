import discord

async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    activity = discord.Game(name="DM !invite")
    await bot.change_presence(activity=activity)

def setup(bot_instance):
    global bot
    bot = bot_instance
    bot.add_listener(on_ready)



