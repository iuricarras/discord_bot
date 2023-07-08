import asyncio
import discord
from discord.ext import commands
from models.music_bot_example import Music


bot = commands.Bot('music.', description='Yet another music bot.', intents = discord.Intents.all())
perms = discord.Permissions.general()
perms.manage_guild = True

@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))


async def main():
    global musicClass
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start('MTA4MTI4MjE2MjU2MjcwMzU0Mg.GHNXUz.JCrreqwr3fWFXnzVvtGrM6_qoLSgjf1-plI5Yg')

if __name__ == "__main__":
    asyncio.run(main())

