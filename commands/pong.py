import discord
from discord import Member
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.ext.commands import Bot
from discord.ext.commands import Context

# Pong
async def pong(bot: Bot) -> str:
    return f"Pong! {round(bot.latency * 1000)}ms"


class CommandPong(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @command()
    async def hola(self, ctx: Context, *, member: Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f"HOLA {(member.name).upper()}~")
        else:
            await ctx.send(f"Hola {member.name}... Yo a vos te conozco.")

        self._last_member = member
    
    @command()
    async def adios(self, ctx: Context, *, member: Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            if member.id == 775371954852986891:
                await ctx.send(f"Pinches putos pendejos, putos pendejos")
            else:
                await ctx.send(f"Adios {member.name} :(")
        else:
            await ctx.send(f"Adios {member.name}... Yo a vos te conozco.")

        self._last_member = member

async def setup(bot: Bot):
    await bot.add_cog(CommandPong(bot))