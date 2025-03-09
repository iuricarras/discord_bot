import discord

from models.YTDLSource import YTDLSource


class Song:
    __slots__ = ('source', 'requester', 'is_radio', 'is_file')

    def __init__(self, source: YTDLSource, is_radio, is_file):
        self.source = source
        self.requester = source.requester
        self.is_radio = is_radio
        self.is_file = is_file

    def create_embed(self):
        if self.is_file:
            print("embed created")
            embed = (discord.Embed(title='A tocar',
                               description=f'```css\n{self.source.title}\n```',
                               color=discord.Color.blurple())
                    .add_field(name='Duração', value="O ficheiro é teu PORRA!")
                    .add_field(name='A pedido de:', value=self.requester.mention)
                    .add_field(name='De:', value=self.requester.mention)
                    .add_field(name='Cadeia de caracteres mágica que te leva a sitios da internet', value=f'[Click]({self.source.stream_url})')
                    .set_thumbnail(url=self.requester.avatar.url))
            print("embed finished")
        elif(self.is_radio):
            print("embed created")
            embed = (discord.Embed(title='A tocar',
                               description=f'```css\n{self.source.title}\n```',
                               color=discord.Color.blurple())
                    .add_field(name='Duração', value="É uma rádio PORRA!")
                    .add_field(name='A pedido de:', value=self.requester.mention)
                    .add_field(name='De:', value=f'[{self.source.uploader}]({self.source.uploader_url})')
                    .add_field(name='Cadeia de caracteres mágica que te leva a sitios da internet', value='[Click](https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUTcmljayBhc3RsZXkgZ2l2ZSB1cA%3D%3D)')
                    .set_thumbnail(url=self.source.thumbnail))
            print("embed finished")
        else:
            embed = (discord.Embed(title='A tocar',
                                description='```css\n{0.source.title}\n```'.format(self),
                                color=discord.Color.blurple())
                    .add_field(name='Duração', value=self.source.duration)
                    .add_field(name='A pedido de:', value=self.requester.mention)
                    .add_field(name='De:', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                    .add_field(name='Cadeia de caracteres mágica que te leva a sitios da internet', value='[Click]({0.source.url})'.format(self))
                    .set_thumbnail(url=self.source.thumbnail))
            

        return embed

