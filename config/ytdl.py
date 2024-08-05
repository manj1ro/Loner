import yt_dlp as youtube_dl
import discord
from discord.ext import commands
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

def get_ffmpeg_options(effect):
    base_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    filter_map = {
        'bassboost': 'equalizer=f=50:width_type=h:width=2:g=10',
        'slow': 'atempo=0.75',
        'fast': 'atempo=1.25',
        'bassboost+slow': 'equalizer=f=50:width_type=h:width=2:g=10,atempo=0.8',
        'bassboost+fast': 'equalizer=f=50:width_type=h:width=2:g=10,atempo=1.5'
    }

    if effect in filter_map:
        base_options['options'] = f'-vn -af {filter_map[effect]}'

    return base_options

class YTDLSource(discord.PCMVolumeTransformer):
    ytdl = ytdl

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, effect=None):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=not stream))
            if 'entries' in data:
                data = data['entries'][0]  # Take first item from a playlist

            filename = data['url'] if stream else cls.ytdl.prepare_filename(data)

            ffmpeg_options = get_ffmpeg_options(effect)
            print(f"FFmpeg options: {ffmpeg_options}")

            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except Exception as e:
            raise commands.CommandInvokeError(f'An error occurred while processing this request: {e}')
        
    @staticmethod
    def get_ffmpeg_options(effect):
        base_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        filter_map = {
            'bassboost': 'equalizer=f=50:width_type=h:width=2:g=10',
            'slow': 'atempo=0.75',
            'fast': 'atempo=1.25',
            'bassboost+slow': 'equalizer=f=50:width_type=h:width=2:g=10,atempo=0.8',
            'bassboost+fast': 'equalizer=f=50:width_type=h:width=2:g=10,atempo=1.5'
        }

        if effect in filter_map:
            base_options['options'] = f'-vn -af {filter_map[effect]}'

        return base_options
