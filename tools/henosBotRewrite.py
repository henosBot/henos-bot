import discord
from discord.ext import commands

import asyncio
import datetime
import hcolours
import henostools
import traceback

from tools.database import db

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
                name='New Commands Being added'
                )
        )
    
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
        print(f'I just got removed from {guild.name} :)\nIf you want to contact the owner, here is their name and id:\n{guild.owner} ({guild.owner.id})')
    
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
    
    async def on_message(self, message):
        db.open_account(message.author)
        if message.guild == None:
            if message.author != self.user:
                me = self.get_user(self.owner_id)
                await me.send(f'hey henos, I just got sent a message from {message.author.mention}! Here it is:\n{message.content}')
        else:
            xp = db.get(message.author, 'xp')
            level = db.get(message.author, 'level')
            if xp+1 >= 50:
                db.set(message.author, 'xp', 0)
                db.save(message.author, 'level', 1)
                if not db.ignored(message.guild):
                    msg = await message.channel.send(
                        f"Well done {message.author.mention}!! You are now level {level+1}"
                    )
                    await henostools.sleep('10s')
                    try:
                        await msg.delete()
                    except Exception:
                        pass
        await self.process_commands(message)