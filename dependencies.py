import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

all_up_to_date = True

try:
    import discord
    print("discord.py found")
except ImportError:
    install("discord.py")
    all_up_to_date = False

try:
    import yt_dlp
    print("\nyt-dlp found")
except ImportError:
    install("yt-dlp")
    all_up_to_date = False

try:
    import dotenv
    print("\npython-dotenv found")
except ImportError:
    install("python-dotenv")
    all_up_to_date = False

if all_up_to_date:
    print("\nAll dependencies are up to date.\n")

