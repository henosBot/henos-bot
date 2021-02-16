import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils import manage_commands
from tools.other import is_booster, timetext, date
from tools.database import database as db
from io import BytesIO
# import math
# import datetime
# import time

red = discord.Colour.red()

class Utilitys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='info',
        description='shows info on a user',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
            name = "user",
            description = "the user you want to see the info of",
            option_type = 6,
            required = False
        )]
    )
    async def info(self, ctx, member: discord.Member = None):
        member = member if member != None else ctx.author
        embed = discord.Embed(
            title='User Info',
            description='do `hb: info` to get info about you'
            )
        embed.add_field(name='Name:', value=member.name)
        embed.add_field(name='Discriminator:', value=member.discriminator)
        embed.add_field(name='ID:', value=member.id)
        embed.add_field(name='Bot?', value=member.bot)
        embed.add_field(name='Booster?', value=is_booster(member))
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(
        name='userinfo',
        description='shows info on a user',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
            name = "user",
            description = "the user you want to see the info of",
            option_type = 6,
            required = True
        )]
    )
    async def userinfo(self, ctx, user : discord.User):
        embed = discord.Embed(
            title='User Info',
        )
        embed.add_field(name='Name:', value=user.name)
        embed.add_field(name='Discriminator:', value=user.discriminator)
        embed.add_field(name='ID:', value=user.id)
        embed.add_field(name='Bot?', value=user.bot)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='botinfo',
        description='shows info about this bot',
        guild_ids=[740531414008856596]
    )
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title='henos bot',
            description='use `hb: help` for a list of the commands'
            )
        embed.add_field(name='Name:', value=self.bot.user.name)
        embed.add_field(name='Discriminator:', value=self.bot.user.discriminator)
        embed.add_field(name='ID:', value=self.bot.user.id)
        embed.add_field(name='Owner:', value='henos')
        embed.add_field(name='Ping:', value=f'{round(self.bot.latency * 1000)} ms')
        embed.add_field(name='Invite:', value='http://tiny.cc/henosbot')
        embed.add_field(name='Servers:', value=len(self.bot.guilds))
        embed.add_field(name='Members:', value=len(self.bot.users))
        embed.add_field(name='Prefixs:', value='hb: , hb:')
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='serverinfo',
        description='shows info on a server',
        guild_ids=[740531414008856596]
    )
    async def guildinfo(self, ctx):
        embed = discord.Embed(title='Server Info')
        embed.add_field(name='Name:', value=ctx.guild.name)
        embed.add_field(name='ID:', value=ctx.guild.id)
        embed.add_field(name='Channels:', value=len(ctx.guild.channels))
        embed.add_field(name='Members:', value=len(ctx.guild.members))
        embed.add_field(
            name='Boosts:', value=len(ctx.guild.premium_subscribers))
        embed.add_field(name='Owner:', value=ctx.guild.owner.mention)
        welcome_msgs = await db.ignored(ctx.guild, 'welcome_msgs')
        lvl_msgs = await db.ignored(ctx.guild, 'lvl_msgs')
        embed.add_field(name='Interaction disabled?', value=f'Welcome: {welcome_msgs}, Level: {lvl_msgs}')
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='disableinteraction',
        description='disables interaction in a server',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
            name = "type",
            description = "the type of thing u want to disable",
            option_type = 3,
            required = True
        )]
    )
    @commands.has_permissions(manage_guild=True)
    async def disableinteraction(self, ctx, type):
        await db.guild_set(ctx.guild, type, False)
        await ctx.send(f'Guild {ctx.guild.name} has disabled {type} messages.')
    
    @cog_ext.cog_slash(
        name='enableinteraction',
        description='enables interaction in a server',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
            name = "type",
            description = "the type of thing u want to enable",
            option_type = 3,
            required = True,
            choices=[
                manage_commands.create_choice(
                    name='level',
                    value='lvl'
                ),
                manage_commands.create_choice(
                    name='welcome',
                    value='welcome'
                )]
        )]
    )
    @commands.has_permissions(manage_guild=True)
    async def enableinteraction(self, ctx, type):
        await db.guild_set(ctx.guild, type, True)
        await ctx.send(f'Guild {ctx.guild.name} has enabled {type} messages.')
    
    @commands.command()
    @commands.is_owner()
    async def text(self, ctx, user : discord.User, *, message):
        msg = await user.send('Incoming text message from my owner...')
        await msg.edit(content=f'Message: {message}')
        await ctx.send('Message sent successfully')
    
    @cog_ext.cog_slash(
        name='roles',
        description='shows all the roles in a server',
        guild_ids=[740531414008856596]
    )
    @commands.guild_only()
    async def roles(self, ctx):
        allroles = ""

        for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
            allroles += f"[{str(num).zfill(2)}] {role.id}\t{role.name}\t[ Users: {len(role.members)} ]\r\n"

        data = BytesIO(allroles.encode('utf-8'))
        await ctx.send(content=f"Roles in **{ctx.guild.name}**", file=discord.File(data, filename=f"{timetext('Roles')}"))

    @cog_ext.cog_slash(
        name='joinedat',
        description='show when a user joined ur server',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
                name='user',
                description='the user to see the `joinedat` of',
                option_type=6,
                required=False
            )]
    )
    @commands.guild_only()
    async def joinedat(self, ctx, user: discord.Member = None):
        user = user or ctx.author

        embed = discord.Embed()
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = f'**{user}** joined **{ctx.guild.name}**\n{date(user.joined_at)}'
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='mods',
        description='shows the mods that are currently online',
        guild_ids=[740531414008856596]
    )
    @commands.guild_only()
    async def mods(self, ctx):
        message = ""
        all_status = {
            "online": {"users": [], "emoji": "🟢"},
            "idle": {"users": [], "emoji": "🟡"},
            "dnd": {"users": [], "emoji": "🔴"},
            "offline": {"users": [], "emoji": "⚫"}
        }

        for user in ctx.guild.members:
            user_perm = ctx.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(f"**{user}**")

        for g in all_status:
            if all_status[g]["users"]:
                message += f"{all_status[g]['emoji']} {', '.join(all_status[g]['users'])}\n"

        await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")
    
    # @commands.command(aliases=['startuptime', 'uptime'])
    # async def botstats(self, ctx):
    #     uptime = datetime.datetime.utcnow() - self.bot.uptime
    #     days = math.floor(uptime.days)
    #     seconds = math.floor(uptime.seconds)
    #     uptime = uptime.seconds
    #     hours = math.floor(uptime / 3600)
    #     minutes = math.floor(uptime / 60)
    #     embed = discord.Embed(
    #       title='Bot Statistics:',
    #       description=f'__Uptime:__\n{days}d {hours}h {minutes}m {seconds}s\n__Startup time:__\n{self.bot.startuptime.seconds}s'
    #     )
    #     await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Utilitys(bot))