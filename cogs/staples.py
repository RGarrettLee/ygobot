import discord
import os
import requests
import json
import time
from discord.ext import commands

class Staples(commands.Cog):
    api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?staple=yes'
    tcgplayer = 'https://www.tcgplayer.com/search/yugioh/product?productLineName=yugioh&productName='
    msgID = 0
    page = 1

    def __init__(self, bot):
        self.bot = bot
        self.names = []
        data = requests.get(self.api).json()

        for i in range(len(data['data'])):
            self.names.append(data['data'][i]['name'])

        self.page1 = ''
        self.page2 = ''

        for i in range(len(self.names)):
            if (i <= (len(self.names) / 2)):
                self.page1 = self.page1 + self.names[i] + '\n'
            else:
                self.page2 = self.page2 + self.names[i] + '\n'

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name

        if ((emoji == '\N{Leftwards Black Arrow}' or emoji == '\N{Black Rightwards Arrow}') and not str(user) == 'YugiBot#5373'):
            if (message.id == self.msgID):
                if (emoji == '\N{Leftwards Black Arrow}' and self.page == 2):
                    embed = discord.Embed(title='**Staple Cards**', color=0x0000ff)
                    embed.set_footer(text='Page 1/2')
                    embed.add_field(name='Card List:', value=self.page1, inline=False)
                    await message.edit(embed=embed)
                    await message.remove_reaction(emoji, user)
                    self.page = 1
                elif (emoji == '\N{Black Rightwards Arrow}' and self.page == 1):
                    embed = discord.Embed(title='**Staple Cards**', color=0x0000ff)
                    embed.set_footer(text='Page 2/2')
                    embed.add_field(name='Card List:', value=self.page2, inline=False)
                    await message.edit(embed=embed)
                    await message.remove_reaction(emoji, user)
                    self.page = 2

    @commands.command()
    async def staples(self, ctx):
        message = await ctx.send('Retrieving staples...')

        embed = discord.Embed(title='**Staple Cards**', color=0x0000ff)
        embed.add_field(name='Card List:', value=self.page1, inline=False)
        embed.set_footer(text='Page 1/2')

        await message.edit(content='Retrieved staple cards', embed=embed)
        await message.add_reaction('\N{Leftwards Black Arrow}')
        await message.add_reaction('\N{Black Rightwards Arrow}')
        self.msgID = message.id

def setup(bot):
    bot.add_cog(Staples(bot))
