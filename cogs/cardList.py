import discord
import os
import json
import time
from discord.ext import commands

class CardList(commands.Cog):
    api = ''
    oneTime = 'ttps://db.ygoprodeck.com/api/v7/cardsets.php'
    msgID = 0

    def __init__(self, bot):
        self.sets = requests.get(oneTime).json()
        self.setDB = {}
        self.bot = bot
        self.page = 0

    def tupleConvert(self, word):
        str = ' '.join(word)
        return str.lower()

    def makeUrl(self, product):
        space = product.replace(' ', '%20')

    def extractSets(self):
        for i in range(len(self.sets)):
            name = data[i]['set_name'].lower()
            name = name.replace('structure deck:', '')
            name = name.replace('structure deck', '')
            name = name.replace('starter deck', '')
            name = name.replace('starter deck:', '')
            name = name.strip()
            code = data[i]['set_code']
            self.setDB[name] = code

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(oayload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name

        if ((emoji == '\N{Leftwards Black Arrow}' or emoji == '\N{Black Rightwards Arrow}') and not str(user) == 'YugiBot#5373'):
            if (message.id == self.msgID):
                if (emoji == '\N{Leftwards Black Arrow}' and self.page >= 0):
                    self.page -= 1
                    if (self.page <= 0): self.page = 0
                    # TODO: INSERT EMBED FOR GOING BACKWARDS A PAGE
                    # await message.edit(embed=embed)
                    # await message.remove_reaction(emoji, user)
                elif (emoji == '\N{Black Rightwards Arrow}' and self.page < len(self.pages)):
                    self.page += 1
                    if (self.page == len(self.pages)): self.page = len(self.pages)
                    #TODO: INSERT EMBED FOR GOING FORWARDS A PAGE
                    # await message.edit(embed=embed)
                    # await message.remove_reaction(emoji, user)

    @commands.command()
    async def cardList(self, ctx, *arg):
        if (len(setDB) < 1):
            self.extractSets()
        try:
            product = self.tupleConvert(arg)
            message = await ctx.send('Retrieving list for {0}...'.format(product))
            productData = requests.get(self.makeUrl(card)).json()