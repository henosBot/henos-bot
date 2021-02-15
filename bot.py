import os
import dotenv
import jishaku

os.system('pip install -r requirements.txt')

dotenv.load_dotenv()
token = os.getenv('TOKEN')

import discord
from tools.henosBotRewrite import henosBotRewrite
from discord_slash import SlashCommand

import time

bot = henosBotRewrite()
bot.slash = SlashCommand(bot, sync_commands=True)
bot.set_embed_color(discord.Colour.red())
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

bot.load_extension('jishaku')
bot.load_extension('cogs.economy')
bot.run(token)