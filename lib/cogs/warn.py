import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json

with open('./data/db/reports.json', "r", encoding='utf-8') as f:
    try:
        report = json.load(f)
    except ValueError:
        report = {}
        report['users'] = []

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def warn(self, ctx,user:discord.Member,*reason:str):
        if not reason:
            await ctx.send(":no_entry: Please provide a reason!")
            return
        reason = ' '.join(reason)
        for current_user in report['users']:
            if current_user['id'] == user.id:
                current_user['reasons'].append(reason)
                if len(current_user['reasons']) >= 3:
                    await user.send("You got kicked for the 3rd warning. The next warning will be an instant ban.")
                    await user.kick(reason=f"{reason} | 3rd warning")
                elif len(current_user['reasons']) >= 4:
                    await user.ban(reason=f"{reason} | 4th warning")
                break
        else:
            report['users'].append({
            'id':user.id,
            'name': user.name,
            'reasons': [reason,]
            })
        with open('./data/db/reports.json','w') as f:
            json.dump(report,f, indent=4)
        
        embed = discord.Embed(
            name="Warned",
            description=f"{user.mention} warned by the moderator {ctx.author.mention}. At: {ctx.message.created_at}",
            color=ctx.author.color
        )
        await ctx.send(embed=embed)
    
    @commands.command(pass_context = True)
    async def warnings(self, ctx,user:discord.Member):
        for current_user in report['users']:
            if user.id == current_user['id']:
                await ctx.send(f"{user.name} has been reported `{len(current_user['reasons'])}` times. Reasons: `{','.join(current_user['reasons'])}`")
                break
        else:
            await ctx.send(f":no_entry: {user.name} has never been reported!")  

def setup(bot):
    bot.add_cog(Warn(bot))