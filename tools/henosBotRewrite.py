import discord
from discord.ext import commands

import asyncio
import datetime
import hcolours
import henostools
import traceback
import random
import logging

from tools.database import database as db

loop = asyncio.get_event_loop()
runtime = datetime.datetime.now()
intents = discord.Intents.default()
intents.members = True

class henosBotRewrite(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('hb; ', 'hb;'),
            intents=intents,
            loop=loop,
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name='Bot being rewrited'
                )
        )
        self.blacklisted = [
            110373943822540800,
            446425626988249089,
            645357850893221918,
            450100127256936458,
            264445053596991498,
            374071874222686211,
            336642139381301249
        ]
    
    async def on_ready(self):
        print(f'{self.user} ({self.user.id}) is online!')
        startuptime = datetime.datetime.now()
        self.startuptime = startuptime - runtime
        print(f'Startup time is {self.startuptime.seconds} seconds')
        await henostools.sleep('1m')
        print(
            f'{hcolours.colour.red}Guild Count:{hcolours.reset} {len(self.guilds)}')
        print(
            f'{hcolours.colour.red}Member Count:{hcolours.reset} {len(self.users)}')
        print(f'Invite url: {discord.utils.oauth_url(self.user.id, permissions= discord.Permissions(permissions=8))}')
        print(f'Owner: {self.get_user(self.owner_id)}')
        print(f'Shards: ({len(self.shards)})')
    
    async def on_resume(self):
        print(f'{self.user} ({self.user.id}) has resumed')
    
    async def on_connect(self):
        print(f'{self.user} ({self.user.id}) has connected')
        self.uptime = datetime.datetime.utcnow()
    
    async def on_shard_connect(self, shard_id):
        print(f'{self.user}\'s {shard_id} has connected')
    
    async def on_disconnect(self):
        print(f'{self.user} ({self.user.id}) has disconnected')
        runtime = datetime.datetime.now()
    
    async def on_shard_disconnect(self, shard_id):
        print(f'{self.user}\'s {shard_id} has disconnected')
    
    async def on_shard_resume(self):
        print(f'{self.user} ({self.user.id}) has resumed')
    
    async def on_shard_ready(self, shard_id):
        print(f'{self.user}\'s {shard_id} is ready')
    
    async def on_guild_join(self, guild):
        try:
            channel = guild.system_channel
            embed = discord.Embed(
                title=f'Hello {guild.name}',
                description=
                f"I'm {self.user} ({self.user.mention})\nThanks for adding me to your server"
            )
            embed.set_footer(text='Use `hb: help` to get a list of my commands')
            await channel.send(embed=embed)
        except Exception:
            pass
        finally:
            me = self.get_user(self.owner_id)
            await me.send(f'''Woo hoo!
            I just got added to {guild.name}!!
            In case you need to contact the owner of the server, here is their name and id:
            {guild.owner} ({guild.owner.id})
            ''')
    
    async def on_guild_remove(self, guild):
        me = self.get_user(self.owner_id)
        await me.send(f'I just got removed from {guild.name} :)\nIf you want to contact the owner, here is their name and id:\n{guild.owner} ({guild.owner.id})')
    
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown) and not isinstance(
                error, commands.CommandNotFound) and not isinstance(error, commands.MissingRequiredArgument) and not isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Oh no!',
                description=
                f'There was a error with the {ctx.command.name} command\n\nError: {error}')
            await ctx.send(embed=embed)
            await ctx.send(f'Traceback: {traceback.format_exc()}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'This command is on a cooldown. Please wait {round(error.retry_after)} seconds'
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You are missing the required argument `{error.param.name}`. Please try again with it.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error)
        else:
            if not isinstance(error, commands.CommandNotFound):
                await ctx.send(error)
    
    async def on_error(self, event, *args, **kwargs):
        print(f'Something went wrong!\nThe error happened in {event} event\nDetails: {args}\n{kwargs}')
        print('Traceback:', logging.warning(traceback.format_exc()))
    
    async def on_message(self, message):
        if message.guild.id not in self.blacklisted:
            await db.open_account(message.author)
            await db.open_guild_account(message.guild)
            if message.guild == None:
                if message.author != self.user:
                    me = self.get_user(self.owner_id)
                    await me.send(f'hey henos, I just got sent a message from {message.author.mention}! Here it is:\n{message.content}')
            else:
                xp = await db.get(message.author, 'xp')
                level = await db.get(message.author, 'level')
                if xp+1 >= 50:
                    await db.set(message.author, 'xp', 0)
                    await db.save(message.author, 'level', 1)
                    if not db.ignored(message.guild, 'lvl_msgs'):
                        msg = await message.channel.send(
                            f"Well done {message.author.mention}!! You are now level {level+1}"
                        )
                        await henostools.sleep('10s')
                        try:
                            await msg.delete()
                        except Exception:
                            pass
        await self.process_commands(message)
    
    async def on_command_completion(self, ctx):
        chance = random.randrange(0, 40)
        ttt = [
            'hi, im dumb', 'jkdvbekjcnejcbne', 'blah blah blah', 'blabity blab',
            'henos bot is THE BEST', 'kjdcijnr', 'kcnec ekcjeovcie ecojecioe',
            'keceivcjhrnvi', '129048907393', '1234567890', '0987654321',
            '(*%&^%%^*&*%)'
        ]
        tttc = random.choice(ttt)
        if chance == 1:
            await ctx.send(f'Common Event time!!\npls type `{tttc}`')
            amount = random.randrange(10, 100)
        elif chance == 10:
            await ctx.send(f'Uncommon Event time!!\npls type `{tttc}`')
            amount = random.randrange(50, 200)
        elif chance == 20:
            await ctx.send(f'Rare Event time!!\npls type `{tttc}`')
            amount = random.randrange(100, 500)
        elif chance == 30:
            await ctx.send(f'Legendary Event time!!\npls type `{tttc}`')
            amount = random.randrange(500, 2000)
        elif chance == 40:
            await ctx.send(f'Mythic Event time!!\npls type `{tttc}`')
            amount = random.randrange(1000, 5000)
        else:
            return

        def check(msg):
            return msg.content == tttc

        msg = await self.wait_for('message', check=check)
        if msg:
            await db.save(msg.author, 'wallet', amount)
            await ctx.send(
                f'Congrats {msg.author.mention}!, you got {amount} dollars')
        else:
            await ctx.send('Too bad :(, nothing for you')
    
    async def on_member_join(self, member):
        if member.guild.id not in self.blacklisted:
            channel = member.guild.system_channel
            if not db.ignored(member.guild, 'welcome_msgs'):
                if not member.bot:
                    try:
                        await channel.send(
                            f'Hi {member.name}, welcome to {member.guild.name}!, use `hb: help` to get a list of the commands'
                        )
                    except Exception:
                        pass

    async def on_member_remove(self, member):
        if member.guild.id not in self.blacklisted:
            channel = member.guild.system_channel
            if not db.ignored(member.guild, 'welcome_msgs'):
                if not member.bot:
                    try:
                        await channel.send(
                            f'Awww, {member} just left {member.guild.name} :('
                        )
                    except Exception:
                        pass