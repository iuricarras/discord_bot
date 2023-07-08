# This example requires the 'message_content' privileged intent to function.
import random as r
import asyncio
import discord
import yt_dlp as youtube_dl
from discord.ext import commands
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


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
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.musicas = []
        self.playing = False
        self.ctx = None
        print("Class music started")

    @commands.command()
    async def join(self, ctx):
        """Join channel"""

        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    """@commands.command()
    async def play(self, ctx, *, query):
        #Plays a file from the local filesystem

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')"""

    @commands.command(aliases=['mete', 'toca'])
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        if(r.randint(1,200) == 1):
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/audio/Rick_Astley_-_Never_Gonna_Give_You_Up.mp3"))
            ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            await ctx.send("Get Rick Rolled!")
        elif self.playing == False:
            asyncio.run(await self.insideplay(url, ctx))
        else:
            self.musicas.append(url)
            self.ctx = ctx
            await ctx.send(f"Põe-te na bicha, crl\n Musica na fila -> Posição {len(self.musicas)}")

         ########
        

    async def listplay(self):
        url = self.musicas.pop(0)
        asyncio.run(await self.insideplay(url, self.ctx))
 
    async def insideplay(self, url, ctx):
        async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                streaming = discord.Streaming(name=player.title, url=url)
                await self.bot.change_presence(activity=streaming)
        await ctx.send(f"A tocar: {player.title}")
        self.playing = True

    @commands.command(aliases=['passa'])
    async def skip(self, ctx,):
        """Skips a music"""
        if(len(self.musicas) > 0):
            await ctx.send("A saltar esta música")
            ctx.voice_client.stop()
        else:
            await ctx.send("Não há mais músicas na lista palhaço")

 


    """@commands.command()
    async def stream(self, ctx, *, url):
        #Streams from a url (same as yt, but doesn't predownload)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')"""

    @commands.command()
    async def radio(self, ctx, *, name):
        """Radios"""
        radios = {"m80": "http://stream-icy.bauermedia.pt/m80.mp3",
                  "m80portugal": "https://stream-icy.bauermedia.pt/m80nacional.aac",
                  "m80rock": "https://stream-icy.bauermedia.pt/m80rock.aac"}
        radios_full = {"m80": "Rádio M80",
                  "m80portugal": "Rádio M80 Nacional",
                  "m80rock": "Rádio M80 Rock"}

        radio_name = name.lower()
        radio = radios.get(radio_name)
        if radio == None:
            await ctx.send('Radio não encontrada')
        else:
            async with ctx.typing():
                ctx.voice_client.play(discord.FFmpegPCMAudio(source=radio))
                streaming = discord.Streaming(name=radios_full.get(radio_name), url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUTcmljayBhc3RsZXkgZ2l2ZSB1cA%3D%3D")
                await self.bot.change_presence(activity=streaming)
            await ctx.send(f'A curtir batidão: {radios_full.get(radio_name)}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(aliases=['morre', 'fodete', 'fode-te', 'pokaralo', 'baza', 'falece'])
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await self.bot.change_presence()
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @radio.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
