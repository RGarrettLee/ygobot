import discord
import os
import requests
import json
import time
from discord.ext import commands

class Card(commands.Cog):
    api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='

    def __init__(self, bot):
        pass

    def makeUrl(self, card):
        space = card.replace(' ', '%20')
        aps = space.replace("'", '%27')
        amp = aps.replace('&', '%26')
        return self.api + amp

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def card(self, ctx, *arg):
        try:
            message = await ctx.send('Retrieving card...')
            card = self.tupleConvert(arg)
            cardData = requests.get(self.makeUrl(card)).json()

            embed = discord.Embed(title='**{0}**'.format(cardData['data'][0]['name']), color=0x0000ff)
            try:
                embed.set_author(name='Archetype: {0}'.format(cardData['data'][0]['archetype']))
            except:
                pass
            try:
                embed.set_footer(text='Banlist Status: {0}'.format(cardData['data'][0]['banlist_info']['ban_tcg']))
            except:
                embed.set_footer(text='Banlist Status: Unlimited')
            embed.set_thumbnail(url=cardData['data'][0]['card_images'][0]['image_url'])
            if ('Trap' not in cardData['data'][0]['type'] and 'Spell' not in cardData['data'][0]['type']):
                if (not 'Link' in cardData['data'][0]['type']): embed.add_field(name='**Attribute: {0} | Level: {1}**'.format(cardData['data'][0]['attribute'], cardData['data'][0]['level']), value='**[ {0} / {1} ]**'.format(cardData['data'][0]['race'], cardData['data'][0]['type'].replace('Monster', '')), inline=False)
                else: embed.add_field(name='**Attribute: {0} | Link Rating: {1}**'.format(cardData['data'][0]['attribute'], cardData['data'][0]['linkval']), value='**[ {0} / {1} ]**'.format(cardData['data'][0]['race'], cardData['data'][0]['type'].replace('Monster', '')), inline=False)
                embed.add_field(name='**Card Description**', value=cardData['data'][0]['desc'], inline=False)
                if (not 'Link' in cardData['data'][0]['type']): embed.add_field(name='**ATK: {0} / DEF: {1}**'.format(cardData['data'][0]['atk'], cardData['data'][0]['def']), value='__Card Price: {0}__'.format(cardData['data'][0]['card_prices'][0]['tcgplayer_price']), inline=False)
                else: embed.add_field(name='**ATK: {0}**'.format(cardData['data'][0]['atk']), value='__Card Price: {0}__'.format(cardData['data'][0]['card_prices'][0]['tcgplayer_price']), inline=False)
            else:
                embed.add_field(name='**[{0} {1}]**'.format(cardData['data'][0]['race'], cardData['data'][0]['type'].replace('Card', '')), value='**Card Description**\n{0}\n\n__Card Price: {1}__'.format(cardData['data'][0]['desc'], cardData['data'][0]['card_prices'][0]['tcgplayer_price']), inline=False)
            await message.edit(content='Retrieved {0}'.format(cardData['data'][0]['name']), embed=embed)
        except:
            await message.edit(content='Invalid card entered')

def setup(bot):
    bot.add_cog(Card(bot))