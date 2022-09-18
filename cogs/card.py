import discord
import os
import requests
import json
import time
import io
import urllib.parse
from fuzzywuzzy import process
from discord.ext import commands
from discord.ext.commands import Option, flag
from discord.ui import Button, View


class Card(commands.Cog):
    api = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='
    db = 'https://db.ygoprodeck.com/card/?search='
    ygorg = 'https://db.ygorganization.com/card#'

    def loadData(self):
        with open('cardIDs.json', 'r') as f:
            self.cardIDs = json.loads(f.read())
        self.names = []

        for i in self.cardIDs:
            self.names.append(i)

    def __init__(self, bot):
        self.bot = bot
        self.loadData()

    def makeUrl(self, card):
        space = card.replace(' ', '%20')
        bracket = space.replace('/', '%2F')
        aps = bracket.replace("'", '%27')
        amp = aps.replace('&', '%26')
        return self.api + amp

    def dbLink(self, card):
        space = card.replace(' ', '%20')
        aps = space.replace("'", '%27')
        amp = aps.replace('&', '%26')
        return self.ygorg + amp

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    @commands.command()
    async def card(self, ctx, card: str):
        """Brings up information about a specified card"""
        try:
            view = View()
            message = await ctx.send('Retrieving card...', ephemeral=True, delete_after=60)

            highest = process.extractOne(card, self.names)
            newCard = highest[0]
            if ('EvilTwin' in newCard or 'LiveTwin' in newCard):
                if ('EvilTwin' in newCard):
                    newCard = newCard.replace('EvilTwin', 'Evil★Twin')
                else:
                    newCard = newCard.replace('LiveTwin', 'Live☆Twin')


            cardData = requests.get(self.makeUrl(newCard)).json()
            dblink = '{0}{1}'.format(self.ygorg, self.cardIDs[newCard.replace('★', '').replace('☆', '')])

            embed = discord.Embed(
                title='**{0}**'.format(cardData['data'][0]['name']), url=dblink, color=0x0000ff)
            try:
                embed.set_author(name='Archetype: {0}'.format(
                    cardData['data'][0]['archetype']))
            except:
                pass
            try:
                embed.set_footer(text='Banlist Status: {0}'.format(
                    cardData['data'][0]['banlist_info']['ban_tcg']))
            except:
                embed.set_footer(text='Banlist Status: Unlimited')

            setPrices = '**__Card Prices:__**\n'

            setPrices = '__Card Price: {0}__'.format(
                cardData['data'][0]['card_prices'][0]['tcgplayer_price'])

            embed.set_thumbnail(
                url=cardData['data'][0]['card_images'][0]['image_url'])
            if ('Trap' not in cardData['data'][0]['type'] and 'Spell' not in cardData['data'][0]['type']):
                if (not 'Link' in cardData['data'][0]['type']):
                    try:
                        embed.add_field(name='**Attribute: {0} | Level: {1} | Scale: {2}**'.format(cardData['data'][0]['attribute'], cardData['data'][0]['level'], cardData['data'][0]['scale']), value='**[ {0} / {1} ]**'.format(
                            cardData['data'][0]['race'], cardData['data'][0]['type'].replace('Monster', '')), inline=False)
                    except:
                        embed.add_field(name='**Attribute: {0} | Level: {1}**'.format(cardData['data'][0]['attribute'], cardData['data'][0]['level']), value='**[ {0} / {1} ]**'.format(
                            cardData['data'][0]['race'], cardData['data'][0]['type'].replace('Monster', '')), inline=False)
                else:
                    embed.add_field(name='**Attribute: {0} | Link Rating: {1}**\n**Link Arrows: {2}**'.format(cardData['data'][0]['attribute'], cardData['data'][0]['linkval'], cardData['data'][0]['linkmarkers']), value='**[ {0} / {1} ]**'.format(
                        cardData['data'][0]['race'], cardData['data'][0]['type'].replace('Monster', '')), inline=False)
                embed.add_field(name='**Card Description**',
                                value=cardData['data'][0]['desc'], inline=False)
                if (not 'Link' in cardData['data'][0]['type']):
                    embed.add_field(name='**ATK: {0} / DEF: {1}**'.format(
                        cardData['data'][0]['atk'], cardData['data'][0]['def']), value=setPrices, inline=False)
                else:
                    embed.add_field(
                        name='**ATK: {0}**'.format(cardData['data'][0]['atk']), value=setPrices, inline=False)
            else:
                embed.add_field(name='**[{0} {1}]**'.format(cardData['data'][0]['race'], cardData['data'][0]['type'].replace(
                    ' Card', '')), value='**Card Description**\n{0}\n\n{1}'.format(cardData['data'][0]['desc'], setPrices, dblink), inline=False)

            cardEncoded = urllib.parse.quote(newCard)

            tcgplayer = Button(label='View on TCGPlayer', url=f'https://www.tcgplayer.com/search/all/product?q={cardEncoded}&view=grid', style=discord.ButtonStyle.link)
            cardMarket = Button(label='View on Card Market', url=f'https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString={cardEncoded}', style=discord.ButtonStyle.link)

            view.add_item(tcgplayer)
            view.add_item(cardMarket)

            await message.edit(content='Retrieved {0}'.format(cardData['data'][0]['name']))
            await ctx.send(embed=embed, view=view)
        except:
            await message.edit(content='<@!174263950685372417> has been notified with the exact **card** you used causing the error')
            user = self.bot.get_user(174263950685372417)
            await user.send(f'The card: **{card}** caused an error')


def setup(bot):
    bot.add_cog(Card(bot))
