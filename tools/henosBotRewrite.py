import discord
from discord.ext import commands

import asyncio
import datetime
import hcolours
import henostools

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