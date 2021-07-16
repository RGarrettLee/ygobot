import discord
import os
import requests
import json
import time
from elosports.elo import Elo
from discord.ext import commands

class Elo(commands.Cog):
    def __init__(self, bot):
        self.elo = Elo(k=20)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open(r'users.json', 'r') as f:
            users = json.load(f)

            await self.update_data(users, member)

            with open(r'users.json', 'w') as f:
                json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open(r'users.json', 'r') as f:
            users = json.load(f)

            if (message.author.bot):
                return
            else:
                await self.update_data(users, message.author)

            with open(r'users.json', 'w') as f:
                json.dump(users, f)

    async def update_data(self, users, user):
        if (not user.id in users):
            self.elo.addPlayer(str(user.id), 1000)
            users[user.id] = {}
            users[user.id]['eloRating'] = self.elo.ratingDict[str(user.id)]
    
    async def probability(self, p1, p2):
        return elo.expectResult(self.elo.ratingDict[p1], self.elo.ratingDict[p2])

    async def eloUpdate(self, p1, p2):
        gameOver(winner = p1, loser = p2, winnerHome = 0)

        with open(r'users.json', 'r') as f:
            users = json.load(f)

            users[p1]['eloRating'] = elo.ratingDict[p1]
            users[p2]['eloRating'] = elo.ratingDict[p2]

            with open(r'users.json', 'w') as f:
                json.dump(users, f) 
    
    @commands.command()
    async def match(self, ctx, *arg):
        winner = arg[0]
        loser = arg[1]
        self.eloUpdate(winner.id, loser.id)

        embed = discord.Embed(title='Match Results', color=0x0000ff)
        embed.add_field('Winner: {0}'.format(winner), value='Elo: {0}'.format(elo.ratingDict[winner.id]), inline=True)
        embed.add_field('Loser: {0}'.format(loser), value='Elo: {0}'.format(elo.ratingDict[loser.id]), inline=True)
        message = ctx.send('Showing match results', embed=embed)

def setup(bot):
    bot.add_cog(Elo(bot))



