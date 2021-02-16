import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from tools.database import database as db
from discord_slash import cog_ext
from discord_slash.utils import manage_commands
import tools.amounts

import typing
import random
import henostools

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)
    
    @cog_ext.cog_slash(
        name='balance',
        description='Sees your, or another user\'s balance',
        guild_ids=[740531414008856596],
        options=[
            manage_commands.create_option(
            name = "user",
            description = "the user you want to see the balance of",
            option_type = 6,
            required = False
        )]
    )
    async def balance(self, ctx, user : typing.Union[discord.Member, discord.User] = None):
        await ctx.respond()
        user = user or ctx.author
        wallet = await db.get(user, 'wallet')
        bank = await db.get(user, 'bank')
        embed = discord.Embed(
            title=f'{user}\'s balance',
            description=f'__Wallet:__ {wallet}\n__Bank:__ {bank}\n__Total:__ {wallet + bank}'
        )
        await ctx.send(embeds=[embed])
    
    @cog_ext.cog_slash(
        name='beg',
        description='begs for money',
        guild_ids=[740531414008856596],
    )
    async def beg(self, ctx):
        amount = random.randrange(100, 500)
        await ctx.send(f'Someone gave you {amount} dollars')
        await db.save(ctx.author, 'wallet', amount)
    
    @cog_ext.cog_slash(
        name='daily',
        description='get your daily dollars',
        guild_ids=[740531414008856596],
    )
    async def daily(self, ctx):
        amount = 3000
        await ctx.send(f'You got {amount} dollars')
        await db.save(ctx.author, 'wallet', amount)

    @cog_ext.cog_slash(
        name='deposit',
        description='deposits some money',
        guild_ids=[740531414008856596],
        options=manage_commands.create_option(
            name = "amount",
            description = "the amount you want to deposit",
            option_type = 3,
            required = False
        )
    )
    async def deposit(self, ctx, amount):
        wallet = await db.get(ctx.author, 'wallet')
        bank = await db.get(ctx.author, 'bank')
        amount = amount if amount != 'all' else wallet
        if amount >= wallet:
            await db.save(ctx.author, 'bank', amount)
            await db.remove(ctx.author, 'wallet', amount)
            await ctx.send(f'You deposited {amount} dollars into your bank')
        else:
            await ctx.send('You do not have enough money in your wallet')
    
    @cog_ext.cog_slash(
        name='withdraw',
        description='withdraws some money',
        guild_ids=[740531414008856596],
        options=manage_commands.create_option(
            name = "amount",
            description = "the amount you want to withdraw",
            option_type = 3,
            required = False
        )
    )
    async def withdraw(self, ctx, amount):
        wallet = await db.get(ctx.author, 'wallet')
        bank = await db.get(ctx.author, 'bank')
        amount = amount if amount != 'all' else bank
        if amount >= bank:
            await db.save(ctx.author, 'wallet', amount)
            await db.remove(ctx.author, 'bank', amount)
            await ctx.send(f'You withdrawed {amount} dollars from your bank')
        else:
            await ctx.send('You do not have enough money in your bank')
    
    @cog_ext.cog_slash(
        name='work',
        description='work for money',
        guild_ids=[740531414008856596],
    )
    async def work(self, ctx):
        jobs = [
            'Janitor', 'Computer Programmer', 'Landscape Architect', 'Referee',
            'Teacher', 'Security Guard', 'Truck Driver', 'Plumber', 'Reporter',
            'Dancer', 'Vet', 'Chef', 'Childcare worker', 'Mason',
            'Electrician', 'Librarian', 'Writer', 'Bus Driver', 'Artist',
            'Accountant', 'CEO'
        ]
        amount = random.randrange(100, 5000)
        await db.save(ctx.author, 'wallet', amount)
        embed = discord.Embed(
            title=f'{ctx.author.name} worked!',
            description=f'You worked as a {random.choice(jobs)} and got {amount} dollars')
        embed.set_footer(text='Well done!! 👏')
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(
        name='hh',
        description='give someone some help',
        guild_ids=[740531414008856596],
    )
    async def hh(self, ctx):
        amount = random.randrange(10, 500)
        await ctx.send(f'You helped someone and got {amount} dollars in return')
        await db.save(ctx.author, 'wallet', amount)

    @cog_ext.cog_slash(
        name='search',
        description='search for money',
        guild_ids=[740531414008856596],
    )
    async def search(self, ctx):
        c1 = ['bed', 'discord', 'tree', 'street']
        c2 = ['car', 'bed', 'wallet', 'pantry',]
        c3 = ['shop', 'bushes', 'bin']
        choices = [random.choice(c1), random.choice(c2), random.choice(c3)]
        await ctx.send(f'Where do you want to search? Pick from the list below and type it in chat.\n`{choices[0]}, {choices[1]}, {choices[2]}`')

        def search_check(msg):
            return msg.content in choices and msg.author.id == ctx.author.id

        msg = await self.bot.wait_for('message', check=search_check)
        amount = random.randrange(100, 500)
        if msg:
            await db.save(ctx.author, 'wallet', amount)
            await ctx.send(f'{ctx.author.mention} **Searched the:** `{msg.content}`\nYou found {amount} dollars!')
        else:
            await ctx.send('thats not a valid option')

    @cog_ext.cog_slash(
        name='gamble',
        description='gamble some money',
        guild_ids=[740531414008856596],
    )
    async def gamble(self, ctx, amount: int):
        wallet = await db.get(ctx.author, 'wallet')
        if int(wallet) >= amount:
            chance = ['win', 'lose']
            chance = random.choice(chance)
            em1 = discord.Embed(
                title=f"{ctx.author.name}'s gambling game!!",
                description='Will you win?')
            msg = await ctx.send(embed=em1)
            await henostools.sleep('2s')
            await msg.delete()
            msg2 = await ctx.send('Rolling now ...')
            if chance == 'win':
                amount2 = amount + 500
                amount = random.randrange(amount, amount2)
                await db.save(ctx.author, 'wallet', amount)
                await msg2.edit(content=f'You Won!!\n\nYou got {amount} dollars!!')
            else:
                amount2 = amount + 500
                amount = random.randrange(amount, amount2)
                await db.remove(ctx.author, 'wallet', amount)
                await msg2.edit(content=f'You lost ):\n\n{amount} dollars was removed from your account')
        else:
            await ctx.send("You don't have enough money. Please try again")
    
    @cog_ext.cog_slash(
        name='lottery',
        description='enter the lottery for a chance to win over 2 million dollars',
        guild_ids=[740531414008856596],
    )
    async def lottery(self, ctx):
        await ctx.send('Are you sure you want to enter the lottery??\nEnter `yes` or `no`')

        def lottcheck(msg):
            return msg.content.lower().startswith('y') and msg.author.id == ctx.author.id

        msg = await self.bot.wait_for('message', check=lottcheck)
        if msg:
            await db.remove(ctx.author.id, 'wallet', 100)
            amount = random.randrange(100000, 2000000)
            chance = random.randrange(1, 2000)
            await ctx.send('Drumroll please ...')
            await henostools.sleep('10s')
            if chance == 100:
                await ctx.send(f'Congrats!!!\n\nYou won the lottery and got {amount} dollars')
                await db.save(ctx.author, 'wallet', amount)
            else:
                await ctx.send('Sooo close!!\nPlay again for the chance to win over 2 million dollars!!')
        else:
            await ctx.send('Goodbye')
    
    @cog_ext.cog_slash(
        name='shop',
        description='',
        guild_ids=[740531414008856596],
    )
    async def shop(self, ctx):
        colours = discord.Embed(
            title='Colours',
            description=
            'Every colour costs `50,000`\n**Colours:**\n- `red`\n- `blue`\n- `green`\n- ` orange`\n- `pink`\n- `purple`\n- `gray`\n- `black`\nTo buy a role type `hb: buy colour <colour>`\n\nYou can also buy a custom colour for 100,000, use `hb:  buy customcolour <hexcode>`')
        await ctx.send(embed=colours)
        items = discord.Embed(
            title='Items',
            description=
            '- `Cookie` | 100 dollars\n- `Chocolate` | 500 dollars\n- `Coin` | 1,000 dollars\n- `Rare Coin` | 5,000 dollars\n- `Medal` | 10,000 dollars\n- `Rare Medal` | 50,000 dollars\n- `Trophy` | 100,000 dollars\n- `Rare Trophy` | 500,000 dollars\n- `Ultra Collectable Thingy` | 1,000,000 dollars\n\nUse `hb: buy item <item>`')
        await ctx.send(embed=items)
    
    @commands.group()
    async def buy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid catagory.\nExample: `hb: buy item Chocolate` (`hb: buy <catagory> <item>`)')
    
    @buy.command()
    async def colour(self, ctx, *, colour : discord.Colour):
        try:
            role = discord.utils.get(ctx.guild.roles, name=colour.__name__)
        except:
            role = await ctx.guild.create_role(name=colour.__name__, colour=colour)
        wallet = await db.get(ctx.author, 'wallet')
        if int(wallet) >= 50000:
            await db.remove(ctx.author, 'wallet', 50000)
            await ctx.author.add_roles(role, reason='colour role add')
            await ctx.send(f'Gave you the colour {colour}!\nEnjoy!!')
        else:
            await ctx.send("You don't have enough money to buy this colour :(")

    @buy.command()
    async def item(self, ctx, *, item):
        item = item.lower()
        wallet = db.get(ctx.author)
        if int(wallet) >= tools.amounts(item):
            await db.buy_item(ctx.author, item)
            await ctx.send(f'Congrats, You bought a {item}')
        else:
            await ctx.send(
                "You don't have enough money to buy this item :(")

    @buy.command()
    async def customcolour(self, ctx, colour : discord.Colour):
        wallet = db.get(ctx.author, 'wallet')
        if wallet >= 100000:
            await db.remove(ctx.author, 'wallet', 100000)
            role = await ctx.guild.create_role(
                name=f'{ctx.author.name} - {colour}', colour=colour)
            await ctx.author.add_roles(role, reason='custom colour role add')
            await ctx.send(f'Gave you the colour {colour}\nEnjoy!!')
        else:
            await ctx.send("You don't have enough money to buy this :(")

def setup(bot):
    bot.add_cog(Economy(bot))