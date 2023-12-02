# ============================
# ====== Obtener Perfil ======
# ============================

from discord import Member
from discord import Embed
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import MemberConverter

# Perfil
class EconomyProfile(Cog):
    bot: Bot = None
    MemberConverter: MemberConverter = None
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.MemberConverter = MemberConverter()
    
    # Comando Perfil
    @command(aliases=["perfil", "p"], help="Muestra la informacion de tu perfil")
    async def profile(self, ctx: Context, *, member: Member = None) -> None:
        author: Member = ctx.author
        member: Member = None
        
        # Si se esta mencionando a un usuario, entonces obtener su perfil
        if ctx.message.mentions:
            member = ctx.message.mentions[0]

        if not member:
            member = author
        
        # Si el usuario no existe entonces crearlo
        if not self.bot.economy.UserExists(member):
            self.bot.economy.CreateUser(member)
        
            
        profile: Embed = self.bot.economy.GetProfile(member)
        await ctx.send(embed=profile)

# Setup
async def setup(bot: Bot) -> None:
    await bot.add_cog(EconomyProfile(bot))