from discord.ext import commands
import discord
import random as r

class Citation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.citation_channel = None

    def add_channel(self, server):
        self.citation_channel = server.get_channel(775797448643313735)

    @commands.command(name='cita')
    async def _cita(self, ctx: commands.Context, *, user: discord.User = None):
        messages = [message async for message in self.citation_channel.history()]
        if(user == None):
            i = r.randint(1, len(messages))
            await ctx.send(messages[i-1].content)
        else:
            user_message = []
            for message in messages:
                if user in message.mentions:
                    user_message.append(message)
            if(len(user_message) == 0):
                await ctx.send("Essa pessoa não é merecedora de ser citada")
            else:
                i = r.randint(1, len(user_message))
                await ctx.send(user_message[i-1].content)
    
    @commands.command(name='test')
    async def _test(self, ctx: commands.Context):
        print(ctx.message.attachments[0].url)