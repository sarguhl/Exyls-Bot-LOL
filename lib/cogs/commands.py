import datetime
import platform
import time
from datetime import datetime, timedelta
from platform import python_version
from time import time

import discord
from discord import __version__ as discord_version
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="stats")
    async def stats(self, ctx):
        start_time = time.time()
        current_time = time.time()
        difference = int(round(current_time - start_time))
        up_time_out = str(datetime.timedelta(seconds=difference))
        
        embed = discord.Embed(
            title="Stats",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Servers:", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Uptime", value=up_time_out, inline=True)
        embed.add_field(name="All Members", value=str(len(self.bot.users)), inline=True)
        embed.add_field(name="Python version:", value=str(platform.python_version()), inline=True)
        embed.add_field(name="Discord version:", value=discord_version, inline=True)
        embed.add_field(name="Bot version:", value=self.bot.VERSION, inline=True)
        embed.add_field(name='Team:', value='Owner/Programmer: Sarguhl#1337\nAdministrator: Steinhose#2867', inline=True)
        embed.set_footer(text="Bot Version: " + self.bot.VERSION)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + up_time_out)

def setup(bot):
    bot.add_cog(Commands(bot))