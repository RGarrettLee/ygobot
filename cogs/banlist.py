import discord
import os
import requests
import json
import time
from discord.ext import commands

class Banlist(commands.Cog):
    api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?banlist=tcg'
    msgID = 0

    def __init__(self, bot):
        self.bot = bot
        self.names = []
        self.pages = []
        data = requests.get(self.api).json()

        for i in range(len(data['data'])):
            self.names.append('{0}: **{1}**'.format(data['data'][i]['name'], data['data'][i]['banlist_info']['ban_tcg']))

        out = ''
        self.page = 0

        for i in range(len(self.names)):
            if (i % 30 == 0):
                self.pages.append(out)
                self.page += 1
                out = ''
            else:
                out = out + self.names[i] + '\n'
        self.pages.append(out)
        self.pages.pop(0)
        self.page = 0

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name

        if ((emoji == '\N{Leftwards Black Arrow}' or emoji == '\N{Black Rightwards Arrow}') and not str(user) == 'YugiBot#5373'):
            if (message.id == self.msgID):
                if (emoji == '\N{Leftwards Black Arrow}' and self.page >= 0):
                    self.page -= 1
                    if (self.page <= 0): self.page = 0
                    embed = discord.Embed(title='Banlist', color=0x0000ff)
                    embed.add_field(name='Card List:', value=self.pages[self.page], inline=False)
                    embed.set_footer(text='Page {0}/{1}'.format(self.page + 1, len(self.pages)))
                    await message.edit(embed=embed)
                    await message.remove_reaction(emoji, user)
                elif (emoji == '\N{Black Rightwards Arrow}' and self.page < len(self.pages)):
                    self.page += 1
                    if (self.page == len(self.pages)): self.page = len(self.pages) - 1
                    embed = discord.Embed(title='Banlist', color=0x0000ff)
                    embed.add_field(name='Card List:', value=self.pages[self.page], inline=False)
                    embed.set_footer(text='Page {0}/{1}'.format(self.page + 1, len(self.pages)))
                    await message.edit(embed=embed)
                    await message.remove_reaction(emoji, user)

    @commands.command()
    async def banlist(self, ctx):
        self.page = 0
        message = await ctx.send('Retrieving the banlist...')

        embed = discord.Embed(title='Banlist', color=0x0000ff)
        embed.add_field(name='Card List:', value=self.pages[0], inline=False)
        embed.set_footer(text='Page 1/{0}'.format(len(self.pages)))

        await message.edit(content='Retrieved the banlist', embed=embed)
        await message.add_reaction('\N{Leftwards Black Arrow}')
        await message.add_reaction('\N{Black Rightwards Arrow}')
        self.msgID = message.id

def setup(bot):
    bot.add_cog(Banlist(bot))