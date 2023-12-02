# ==============================
# =========== Trabajo ==========
# ==============================

from time import time

from discord import Member
from discord import Embed
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.ext.commands import Bot
from discord.ext.commands import Context

import random

# Personajes relacionados con el trabajo
# Caine: Es el administrador del circo digital
# Jax: Es el alivio comico del circo digital
# Pomni: Es la protagonista del circo digital
# Ragatha: Es la amiga de Pomni
# Kinger: Es el rey del circo digital
# Gangle: Es la chica con doble personalidad del circo digital (Cuando su mascara se rompe, cambia a personalidad triste)
# Zooble: Es la chica que no le importa nada del circo digital

# Tipos de trabajo disponible

MONEDA: str = "<:Bubble:1167495005196263524>"

TIPO_TRABAJOS: list[str] = [
    "Haz encontrado gloings en tu busqueda, has ganado {x} Digital Coins",
    "Dejaste que Jax perdiera su pijama, has ganado {x} Digital Coins",
    "Completaste una tarea de Caine, has ganado {x} Digital Coins",
    "Fuiste al carnaval digital, has ganado {x} Digital Coins",
    "Mientras buscabas Monedas Digitales, encontraste {x} Digital Coins",
    "Caine se le callo su baston y se lo devolviste, has ganado {x} Digital Coins",
    "Ragatha te pidio que le ayudaras a buscar a Pomni, has ganado {x} Digital Coins",
    "Encontraste la llave del cofre de Jax, has ganado {x} Digital Coins",
    "Le ganaste a Kingers en una partida de ajedrez, has ganado {x} Digital Coins",
]


# Comando de trabajo
class EconomyWork(Cog):
    bot: Bot = None
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    # Comando Trabajo
    @command(aliases=["trabajo", "t"])
    async def work(self, ctx: Context, member: Member = None) -> None:
        member = ctx.author
        FirstTime: bool = False

        if not self.bot.economy.UserExists(member):
            self.bot.economy.CreateUser(member)
            FirstTime = True

        # Si el usuario no puede trabajar entonces decirle que debe esperar
        if not self.bot.economy.CanWork(member, 10) and not FirstTime:
            await ctx.send("Debes esperar para poder trabajar de nuevo")
            return
        
        # Obtener el tipo de trabajo
        trabajo: str = random.choice(TIPO_TRABAJOS)
        dinero: int = random.randint(1, 20)
        
        trabajo = trabajo.replace("{x}", str(dinero))
        
        billetera: int = self.bot.economy.GetMoney(member)
        
        self.bot.economy.AddMoney(member, dinero)
        self.bot.economy.ActionWork(member)
        
        embed: Embed = Embed(
            title=f"{member.name} chambeando...",
            description=f"{trabajo} {MONEDA}",
            color=0x33ccff,
        )
        embed.set_footer(text=f"{billetera} (+{dinero}) => {billetera + dinero}")
        
        # Enviar el embed
        await ctx.send(embed=embed)


# Setup
async def setup(bot: Bot) -> None:
    await bot.add_cog(EconomyWork(bot))