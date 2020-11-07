import datetime as DT
import pathlib
from pathlib import Path

import discord
from discord import DMChannel, Embed, Guild, Member
from discord.errors import Forbidden, HTTPException
from discord.ext import commands, tasks
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandOnCooldown, Context,
                                  MissingPermissions, NotOwner, command,
                                  when_mentioned_or)
from discord.ext.commands.errors import (BadArgument, CommandNotFound,
                                         MissingRequiredArgument)
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
intents.presences = True

currentDT = DT.datetime.now()
OWNER_IDS = [703686351111061605]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    prefix = ">"
    return when_mentioned_or(prefix)(bot, message)

class Ready(object):
    def __init__(self):
        print("Ready up")

# Main class
class Bot(BotBase):
    def __init__(self):
        self.guild = None
        self.ready = False
        
        self._cogs = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
        
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS, intents=intents)
        
    def setup(self):
        self.remove_command("help")
        
        print("running setup...")
        
        for cog in self._cogs:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"loaded {cog} cog")
        
        print("setup complete.")
        
    def run(self, version):
        self.VERSION = version
        with open("./data/token.txt", "r", encoding="utf-8") as f:
            self.TOKEN = f.read()
        
        self.setup()
        
        print("bot running...")
        
        super().run(self.TOKEN)
    
    async def on_connect(self):
        print("bot connected to the API")
    
    async def on_disconnect(self):
        print("bot disconnected from the API")
            
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")
        
        #await self.log.send("CAPAINT! WE GOT AN ERROR!")
        raise
    
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
            
        elif isinstance(exc, MissingRequiredArgument):
            embed = Embed(
                title="Error",
                description="One or more arugments are missing."
            )
            await ctx.send(embed=embed)
        
        elif isinstance(exc, CommandOnCooldown):
            embed = Embed(
                title="Error",
                description="Command on cooldown plase wait a few seconds."
            )
            await ctx.send(embed=embed)
        
        elif isinstance(exc, NotOwner):
            embed = Embed(
                title="Error",
                description="You're not the owner of the bot."
            )
            await ctx.send(embed=embed)
        
        elif isinstance(exc.original, Forbidden):
            embed = Embed(
                title="Error",
                description="I do not have the required permissions to execute that commmand."
            )
            await ctx.send(embed=embed)
        
        else:
            raise exc
    
    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(747177901715357788)
            self.log = self.get_channel(747178230812770355)
            self.ready = True
            
            meta = self.get_cog("Meta")
            await meta.set()
            
            
            print("Bot is now ready to work.")
            
            
            #await self.log.send("Bot is now online!")
        else:
            print("bot reconnected.")
        
bot = Bot()