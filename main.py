import asyncio
import discord
from models.Bot import Bot



#perms = discord.Permissions.general()
#perms.manage_guild = True

async def main():
    bot = Bot('music.', description='Yet another music bot.', intents = discord.Intents.all())

    async with bot:
        await bot.add_cog()
        await bot.start()


if __name__ == "__main__":
    asyncio.run(main())

