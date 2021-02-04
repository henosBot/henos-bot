import os

token = os.get_env('TOKEN')

import discord
from discord.ext import commands
from tools.henosBotRewrite import henosBotRewrite
from tools.database import db

import time

bot = henosBotRewrite()
# bot.set_embed_color(discord.Colour.red())
bot.owner_id = 717633235789807657

# bot.remove_command('help')
# botextentions = [
#     'cogs.economy',
#     'cogs.rank',
#     'cogs.utils',
#     'cogs.tsos',
#     'cogs.music',
#     'cogs.fun',
#     'cogs.moderation',
#     'cogs.help',
#     'cogs.image',
#     'cogs.emoji',
#     'jishaku'
# ]
# for extension in botextentions:
#     bot.load_extension(extension)
#     print(f'{extension} loaded succesfuly')

# time.sleep(5)
# os.system('clear')

bot.run(token)