import discord
from discord.ext import commands
from tools.database import database as db
from discord_slash import cog_ext
from discord_slash.utils import manage_commands

import typing

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)
    
    @cog_ext.cog_slash(
        name='rank',
        description='Sees your, or another user\'s rank',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
            name = "user",
            description = "the user you want to see the rank of",
            option_type = 6,
            required = False
        )]
    )
    async def rank(self, ctx, user : typing.Union[discord.Member, discord.User] = None):
        await ctx.respond()
        user = user or ctx.author
        xp = await db.get(user, 'xp')
        level = await db.get(user, 'level')
        embed = discord.Embed(
            title=f'{user}\'s rank',
            description=f'__XP:__ {xp}\n__Level:__ {level}'
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Rank(bot))