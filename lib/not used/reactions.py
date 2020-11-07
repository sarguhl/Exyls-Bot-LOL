import discord
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.forbidden_reactions = ["🖕", "🤬", "😡", "🤮", "💩", "👺", "🤢", "🍆"]
        self.announcement_channel = self.bot.get_channel(707544941554827265)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.channel_id == self.announcement_channel.id:
            for emoji in self.forbidden_reactions:
                if payload.emoji.name == emoji:
                    message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, payload.member)

def setup(bot):
    bot.add_cog(Reactions(bot))