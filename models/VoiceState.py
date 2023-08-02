import asyncio
from async_timeout import timeout
from discord.ext import commands
import discord

from models.ErrorHandler import VoiceError
from models.SongQueue import SongQueue

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()
        self.dead = False


        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()
            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        print("DEGUB - Looking for songs")
                        self.current = await self.songs.get()
                        print("DEGUB - Song found")
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return
            print("DEGUB - Start playing")
            self.current.source.volume = self._volume
            print("Playing")
            self.voice.play(self.current.source, after=self.play_next_song)
            print("Playing")
            await self.current.source.channel.send(embed=self.current.create_embed())
            streaming = discord.Streaming(name=self.current.source.title, url=("https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUTcmljayBhc3RsZXkgZ2l2ZSB1cA%3D%3D" if self.current.is_radio or self.current.is_file else self.current.source.url))
            await self.bot.change_presence(activity=streaming)

            await self.next.wait()


    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()
        self.dead = True
        await self.bot.change_presence()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None