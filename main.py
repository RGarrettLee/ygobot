import discord
import os
import io
from discord.ext import commands

f = open('token.txt', 'r')
token = f.readline()
f.close()

prefix = '.'

bot = commands.Bot(command_prefix=(prefix))

@bot.event
async def on_ready():
    print(bot.user.name, 'logged in')
    print('----------------')
    await bot.change_presence(activity=discord.Game(name='Yu-Gi-Oh! TCG', type=3))

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='All the functions this bot can do', color=0x0000ff)
    embed.add_field(name='{0}card (name)'.format(prefix), value='Brings up information about specified card', inline=False)
    embed.add_field(name='{0}staples'.format(prefix), value='Brings up current staples in the game', inline=False)
    embed.add_field(name='{0}banlist'.format(prefix), value='Brings up the current TCG banlist', inline=False)
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