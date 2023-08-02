import asyncio
import functools
import discord
from discord.ext import commands
from models.ErrorHandler import YTDLError
import yt_dlp as youtube_dl
from pyradios import RadioBrowser

youtube_dl.utils.bug_reports_message = lambda: ''

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5, is_radio, is_file = False):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data
        self.title = data.get('title')
        self.stream_url = data.get('url')
        self.uploader = data.get('uploader')
        if is_file:
            return
        self.uploader_url = data.get('uploader_url')
        self.thumbnail = data.get('thumbnail')
        if not is_radio:
            date = data.get('upload_date')
            self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
            self.description = data.get('description')
            self.duration = self.parse_duration(int(data.get('duration')))
            self.tags = data.get('tags')
            self.url = data.get('webpage_url')
            self.views = data.get('view_count')
            self.likes = data.get('like_count')
            self.dislikes = data.get('dislike_count')


    def __str__(self):
        return '**{0.title}** por **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None, is_radio, is_file = False):
        if is_file:
            info = {"title": "Uma Merda Qualquer ®",
                    "url": search, 
                    "uploader": ctx.author}
            return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info, is_radio=False, is_file=True)
        elif is_radio:
            rb = RadioBrowser()
            radios = rb.search(name=search, name_exact=False, order="clickcount", reverse=True)
            #radios = {"m80": {"title": "Rádio M80", "uploader": "M80" ,"uploader_url": 'https://m80.pt',"url": "http://stream-icy.bauermedia.pt/m80.mp3"},
            #      "m80portugal": {"title": "Rádio M80 Portugal", "uploader": "M80", "uploader_url": "https://m80.pt/","url": "https://stream-icy.bauermedia.pt/m80nacional.aac"},
            #      "m80rock": {"title": "Rádio M80 Rock", "uploader": "M80","uploader_url": "https://m80.pt/","url": "https://stream-icy.bauermedia.pt/m80rock.aac"}}
            
            #radio_name = search.lower()
            #radio = radios.get(radio_name)
            if radios is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))


            radio = {"title": radios[0].get("name"), "url": radios[0].get("url"), "uploader": radios[0].get("country"), "uploader_url": radios[0].get("homepage"), "thumbnail": radios[0].get("favicon")}

            return cls(ctx, discord.FFmpegPCMAudio(radio['url'], **cls.FFMPEG_OPTIONS), data=radio, is_radio=True)
        else:
            loop = loop or asyncio.get_event_loop()

            partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
            data = await loop.run_in_executor(None, partial)

            if data is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

            if 'entries' not in data:
                process_info = data
            else:
                process_info = None
                for entry in data['entries']:
                    if entry:
                        process_info = entry
                        break

                if process_info is None:
                    raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

            webpage_url = process_info['webpage_url']
            partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
            processed_info = await loop.run_in_executor(None, partial)

            if processed_info is None:
                raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

            if 'entries' not in processed_info:
                info = processed_info
            else:
                info = None
                while info is None:
                    try:
                        info = processed_info['entries'].pop(0)
                    except IndexError:
                        raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info, is_radio=False)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)