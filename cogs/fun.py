from discord.ext import commands, menus  #, tasks
import discord
import random
import henostools
import time
import aiohttp
import tools
import faker
from phone_gen import PhoneNumber
import sr_api
from discord_slash import cog_ext
from discord_slash.utils import manage_commands

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.faker = faker.Faker()
        self.srapi = sr_api.Client()

    # stuff
    @cog_ext.cog_slash(
        name='invite',
        description='shows the bot\'s invite'
    )
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Invites:',
            description=
            'Bot: [tiny.cc/henosbot](https://tiny.cc/henos_bot)\nHelp Server: [tiny.cc/hb_help_server](https://tiny.cc/hb_help_server)')
        await ctx.send(embed=embed)

    # fun
    @cog_ext.cog_slash(
        name='poll',
        description='creates a poll'
        options=[
            manage_commands.create_option(
                name='reaction1',
                description='the first reaction',
                option_type=0,
                required=True
            ),
            manage_commands.create_option(
                name='reaction2',
                description='the second reaction',
                option_type=0,
                required=True
            ),
            manage_commands.create_option(
                name='poll',
                description='the poll',
                option_type=0,
                required=True
            ),
        ]
    )
    async def poll(self, ctx, r1, r2, *, pollctx):
        embed = discord.Embed(
            title="__Poll!__",
            description=f'{pollctx}'
            )
        embed.set_footer(text=f'Poll by {ctx.author.name}#{ctx.author.discriminator} | React with {r1} or {r2} to vote')
        message = await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        await message.add_reaction(r1)
        await message.add_reaction(r2)

    @cog_ext.cog_slash(
        name
    )
    async def hack(self, ctx, user: discord.Member):
        ends = [
            'gmail.com', 'hotmail.com', 'outlook.com', 'optusnet.net',
            'bigpond.com'
        ]
        email = f'{user.name}{random.randrange(1000, 9999)}@{random.choice(ends)}'
        times = random.randrange(8, 20)
        chars = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_-+={}|[],./<>?~`'
        password = ''
        for x in range(times):
            password += random.choice(chars)
        countrys = ['Australia', 'America', 'Italy', 'England', 'Russia', 'Brazil']
        message = await ctx.send(f'Hacking {user.mention} ...')
        embed = discord.Embed(
          title=f'Succesfully Hacked {user}!',
          description=f'{ctx.author.mention}: Here is what i got from discord\'s DB'
        )
        countrys = random.choice(countrys)
        phnum = PhoneNumber(countrys)
        phnum = phnum.get_number()
        device = random.choice(['PC', 'Laptop', 'Mac', 'Phone', 'Windows', 'Linux', 'Chrome', 'Browser', 'Edge', 'Firefox', 'Opera'])
        userobj = await self.bot.fetch_user(user.id)
        embed.add_field(name='Login:', value=f'```Email: {email}\nPassword: {password}\nPhone Number: {phnum}```', inline=False)
        embed.add_field(name='Personal:', value=f'```IP: {self.faker.ipv4()}\nCountry: {countrys}\nCurrent Device: {device}```', inline=False)
        embed.add_field(name='Discord Stuff:', value=f'```ID: {user.id}\nUsername: {user.name}\nNickname: {user.nick}\nToken: {await self.srapi.bot_token()}\nActivity: {user.activity}\nStatus: {user.status}\nTotal Servers: {random.randrange(1, 100)}\nJoined Discord At: {(userobj.created_at).strftime("%d %b %Y %I:%M")}```', inline=False)
        await henostools.sleep('10s')
        await message.edit(embed=embed)

    @commands.command()
    async def giveaway(self, ctx, duration, *, prize):
        try:
            await ctx.message.delete()
        except:
            pass
        embed = discord.Embed(
            title='Giveaway!! 🎉',
            description=
            f'__**Prize**__: {prize}\n__**Duration**__: {duration}\n__**Hosted by**__: {ctx.author.mention}')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        await henostools.sleep(duration)
        message = await ctx.channel.fetch_message(msg.id)
        for reaction in message.reactions:
            if str(reaction.emoji) == '\U0001f389':
                reaction = reaction
        users = await reaction.users().flatten()
        users.remove(self.bot.user)
        winner = random.choice(users)
        embed2 = discord.Embed(
            title='Giveaway Ended',
            description=
            f'__**Winner**__: {winner.mention}\n__**Hosted by**__: {ctx.author.mention}')
        await message.edit(embed=embed2)
        await ctx.send(
            f'Congrats {winner.mention}, you won {prize}!!\nhttps://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}\n({ctx.author.mention})'
        )

    @commands.command()
    async def embedify(self, ctx, titletag, title, bodytag, body, footertag, footer, colourtag, colour : discord.Colour):
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(
            title=title,
            description=body,
            colour=colour
        )
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command()
    async def reactify(self, ctx, messageid: int, *reactions):
        await ctx.channel.purge(limit=1)
        message = await ctx.channel.fetch_message(messageid)
        for reaction in reactions:
            await message.add_reaction(reaction)

    # ping
    @commands.command()
    async def ping(self, ctx):
        pings = []
        number = 0
        typings = time.monotonic()
        await ctx.trigger_typing()
        typinge = time.monotonic()
        typingms = round((typinge - typings) * 1000)
        pings.append(typingms)
        latencyms = round(self.bot.latency * 1000)
        pings.append(latencyms)
        discords = time.monotonic()
        url = "https://discordapp.com/"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = r
            if resp.status == 200:
                discorde = time.monotonic()
                discordms = round((discorde-discords)*1000)
                pings.append(discordms)
                discordms = f"{discordms}ms"
            else:
                discordms = "Failed"
        for ms in pings:
            number += ms
        average = round(number / len(pings))
        embed = discord.Embed(
          title='__Pong:__',
          description=f'Typing: `{typingms}ms`  |  Latency: `{latencyms}ms`\nDiscord: `{discordms}`  |  Average: `{average}ms`'
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def kill(self, ctx, user : discord.Member = None):
        if user == None:
            await ctx.send(f'{ctx.author.mention} just got stabbed \U0001f52a')
        else:
            await ctx.send(f'{ctx.author.mention} just stabbed {user.mention} \U0001f52a')
    
    @commands.command()
    async def reverse(self, ctx, *, text: str):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        async with ctx.channel.typing():
            try:
                url = 'https://api.urbandictionary.com/v0/define'
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url, params={'term': search}) as r:
                        resp = await r.json()
            except Exception as e:
                return await ctx.send(f'Urban API returned invalid data... might be down atm.\nError: `{e}`')
            
            sortlist = sorted(resp['list'], reverse=True, key=lambda g: int(g["thumbs_up"]))
            urbanmenu = tools.UrbanMenu()
            await urbanmenu.start(ctx, sortlist)
    
    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, IndexError):
            return await ctx.send('No results were found :(')
        elif isinstance(error, discord.HTTPExeption):
            return await ctx.send('Definition is to long for discord to process\nSorry :(')
        else:
            return


def setup(bot):
    bot.add_cog(fun(bot))