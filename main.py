import discord
import os
import io
import json
from elosports.elo import Elo
from discord.ext import commands

elo = Elo(k=20)

f = open('token.txt', 'r')
token = f.readline()
f.close()

with open(r'cogs/users.json', 'r') as f:
    users = json.load(f)

    for i in users:
        elo.addPlayer(i, users[i])

prefix = '.'

bot = commands.Bot(command_prefix=(prefix))

@bot.event
async def on_ready():
    print(bot.user.name, 'logged in')
    print('----------------')
    await bot.change_presence(activity=discord.Game(name='Yu-Gi-Oh! TCG | .help', type=3))

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='All the functions this bot can do', color=0x0000ff)
    embed.add_field(name='{0}card (name)'.format(prefix), value='Brings up information about specified card', inline=False)
    embed.add_field(name='{0}staples'.format(prefix), value='Brings up current staples in the game', inline=False)
    embed.add_field(name='{0}banlist'.format(prefix), value='Brings up the current TCG banlist', inline=False)
    embed.add_field(name='{0}match (winner) (loser)'.format(prefix), value='Displays the new Elo of players involved in a match. Mention the winner first and loser second', inline=False)
    embed.add_field(name='{0}.leaderboard / {0}.lb'.format(prefix), value='Brings up a leaderboard if all players Elo ratings on the server', inline=False)
    embed.add_field(name='{0}.cardList (set name)'.format(prefix), value='Displays the cards in a specified set or structure/starter deck', inline=False)
    await ctx.send(embed=embed)

for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f'{cog} can not be loaded:')
            raise e

bot.run(token)