import discord
from typing import Optional

from discord.ext import commands
from discord.utils import get


class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(765194100143292426)
        role_id = 765692519702593577
        self.role = get(guild.roles, id=role_id)
    
    @commands.command(name="lockdown")
    async def lockdown_command(self, ctx, target: Optional[discord.TextChannel]):
        target = target or ctx.channel
        await target.set_permissions(ctx.guild.default_role, send_messages=False)
        await target.set_permissions(self.role, send_messages=True)
        await ctx.send("Channel has been updated.")

    @commands.command(name="unlock")
    async def unlock_command(self, ctx, target: Optional[discord.TextChannel]):
        target = target or ctx.channel
        await target.set_permissions(ctx.guild.default_role, send_messages=True)
        await target.set_permissions(self.role, send_messages=True)
        await ctx.send("Channel has been updated.")
        
    @commands.command(name="slowmode")
    async def slowmode_command(self, ctx, seconds: Optional[int]):
        seconds = seconds or None
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
        
def setup(bot):
    bot.add_cog(Lockdown(bot))
