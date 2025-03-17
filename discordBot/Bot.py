import discord
from discord.ext import commands
from unidecode import unidecode
from Citation import Citation
from Music import Music
from dotenv import load_dotenv
import os
import re
import asyncio
import random as r
import time

server = discord.Guild
iuriRole = 0
sala = 0
CdTP = 0

class Bot(commands.Bot):

    def __init__(self, command_prefix, description, intents):
        super().__init__(command_prefix, description=description, intents=intents)
        self.music = None
        self.citaton = None
        file = open(os.getenv("DISCORD_CONFIG_PATH"), "r")

        self._discordtoken = file.readline()
        file.close()

    async def on_ready(self):
        global server
        global iuriRole
        global sala
        global CdTP
        server = self.get_guild(464180049327947787)
        iuriRole = server.get_role(476152428161662993)
        sala = server.get_channel(1079476335841378395)
        CdTP = server.get_channel(538134492838363171)
        self.citaton.add_channel(server)
        print(f'Logged in as:\n{self.user.name}\n{self.user.id}')


    async def add_cog(self) :
        self.music = Music(self)
        self.citaton = Citation(self)
        await super().add_cog(self.music)
        await super().add_cog(self.citaton)
    
    async def start(self):
        return await super().start(self._discordtoken)

    async def on_voice_state_update(self, member, before, after):
        global server
        global iuriRole
        global sala
        global CdTP
        global musicClass
        if iuriRole in member.roles: #é o iuri
            if before.channel != after.channel: #mudou de canal
                if after.channel == sala:
                    await CdTP.send(self.oIuriEntrou())
                    sala = await sala.edit(name="Sala Com o Iuri")
                elif before.channel == sala:
                    for m in sala.members:
                        if iuriRole in m.roles:
                            return
                        sala = await sala.edit(name="Sala Sem o Iuri")

    async def on_message(self, message):
        global anusPessoal
        mnsg = unidecode(message.content)
        await self.process_commands(message)
        if re.search("boda", mnsg, re.IGNORECASE):
            await asyncio.sleep(r.randint(1, 60))
            await message.channel.send("O caralho que te foda")
        if r.randint(1, 400) == 1:
            n = r.randint(1, 10)
            for i in range(0, n):
                await message.channel.send("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. And rats make me crazy.")
                await asyncio.sleep(r.uniform(0.5,10))  
        if message.author == self.user:
            return
        anv = self.diaDeAnus()
        if self.mensagem_de_anos(mnsg):
            dias_id = 464176034627977216
            if message.author.id == anv:
                    await message.channel.send("Já sabia, bronco...")
            elif message.author.id == dias_id:
                if not anv:
                    anusPessoal[time.localtime()] = dias_id
                    await message.channel.send("Parece-me plausível")
                else:
                    await  message.channel.send("É LITERALMENTE IMPOSSÍVEL DUAS PESSOAS FAZEREM ANOS NO MESMO DIA")
            else:
                await message.channel.send("Tu não és especial")
        men = self.menciona(message, anv)
        if anv and men:
            await self.anus(anv, men, message)
        elif self.ativacaoOndeEstaOIuri(mnsg):
            await message.channel.send(self.ondeEstaOIuri(message))
        elif re.search("sabias que", mnsg, re.IGNORECASE):
           # await message.channel.send("Olá damas, cavalheiros e Iuri :nauseated_face:. Sejam bem-vindos à entrada da maravilhosa casa das citações. Quando disserem ou ouvirem dizer algo engraçado, mesmo muito engraçado ou até mesmo engraçadeco podem pôr aqui.\nDeixem-me exemplificar:\n```Contexto (opcional)\n\"Mensagem muito engraçada\" - @PessoaEngraçadaQueDisseAquilo 2023\n\"Resposta engraçada à mensagem engraçada\" - @OutraPessoaEngraçada 2023\n```\nÉ favor usarem os @ e escreverem como deve ser.\nPodem posteriormente colher o que semearam com uma simples mensagem na #casa-da-tua-prima `ola bot cita [@pessoa se quiserem especificar]`\nObrigado e volte sempre. São 5€ ")
            await message.channel.send(self.stringFixe())
        elif re.search("O LOL", mnsg) or re.search("A LOL", mnsg):
            await message.channel.send(self.lolPasta())
        elif re.search("culpa", message.content, re.IGNORECASE):
            await message.channel.send(self.aCulpa(message.content))
    
    def menciona(self, message, anv):
        val = 0
        for gajo in message.raw_mentions:
            if gajo == anv:
                return 2
            else:
                val = 1
        return val


    def diaDeAnus(self):
        anusPessoal = {time.strptime("02 02", "%d %m"): 605502890244833292, #Bernardo
               time.strptime("19 02", "%d %m"): 330033175881318401, #Cardas
               time.strptime("04 03", "%d %m"): 308697718006480908, #Diogo
               time.strptime("13 03", "%d %m"): 503693859767713792, #Ruben
               time.strptime("16 06", "%d %m"): 210832481316765706, #Fábio
               time.strptime("17 07", "%d %m"): 1064133004496216064, #Rodrigo
               time.strptime("19 08", "%d %m"): 464176034627977216, #Dias
               time.strptime("14 11", "%d %m"): 210831222677438465, #Iuri
               time.strptime("12 02", "%d %m"): 365586199231987722, #Braulio
               time.strptime("22 11", "%d %m"): 753284184818188309  #Claudia
               #time.strptime("12 03", "%d %m"): 601454336245235712 #Yuwi UwU
               #time.strptime("12 03", "%d %m"): 1081282162562703542 #Bot
}

        aniversariante = 0
        hoje = time.localtime()
        for dia in anusPessoal.keys():
            pessoa = anusPessoal[dia]
            if dia[2] == hoje[2] and dia[1] == hoje[1]:
                aniversariante = pessoa
                break
        return aniversariante

    async def anus(self, anv, men, message):
        global server
        if anv == 1081282162562703542:
            if men == 2:
                await message.channel.send("SIM! EU! O GLORIOSO BOT SEM O IURI NASCI HÁ PRECISAMENTE *N* ANO(S)")
            else:
                await message.channel.send("SEU GRANDESSÍSSIMO MONTE DE MERDA! EU, O BOT SEM O IURI, FAÇO ANOS E EXIJO A DEVIDA ATENÇÃO!")
        else:
            if men == 2:
                await message.channel.send(f"https://media.discordapp.net/attachments/881943053416411137/1084506032786645002/iu.png")
                await message.channel.send(f"É ELE! O GAJO QUE FAZ ANOS!!!\n")
            else:
                await message.channel.send(f"Gajo errado, menciona este: <@{anv}>\n\n\n\n||Já agora <@{anv}>, PARABÉNS!||")

            channel = server.get_member(anv).voice.channel
            if not self.music.voice_states and channel:
                self.music.anv = True
                voice = await channel.connect()
                i = r.randint(1,2)
                duration = [60, 20]
                music = "/home/anna/sites/discord/assets/audio/music_anv_" + str(i) + ".mp3"
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music))
                voice.play(source)
                await asyncio.sleep(duration[i-1])
                await voice.disconnect()
                self.music.anv = False

    def stringFixe(self):
        return ':flag_jp:\n                                                                       )\\_\\_\\_(\n                                                           \\_\\_\\_\\_\\_/\\_\\_/\\_\n                                                         /========= |\n                                -{]\\_\\_\\_\\_\\_\\_\\_\\_/\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_|\\_\\_\\_\\_\\_\\_[}-\n  \\_\\_-{]\\_\\_\\_\\_\\_-{]\\_\\_/\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\\\_\\_\\_[}-\\_\\_\\_\n  \\           Sabias que os Japoneses são maioritariamente            |\n    \\                               ~:sparkles:~***Light Cruisers***~:sparkles:~                             /\n\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\n'

    def lolPasta(self):
        return "Olá amigos, vamos jogar? E se transferissem o League of Legends agora mesmo, começassem a jogar, e ficassem imediatamente viciados. Aprendem rapidamente como funciona, duas equipas de 5 jogadores tentam destruir a base da outra equipa, em combate num mapa cheio de lacaios e monstros, Talvez joguem com o Garen. Gostam do Garen? É fácil matar adversários com o Garen. Não precisam de ser logo fantásticos porque o jogo junta os seus jogadores do mesmo nível, ou seja melhoram ao jogar cada vez mais e ao divertirem-se, e assim ganham o primeiro jogo de League of Legends na companhia de 5 desconhecidos, que bom. Mas lá no fundo teriam preferido contra inimigos na companhia de um grupo de amigos, podem ser um tanque, os vossos amigos podem ser curadores, arqueiros, assassinos, ou até magos, existem tantas funções disponíveis e prontas a serem usadas durante o jogo. O tempo passa, começam a perceber os outros campeões como Lux e os seus feitiços irritantes, Darius que gosta de afundar pessoas, e Teemo o exemplo de tudo o que há de errado na civilização moderna, gostam destes campeões, cada um com o seu estilo, também começam a descobrir pormenores as histórias únicas de cada campeão, e da sua ligação com o estilo de combate. O universo entra bem de vocês mas no bom sentido. A certa altura descobrem jogos com classificações onde os resultados decidem a posição num sistema de ligas e Divisões, Apercebem-se facilmente de que podem jogar e divertirem-se para todo o sempre. Mas com tantas coisas para experimentar, não há qualquer pressa. Isto é o League of Legends é competitivo, social e dinâmico, e depois de cada jogo só apetece clicar naquele botão grande que diz jogar novamente. E isto se tiverem mesmo transferido o League of Legends, a escolha é vossa."

    def oIuriEntrou(self):
        # Fabio, Dias, Yuri, Diogo, Rodrigo, Cardas, Cardas, Cardas, Ruben, Ruben, Ruben, Berna
        listEveryone = [210832481316765706, 464176034627977216, 210831222677438465, 308697718006480908, 1064133004496216064, 330033175881318401, 330033175881318401, 330033175881318401, 503693859767713792, 503693859767713792, 503693859767713792, 605502890244833292]
        n = r.randint(0, len(listEveryone))
        return f"<@{listEveryone[n]}> o IURI! ENTROU! NA SALA ***COM*** O __IURI__"

    def aCulpa(self, string):
        i = 0
        while i<len(string):
            if string[i] == "C" or string[i] == "c":
                if re.search("culpa", string[i:i+5], re.IGNORECASE):
                    break
            i += 1

        return "> " + string[0:i] + "**" + string[i:i+5] + "**" + string[i+5:len(string)] + f"\n ...é do <@{503693859767713792}>"

    def mensagem_de_anos(self, text):
        text = text.lower()
        return text.startswith("ola bot hoje faco anos")

    def ativacaoOndeEstaOIuri(self, message):
        val = (bool(re.search("onde", message, re.IGNORECASE)) and bool(re.search("iuri", message, re.IGNORECASE))) or \
            bool(re.search("que e do iuri", message, re.IGNORECASE))
        return val

    def ondeEstaOIuri(self, message):
        respostas = ["L̸̛̟͇̹̰̘͂̊̂̈́ê̵̱̫̻̲̞͂͗͗͋̋ï̵̝̣̻͙̗͆̃́̀̚r̴̨̳̲̟̠̈́̀͌̉̚ï̶͎̙͙̘̫̈̌͒͛͘å̵̡̫͍̫̱̔̀̾͌́", "No cu do conde", "Hogwarts :man_mage:", "C'o Boda", "_ _", "Qual Iuri?"]
        n = r.randint(0, len(respostas) + len(respostas)//2)
        n = n if n < len(respostas) else len(respostas)-1 # mais chance de calhar "Qual Iuri?"
        # depois fazer com que seja uma resposta à mensagem que gerou isto
        return respostas[n]
