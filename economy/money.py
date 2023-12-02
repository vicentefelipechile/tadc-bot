# ==============================
# =========== Dinero ===========
# ==============================

from time import time

from discord import Member
from discord import Embed
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.ext.commands import Bot
from discord.ext.commands import Context

import random


# Comandos de dinero
class EconomyMoney(Cog):
    bot: Bot = None
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    # Mostrar cuanto dinero tiene el usuario
    @command(aliases=["dinero", "d"])
    async def money(self, ctx: Context, *, member: Member = None) -> None:
        member = ctx.author
        
        if not self.bot.economy.UserExists(member):
            self.bot.economy.CreateUser(member)
        
        money: int = self.bot.economy.GetMoney(member)
        
        embed: Embed = Embed(
            title = "Dinero Digital",
            description = f"{member.mention} tiene {money} Digital Coins",
            color = 0x2d85c8,
            timestamp = ctx.message.created_at,
            )
        
        await ctx.reply(embed=embed)
    
    # Depositar el dinero en el banco
    @command(aliases=["depositar", "dep"])
    async def deposit(self, ctx: Context, amount: int | str = None) -> None:
        member: Member = ctx.author
        amount: int = amount if type(amount) == int else "todo"

        # Si la cantidad es 0 significa que depositara todo el dinero
        if amount == "todo":
            amount = self.bot.economy.GetMoney(member)

        # Si el usuario no tiene dinero entonces no depositar nada
        if amount == 0:
            await ctx.reply("No tienes dinero para depositar")
            return

        result: bool = self.bot.economy.MoneyToBank(member, amount)
        
        if result:
            embed: Embed = Embed(
                title = "Deposito",
                description = f"{member.mention} deposito {amount} Digital Coins",
                color = 0x2d85c8,
                timestamp = ctx.message.created_at,
                )
            
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("No tienes suficiente dinero para depositar")

async def setup(bot: Bot) -> None:
    await bot.add_cog(EconomyMoney(bot))