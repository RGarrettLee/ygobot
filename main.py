import discord
import os
import io
from discord.ext import commands

f = open('token.txt', 'r')
token = f.readline()
f.close()

prefix = '.'

intents = discord.Intents().all()
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix=(prefix), intents=intents, slash_commands=True)

@bot.event
async def on_ready():
    print(bot.user.name, 'logged in')
    print('----------------')
    await bot.change_presence(activity=discord.Game(name='Yu-Gi-Oh! TCG | /card', type=3))

bot.remove_command('help')

for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f'{cog} can not be loaded:')
            raise e

bot.run(token)