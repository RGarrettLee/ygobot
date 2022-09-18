from tkinter import PAGES
import discord
import os
import requests
import json
import time
from discord.ext import commands
from discord.ui import Button, View
class arrowButton(Button):
    def __init__(self, label, pages):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.pages = pages
        self.page = 1

    async def callback(self, interaction):
        embed = discord.Embed(title='**Banlist**', color=0x0000ff)
        if (self.label == 'Previous Page'):
            if (self.page > 1):
                self.page -= 1
                for i in self.view.children:
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

class Banlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?banlist=tcg'

    @commands.command()
    async def banlist(self, ctx):
        """See all the cards on the banlist"""
        view = View()
        message = await ctx.send('Retrieving the banlist...')

        count = 0
        names = []
        data = requests.get(self.api).json()

        for i in range(len(data['data'])):
            names.append('{0}: **{1}**'.format(data['data'][i]['name'], data['data'][i]['banlist_info']['ban_tcg']))

        page = ''
        pages = []
        for i in range(len(names) - 1):
            page += f'{names[i]}\n'
            count += 1
            if (count == 20):
                count = 0
                pages.append(page)
                page = ''
        pages.append(page)

        nextPage = arrowButton(label='Next Page', pages=pages)
        previousPage = arrowButton(label='Previous Page', pages=pages)
        banlistLink = Button(label='View Banlist', style=discord.ButtonStyle.link, url='https://www.yugioh-card.com/en/limited/', emoji='📄')

        view.add_item(nextPage)
        view.add_item(previousPage)
        view.add_item(banlistLink)

        embed = discord.Embed(title='**Banlist**', color=0x0000ff)
        embed.add_field(name='Card List:', value=pages[0], inline=False)
        embed.set_footer(text=f'Page 1/{len(pages)}')

        await message.edit(content='Retrieved the banlist', embed=embed, view=view)

def setup(bot):
    bot.add_cog(Banlist(bot))