import random as r
import discord
import re
import logging
import time
import asyncio
from audio import Music, YTDLSource
from unidecode import unidecode
from discord.ext import commands
import yt_dlp as youtube_dl

handler = logging.FileHandler(filename='discord_log.log', encoding='utf-8', mode='w')

intents = discord.Intents.all()

perms = discord.Permlowerissions.general()
perms.manage_channels = True

#client = discord.Client(intents = intents)


client = commands.Bot(
    command_prefix=commands.when_mentioned_or("ola bot ", "olá bot ", "Ola bot ", "Olá bot "),
    description='Relatively simple music bot example',
    intents=intents,
)

client.max_ratelimit_timeout = 30.0
server = discord.Guild
iuriRole = 0
sala = 0
CdTP = 0
musicClass = Music(client)

anusPessoal = {time.strptime("02 02", "%d %m"): 605502890244833292, #Bernardo
               time.strptime("19 02", "%d %m"): 330033175881318401, #Cardas
               time.strptime("04 03", "%d %m"): 308697718006480908, #Diogo
               time.strptime("13 03", "%d %m"): 503693859767713792, #Ruben
               time.strptime("16 06", "%d %m"): 210832481316765706, #Fábio
               time.strptime("17 07", "%d %m"): 1064133004496216064, #Rodrigo
               time.strptime("19 08", "%d %m"): 464176034627977216, #Dias
               time.strptime("14 11", "%d %m"): 210831222677438465 # #Iuri
               #time.strptime("12 03", "%d %m"): 601454336245235712 #Yuwi UwU
               #time.strptime("12 03", "%d %m"): 1081282162562703542 #Bot
               }

@client.event
async def on_ready():
    global server
    global iuriRole
    global sala
    global CdTP
    server = client.get_guild(464180049327947787)
    iuriRole = server.get_role(476152428161662993)
    sala = server.get_channel(1079476335841378395)
    CdTP = server.get_channel(538134492838363171)
    print(f'We have logged in as {client.user}\n')

@client.event
async def on_voice_state_update(member, before, after):
    global server
    global iuriRole
    global sala
    global CdTP
    global musicClass
    if iuriRole in member.roles: #é o iuri
        if before.channel != after.channel: #mudou de canal
            if after.channel == sala:
                await CdTP.send(oIuriEntrou())
                sala = await sala.edit(name="Sala Com o Iuri")
            elif before.channel == sala:
                for m in sala.members:
                    if iuriRole in m.roles:
                        return
                    sala = await sala.edit(name="Sala Sem o Iuri")

    if member.id == client.user.id:
        voice = after.channel.guild.voice_client
        time = -15
        while True:
            await asyncio.sleep(1)
            time = time + 1
            print(time)
            if voice.is_playing():
                 time = 0
            if time == 5:
                if len(musicClass.musicas) > 0:
                    print(len(musicClass.musicas))
                    time = -15
                    asyncio.run(await musicClass.listplay())
                    print(len(musicClass.musicas))
                else:
                    await client.change_presence()
                    musicClass.playing = False
            if time == 300:
                await voice.disconnect()
            if not voice.is_connected():
                break



def stringFixe():
    return ':flag_jp:\n                                                                       )\\_\\_\\_(\n                                                           \\_\\_\\_\\_\\_/\\_\\_/\\_\n                                                         /========= |\n                                -{]\\_\\_\\_\\_\\_\\_\\_\\_/\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_|\\_\\_\\_\\_\\_\\_[}-\n  \\_\\_-{]\\_\\_\\_\\_\\_-{]\\_\\_/\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\\\_\\_\\_[}-\\_\\_\\_\n  \\           Sabias que os Japoneses são maioritariamente            |\n    \\                               ~:sparkles:~***Light Cruisers***~:sparkles:~                             /\n\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\\~\n'

def lolPasta():
    return "Olá amigos, vamos jogar? E se transferissem o League of Legends agora mesmo, começassem a jogar, e ficassem imediatamente viciados. Aprendem rapidamente como funciona, duas equipas de 5 jogadores tentam destruir a base da outra equipa, em combate num mapa cheio de lacaios e monstros, Talvez joguem com o Garen. Gostam do Garen? É fácil matar adversários com o Garen. Não precisam de ser logo fantásticos porque o jogo junta os seus jogadores do mesmo nível, ou seja melhoram ao jogar cada vez mais e ao divertirem-se, e assim ganham o primeiro jogo de League of Legends na companhia de 5 desconhecidos, que bom. Mas lá no fundo teriam preferido contra inimigos na companhia de um grupo de amigos, podem ser um tanque, os vossos amigos podem ser curadores, arqueiros, assassinos, ou até magos, existem tantas funções disponíveis e prontas a serem usadas durante o jogo. O tempo passa, começam a perceber os outros campeões como Lux e os seus feitiços irritantes, Darius que gosta de afundar pessoas, e Teemo o exemplo de tudo o que há de errado na civilização moderna, gostam destes campeões, cada um com o seu estilo, também começam a descobrir pormenores as histórias únicas de cada campeão, e da sua ligação com o estilo de combate. O universo entra bem de vocês mas no bom sentido. A certa altura descobrem jogos com classificações onde os resultados decidem a posição num sistema de ligas e Divisões, Apercebem-se facilmente de que podem jogar e divertirem-se para todo o sempre. Mas com tantas coisas para experimentar, não há qualquer pressa. Isto é o League of Legends é competitivo, social e dinâmico, e depois de cada jogo só apetece clicar naquele botão grande que diz jogar novamente. E isto se tiverem mesmo transferido o League of Legends, a escolha é vossa."

def oIuriEntrou():
    # Fabio, Dias, Yuri, Diogo, Rodrigo, Cardas, Cardas, Cardas, Ruben, Ruben, Ruben, Berna
    listEveryone = [210832481316765706, 464176034627977216, 210831222677438465, 308697718006480908, 1064133004496216064, 330033175881318401, 330033175881318401, 330033175881318401, 503693859767713792, 503693859767713792, 503693859767713792, 605502890244833292]
    n = r.randint(0, len(listEveryone))
    return f"<@{listEveryone[n]}> o IURI! ENTROU! NA SALA ***COM*** O __IURI__"

def aCulpa(string):
    i = 0
    while i<len(string):
        if string[i] == "C" or string[i] == "c":
            if re.search("culpa", string[i:i+5], re.IGNORECASE):
               break
        i += 1

    return "> " + string[0:i] + "**" + string[i:i+5] + "**" + string[i+5:len(string)] + f"\n ...é do <@{503693859767713792}>"

def mensagem_de_anos(text):
    text = text.lower()
    return text.startswith("ola bot hoje faco anos")

def ativacaoOndeEstaOIuri(message):
    val = (bool(re.search("onde", message, re.IGNORECASE)) and bool(re.search("iuri", message, re.IGNORECASE))) or \
        bool(re.search("que e do iuri", message, re.IGNORECASE))
    return val

def ondeEstaOIuri(message):
    respostas = ["L̸̛̟͇̹̰̘͂̊̂̈́ê̵̱̫̻̲̞͂͗͗͋̋ï̵̝̣̻͙̗͆̃́̀̚r̴̨̳̲̟̠̈́̀͌̉̚ï̶͎̙͙̘̫̈̌͒͛͘å̵̡̫͍̫̱̔̀̾͌́", "No cu do conde", "Hogwarts :man_mage:", "C'o Boda", "_ _", "Qual Iuri?"]
    n = r.randint(0, len(respostas) + len(respostas)//2)
    n = n if n < len(respostas) else len(respostas)-1 # mais chance de calhar "Qual Iuri?"
    # depois fazer com que seja uma resposta à mensagem que gerou isto
    return respostas[n]

@client.event
async def on_message(message):
    global anusPessoal
    mnsg = unidecode(message.content)
    await client.process_commands(message)
    if re.search("boda", mnsg, re.IGNORECASE):
        await asyncio.sleep(r.randint(1, 60))
        await message.channel.send("O caralho que te foda")
    if r.randint(1, 200) == 1:
        n = r.randint(1, 10)
        for i in range(0, n):
            await message.channel.send("Crazy? I was crazy once. They put me in a room. A rubber room. A rubber room with rats. And rats make me crazy.")
            await asyncio.sleep(r.uniform(0.5,10))
    if message.author == client.user:
        return
    anv = diaDeAnus()
    if mensagem_de_anos(mnsg):
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
    men = menciona(message, anv)
    if anv and men:
        await anus(anv, men, message)
    elif ativacaoOndeEstaOIuri(mnsg):
        await message.channel.send(ondeEstaOIuri(message))
    elif re.search("sabias que", mnsg, re.IGNORECASE):
        await message.channel.send(stringFixe())
    elif re.search("O LOL", mnsg) or re.search("A LOL", mnsg):
        await message.channel.send(lolPasta())
    elif re.search("culpa", message.content, re.IGNORECASE):
        await message.channel.send(aCulpa(message.content))

def menciona(message, anv):
    val = 0
    for gajo in message.raw_mentions:
        if gajo == anv:
            return 2
        else:
            val = 1
    return val


def diaDeAnus():
    aniversariante = 0
    hoje = time.localtime()
    for dia in anusPessoal.keys():
        pessoa = anusPessoal[dia]
        if dia[2] == hoje[2] and dia[1] == hoje[1]:
            aniversariante = pessoa
            break
    return aniversariante

async def anus(anv, men, message):
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


async def main():
    global musicClass
    async with client:
        await client.add_cog(musicClass)
        await client.start('MTA4MTI4MjE2MjU2MjcwMzU0Mg.GHNXUz.JCrreqwr3fWFXnzVvtGrM6_qoLSgjf1-plI5Yg')

if __name__ == "__main__":
    asyncio.run(main())

