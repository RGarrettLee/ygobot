import discord
import os
import json
import time
import requests
from discord.ext import commands

class CardList(commands.Cog):
    api = ''
    oneTime = 'https://db.ygoprodeck.com/api/v7/cardsets.php'
    infoApi = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset='
    msgID = 0

    def __init__(self, bot):
        self.sets = requests.get(self.oneTime).json()
        self.setDB = {}
        self.pages = []
        self.bot = bot
        self.currentSet = ''
        self.page = 0

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    def makeUrl(self, product):
        space = product.replace(' ', '%20')
        aps = space.replace("'", '%27')
        amp = aps.replace('&', '%26')
        return amp

    def extractSets(self):
        for i in range(len(self.sets)):
            name = self.sets[i]['set_name'].lower()
            name = name.strip()
            self.setDB[name] = name.replace(' ', '%20')
            self.setDB[name] = name.replace("'", '%27')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name

        if ((emoji == '\N{Leftwards Black Arrow}' or emoji == '\N{Black Rightwards Arrow}') and not str(user) == 'The Chesapeake Ripper Bot#6294'):
            if (message.id == self.msgID):
                if (emoji == '\N{Leftwards Black Arrow}' and self.page >= 0):
                    self.page -= 1
                    if (self.page <= 0): self.page = 0
                    embed = discord.Embed(title='{0}'.format(self.currentSet), color=0x0000ff)
                    embed.add_field(name='Card List:', value=self.pages[self.page], inline=False)
                    embed.set_footer(text='Page {0}/{1}'.format(self.page + 1, len(self.pages)))
                    await message.edit(embed=embed)
                    await message.remove_reaction(emoji, user)
                elif (emoji == '\N{Black Rightwards Arrow}' and self.page < len(self.pages)):
                    self.page += 1
                    if (self.page == len(self.pages)): self.page = len(self.pages) - 1
                    embed = discord.Embed(title='{0}'.format(self.currentSet), color=0x0000ff)
                    embed.add_field(name='Card List:', value=self.pages[self.page], inline=False)
                    embed.set_footer(text='Page {0}/{1}'.format(self.page + 1, len(self.pages)))
                    await message.edit(embed=embed)
                    await message.remove_reaction(emoji, user)

    @commands.command(pass_context=True, aliases=['list', 'setList', 'listSet', 'listset', 'cardlist', 'setlist'])
    async def cardList(self, ctx, *arg):
        if (len(self.setDB) < 1):
            self.extractSets()

        self.pages = []
        product = self.tupleConvert(arg)
        message = await ctx.send('Retrieving list for {0}...'.format(product))
        try:
            productData = requests.get(self.infoApi + self.makeUrl(product)).json()
            setCards = []
            for i in range(len(productData['data'][0]['card_sets'])):
                if (product == productData['data'][0]['card_sets'][i]['set_name'].lower()):
                    self.currentSet = productData['data'][0]['card_sets'][i]['set_name']
            for i in range(len(productData['data'])):
                setCards.append('{0}: **{1}**'.format(productData['data'][i]['name'], productData['data'][i]['card_sets'][0]['set_rarity']))

            out = ''
            for i in range(len(setCards)):
                if (i % 25 == 0):
                    self.pages.append(out)
                    self.page += 1
                    out = ''
                else:
                    out = out + setCards[i] + '\n'
            self.pages.append(out)
            self.pages.pop(0)
            self.page = 0

            embed = discord.Embed(title='{0}'.format(self.currentSet), color=0x0000ff)
            embed.add_field(name='Card List', value=self.pages[0])
            embed.set_footer(text='Page 1/{0}'.format(len(self.pages)))

            await message.edit(content='Retrieved {0} card list'.format(self.currentSet), embed=embed)
            await message.add_reaction('\N{Leftwards Black Arrow}')
            await message.add_reaction('\N{Black Rightwards Arrow}')
            self.msgID = message.id
        except:
            await message.edit(content='Invalid set entered')

def setup(bot):
    bot.add_cog(CardList(bot))