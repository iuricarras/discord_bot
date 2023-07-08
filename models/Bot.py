import discord
from discord.ext import commands
from models.Music import Music
from dotenv import load_dotenv
import os

class Bot(commands.Bot):

    def __init__(self, command_prefix, description, intents):
        super().__init__(command_prefix, description=description, intents=intents)
        self.music = None
        load_dotenv()

        self._discordtoken = os.getenv("discord_token")

    async def on_ready(self):
        print("Done")
        print(f'Logged in as:\n{self.user.name}\n{self.user.id}')


    async def add_cog(self) :
        self.music = Music(self)
        return await super().add_cog(self.music)
    
    async def start(self):
        return await super().start(self._discordtoken)