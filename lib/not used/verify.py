import discord
from discord.ext import commands
from discord.utils import get

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        un_role_id = 772214907894235196
        ver_role_id = 772214976135823381
        guild = self.bot.get_guild(772213334070001685)
        
        self.un_role = get(guild.roles, id=un_role_id)
        self.ver_role = get(guild.roles, id=ver_role_id)
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(self.un_role)
    
    @commands.command(name="gamejam")
    @commands.has_role(772214907894235196)
    async def verify_command(self, ctx):
        await ctx.message.delete()
        await ctx.author.add_roles(self.ver_role)
        await ctx.author.remove_roles(self.un_role)
        await ctx.author.send("Welcome in!")

def setup(bot):
    bot.add_cog(Verify(bot))
        