import asyncio
import datetime
from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

import aiohttp
import discord
import discord.utils
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import (CheckFailure, Cog, Greedy,
                                  bot_has_permissions, command,
                                  has_permissions)
from discord.utils import get
from pytz import timezone


class mod(commands.Cog):
    '''Praktische Befehle für Administratoren und Moderatoren'''

    def __init__(self, bot):
        self.bot = bot

    def _currenttime(self):
        return datetime.datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")

    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def unban(self, ctx, user: int=None, *reason):
        user = discord.User(id=user)
        if user is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await ctx.guild.unban(user, reason=reason)
        else:
            await ctx.send('**:no_entry:** No user provided!')

    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def bans(self, ctx):
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID":21}{"Name":25} Reason\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName #:robot: emoji
                reason = str(entry.reason) #Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c) #Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:negative_squared_cross_mark:** No banned users!')

    @commands.command(alias=['clearreactions'])
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def removereactions(self, ctx, messageid : str):
        message = await self.bot.get_message(messageid)
        if message:
            await message.clear_reactions()
        else:
            await ctx.send('**:x:** could not find a message with this ID!')

    @commands.command()
    async def permissions(self, ctx):
        permissions = ctx.channel.permissions_for(ctx.me)

        embed = discord.Embed(title=':customs:  Permissions', color=0x3498db) #Blue
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool == True:
                value = ':white_check_mark:'
            else:
                value = ':x:'
            embed.add_field(name=item, value=value)

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def hierarchy(self, ctx):
        msg = f'Role list for **{ctx.guild}**:\n\n'
        roleDict = {}

        for role in ctx.guild.roles:
            if role.is_default():
                roleDict[role.position] = 'everyone'
            else:
                roleDict[role.position] = role.name

        for role in sorted(roleDict.items(), reverse=True):
            msg += role[1] + '\n'
        await ctx.send(msg)

    @commands.command(alies=['setrole', 'sr'])
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def setrank(self, ctx, member: discord.Member=None, *rankName: str):
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.add_roles(rank)
            await ctx.send(f':white_check_mark: Role **{rank.name}** gave to **{member.name}**')
        else:
            await ctx.send(':no_entry: You need to provide a user!')

    @commands.command(pass_context=True, alies=['rmrole', 'removerole', 'removerank'])
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def rmrank(self, ctx, member: discord.Member=None, *rankName: str):
        rank = discord.utils.get(ctx.guild.roles, name=' '.join(rankName))
        if member is not None:
            await member.remove_roles(rank)
            await ctx.send(f':white_check_mark: Role **{rank.name}** removed from **{member.name}**')
        else:
            await ctx.send(':no_entry: You need to provide a user!')
    
    async def kick_members(self, message, targets, reason):
        for target in targets:
            if (message.guild.me.top_role.position > target.top_role.position 
                and not target.guild_permissions.administrator):
                await target.kick(reason=reason)

                embed = Embed(title="Member kicked:",
                                colour=0xDD2222,
                                timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
                            ("Moderator", message.author.display_name, False),
                            ("Reason  ", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                
                await message.channel.send(embed=embed)
            

    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send(":no_entry: One or more arguments are missing!")

        else:
            await self.kick_members(ctx.message, targets, reason)

    @kick_command.error
    async def kick_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send(":no_entry: You don't meet the requirements to use this command!")

    async def ban_members(self, message, targets, reason):
        for target in targets:
            if (message.guild.me.top_role.position > target.top_role.position 
                and not target.guild_permissions.administrator):
                await target.ban(reason=reason)

                embed = Embed(title="Member banned:",
                                colour=0xDD2222,
                                timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
                            ("Moderator", message.author.display_name, False),
                            ("Reason", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                
                await message.channel.send(embed=embed)

    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send(":no_entry: One or more arguemts are missing!")

        else:
            await self.ban_members(ctx.message, targets, reason)

    @ban_command.error
    async def ban_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send(":no_entry: You don't meet the requirements to use this command!")

    @command(name="clear", aliases=["purge"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
                                                    check=_check)

                await ctx.send(f"`{len(deleted):,}` deleted messages.", delete_after=10)

        else:
            await ctx.send(":no_entry: The limit is 100 messages!")


def setup(bot):
    bot.add_cog(mod(bot))
