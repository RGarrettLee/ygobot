import discord
import requests
import json
from discord.ext import commands, tasks

class Updates(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.updateAPICall = 'https://db.ygorganization.com/data/idx/card/name/en'
        self.updateCards.start()

    @tasks.loop(hours=24)
    async def updateCards(self):
        cards = requests.get(self.updateAPICall).json()

        output = {}

        for i in cards:
            name = i
            strencode = name.encode('ascii', 'ignore')
            strdecode = strencode.decode()
            output[strdecode] = cards[i][0]

        with open('cardIDs.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=True, indent=4)

    @updateCards.before_loop
    async def updateCards_before(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Updates(bot))