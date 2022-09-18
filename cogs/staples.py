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
        embed = discord.Embed(title='**Staple Cards**', color=0x0000ff)
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


class Staples(commands.Cog):
    def __init__(self, bot):
        self.api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?staple=yes'
        self.bot = bot

    @commands.command()
    async def staples(self, ctx):
        """See staple cards"""
        view = View()
        message = await ctx.send('Retrieving staples...')

        count = 0
        names = []
        data = requests.get(self.api).json()

        for i in range(len(data['data'])):
            names.append(data['data'][i]['name'])

        page = ''
        pages = []
        for i in range(len(names)):
            page += f'{names[i]}\n'
            count += 1
            if (count == 20):
                count = 0
                pages.append(page)
                page = ''
        pages.append(page)

        nextPage = arrowButton(label='Next Page', pages=pages)
        previousPage = arrowButton(label='Previous Page', pages=pages)

        view.add_item(nextPage)
        view.add_item(previousPage)

        embed = discord.Embed(title='**Staple Cards**', color=0x0000ff)
        embed.add_field(name='Card List:', value=pages[0], inline=False)
        embed.set_footer(text=f'Page 1/{len(pages)}')

        await message.edit(content='Retrieved staple cards', embed=embed, view=view)

def setup(bot):
    bot.add_cog(Staples(bot))
