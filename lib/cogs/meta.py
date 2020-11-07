from datetime import datetime, timedelta
from platform import python_version
from time import time
from itertools import cycle
from discord.ext import commands, tasks


from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command



class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

        self._message = "playing with Exyl"
        print("LOG: status set: inited")

    @property
    def message(self):
        return self._message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
            raise ValueError("Invalid activity type.")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.bot.change_presence(activity=Activity(
            name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
        ))

    @command(name="setactivity")
    @commands.is_owner()
    async def set_activity_message(self, ctx, *, text: str):
        self.message = text
        await self.set()
        await ctx.send(f"Status set to: {text}")
        print(f"LOG: status set: setactivity by: {ctx.author.name}")

    @command(name="ping")
    async def ping(self, ctx):
        start = time()
        message = await ctx.send(f"Pong! DWSP latency: {self.bot.latency*1000:,.0f} ms.")
        end = time()

        await message.edit(content=f"Pong! DWSP latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

def setup(bot):
	bot.add_cog(Meta(bot))