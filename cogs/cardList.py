import discord
import os
import json
import time
import requests
from fuzzywuzzy import process
from discord.ext import commands
from discord.ext.commands import Option
from discord.ui import Button, View

class arrowButton(Button):
    def __init__(self, label, set, pages):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.pages = pages
        self.set = set
        self.page = 1

    async def callback(self, interaction):
            embed = discord.Embed(title='{0}'.format(self.set), color=0x0000ff)
            if (self.label == 'Previous Page'):
                if (self.page > 1):
                    self.page -= 1
                    for i in self.view.children: # updates pages between buttons memory
                        if (i.label == 'Next Page'):
                            i.page = self.page
            elif (self.label == 'Next Page'):
                if (self.page < len(self.pages)):
                    self.page += 1
                    for i in self.view.children:
                        if (i.label == 'Previous Page'):
                            i.page = self.page

            embed.add_field(name='Card List', value=self.pages[self.page - 1], inline=False)
            embed.set_footer(text=f'Page {self.page}/{len(self.pages)}')
            await interaction.response.edit_message(embed=embed)

class CardList(commands.Cog):
    oneTime = 'https://db.ygoprodeck.com/api/v7/cardsets.php'
    infoApi = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset='

    def __init__(self, bot):
        self.sets = {}
        self.setDB = {}
        self.setNames = []
        self.bot = bot
        self.currentSet = ''

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
            self.setNames.append(name)
            self.setDB[name] = name.replace(' ', '%20')
            self.setDB[name] = name.replace("'", '%27')


    @commands.command()
    async def set(self, ctx, set: str):
        """Retrieve the card list of a given set"""
        view = View()

        self.sets = requests.get(self.oneTime).json()
        if (len(self.setDB) < 1):
            self.extractSets()
        highest = process.extractOne(set, self.setNames)
        product = highest[0]
        message = await ctx.send('Retrieving list', ephemeral=True, delete_after=60)
        try:
            productData = requests.get(self.infoApi + self.makeUrl(product)).json()
            setCards = []
            for i in range(len(productData['data'][0]['card_sets'])):
                if (product == productData['data'][0]['card_sets'][i]['set_name'].lower()):
                    self.currentSet = productData['data'][0]['card_sets'][i]['set_name']
            for i in range(len(productData['data'])):
                for j in range(len(productData['data'][i]['card_sets'])):
                    if (product == productData['data'][i]['card_sets'][j]['set_name'].lower()):
                        setCards.append('{0}: **{1}**'.format(productData['data'][i]['name'], productData['data'][i]['card_sets'][j]['set_rarity']))

            page = ''
            pages = []
            count = 0
            for i in range(len(setCards)):
                page += f'{setCards[i]}\n'
                count += 1
                if (count == 20):
                    count = 0
                    pages.append(page)
                    page = ''
            pages.append(page)

            nextPage = arrowButton(label='Next Page', set=self.currentSet, pages=pages)
            previousPage = arrowButton(label='Previous Page', set=self.currentSet, pages=pages)

            view.add_item(nextPage)
            view.add_item(previousPage)

            embed = discord.Embed(title='{0}'.format(self.currentSet), color=0x0000ff)
            embed.add_field(name='Card List', value=pages[0])
            embed.set_footer(text='Page 1/{0}'.format(len(pages)))

            await message.edit(content='Retrieved {0} card list'.format(self.currentSet))
            await ctx.send(embed=embed, view=view)
        except:
            await message.edit(content='<@!174263950685372417> has been notified with the exact **set** you used causing the error')
            user = self.bot.get_user(174263950685372417)
            await user.send(f'The set: **{set}** caused an error')

def setup(bot):
    bot.add_cog(CardList(bot))