import discord

from models.YTDLSource import YTDLSource


class Song:
    __slots__ = ('source', 'requester', 'is_radio')

    def __init__(self, source: YTDLSource, is_radio):
        self.source = source
        self.requester = source.requester
        self.is_radio = is_radio

    def create_embed(self):
        if(self.is_radio):
            print("embed created")
            embed = (discord.Embed(title='Now playing',
                               description=f'```css\n{self.source.title}\n```',
                               color=discord.Color.blurple())
                    .add_field(name='Duration', value="É uma rádio PORRA!")
                    .add_field(name='Requested by', value=self.requester.mention)
                    .add_field(name='Uploader', value=f'[{self.source.uploader}]({self.source.uploader_url})')
                    .add_field(name='URL', value='[Click](https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUTcmljayBhc3RsZXkgZ2l2ZSB1cA%3D%3D)')
                    .set_thumbnail(url="https://m80.iol.pt/images/capa_indisponivel.png"))
            print("embed finished")
        else:
            embed = (discord.Embed(title='Now playing',
                                description='```css\n{0.source.title}\n```'.format(self),
                                color=discord.Color.blurple())
                    .add_field(name='Duration', value=self.source.duration)
                    .add_field(name='Requested by', value=self.requester.mention)
                    .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                    .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                    .set_thumbnail(url=self.source.thumbnail))
            

        return embed

