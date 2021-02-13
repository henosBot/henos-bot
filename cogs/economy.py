import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from tools.database import database as db
import tools.amounts

import typing
import random
import henostools

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(alisases=['bal'])
    async def balance(self, ctx, user : typing.Union[discord.Member, discord.User]):
        user = user or ctx.author
        wallet = db.get(user, 'wallet')
        bank = db.get(user, 'bank')
        embed = discord.Embed(
            title=f'{user.mention}\'s balance',
            description=f'__Wallet:__ {wallet}\n__Bank:__ {bank}\n__Total:__ {wallet + bank}'
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def beg(self, ctx):
        amount = random.randrange(100, 500)
        await ctx.send(f'Someone gave you {amount} dollars')
        await db.save(ctx.author, 'wallet', amount)
    
    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        amount = 3000
        await ctx.send(f'You got {amount} dollars')
        await db.save(ctx.author, 'wallet', amount)

    @commands.command(aliases=['dep'])
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
    
    @commands.command(aliases=['with'])
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
    
    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
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
            description=
            f'You worked as a {random.choice(jobs)} and got {amount} dollars')
        embed.set_footer(text='Well done!! 👏')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['helping_hand'])
    @commands.cooldown(1, 60, BucketType.user)
    async def hh(self, ctx):
        amount = random.randrange(10, 500)
        await ctx.send(f'You helped someone and got {amount} dollars in return')
        await db.save(ctx.author, 'wallet', amount)

    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
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

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
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
    
    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
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
    
    @commands.command(aliases=['store'])
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