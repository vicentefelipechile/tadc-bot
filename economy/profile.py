# ============================
# ====== Obtener Perfil ======
# ============================

from discord import Member
from discord import Embed
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.ext.commands import Bot
from discord.ext.commands import Context

from .economy_enum import ECONOMY_USER_GET

# Perfil
class EconomyProfile(Cog):
    bot: Bot = None
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    # Comando Perfil
    @command(aliases=["perfil", "p"])
    async def profile(self, ctx: Context, member: Member = None) -> None:
        # Si no se especifica un usuario entonces se toma el usuario que ejecuto el comando
        if ctx.message.mentions:
            member = ctx.message.mentions[0]
        else:
            member = ctx.author
        
        # Si el usuario no existe entonces crearlo
        if not self.bot.economy.UserExists(member):
            self.bot.economy.CreateUser(member)
            
            
        profile: Embed | None = self.bot.economy.GetProfile(member)
        
        if profile is None:
            await ctx.send("La persona m")
            return
        
        await ctx.send(embed=profile)

# Setup
async def setup(bot: Bot) -> None:
    await bot.add_cog(EconomyProfile(bot))