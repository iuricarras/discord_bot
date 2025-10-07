from discord.ext import commands
import discord
import random as r

class Citation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.citation_channel = None

        r.seed(8978979817897)
        n = 14
        secretsantaArray = list(range(n))
        for i in range(n - 1):
            j = r.randrange(i + 1, n)
            secretsantaArray[i], secretsantaArray[j] = secretsantaArray[j], secretsantaArray[i]

        self.secretsantaArray = secretsantaArray
        print(self.secretsantaArray)
        self.listUsers = [330033175881318401, 308697718006480908, 503693859767713792, 210832481316765706, 1064133004496216064, 464176034627977216, 210831222677438465, 365586199231987722, 753284184818188309, 574697874969853968, 1238182201645076571, 511541066579705886, 500413902278885382, 296337477638029322]


    def add_channel(self, server):
        self.citation_channel = server.get_channel(775797448643313735)

    @commands.command(name='prenda')
    async def _prenda(self, ctx: commands.Context):
        if(ctx.author.id in self.listUsers):
            i = self.listUsers.index(ctx.author.id)
            j = self.secretsantaArray[i]
            recetor = await self.bot.fetch_user(self.listUsers[j])
            await ctx.author.send(f"Tens que dar prenda a {recetor.name}")
        else:
            await ctx.send("Você não está na lista de participantes")

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