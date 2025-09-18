import asyncio
import discord
from Bot import Bot
from discord.ext import commands
import ffmpeg

async def main():
    perms = discord.Permissions.general()
    perms.manage_channels = True

    bot = Bot(command_prefix=commands.when_mentioned_or("ola bot ", "olá bot ", "Ola bot ", "Olá bot "), description='Yet another music bot.', intents = discord.Intents.all())

    async with bot:
        await bot.add_cog()
        await bot.start()


if __name__ == "__main__":
    asyncio.run(main())

