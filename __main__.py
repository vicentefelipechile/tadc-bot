# ==========================================================================
# ===================== Discord Bot (TADC) - Main File =====================
# ==========================================================================

print("=========================================")
print("Inicializando bot...")
print("=========================================")

import os
import dotenv
dotenv.load_dotenv()

DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX: str = os.getenv("DISCORD_PREFIX")


QUE_DICT: dict[bool] = {
    "que": True,
    "qe": True,
    "q": True,
    "k": True,
    "ke": True,
}

RRA_DICT: dict[bool] = {
    "rra": True,
    "ra": True,
}

HOLA_DICT: dict[bool] = {
    "hola": True,
    "hla": True,
    "ola": True,
    "holi": True,
    "oli": True,
}


# ==========================================================================
# =============================== Bot Client ===============================
# ==========================================================================

# Librerias
import discord
from discord import app_commands
from database.database_class import DiscordDatabase

# Clases
from discord import File
from discord import Embed
from discord import Intents
from discord import Interaction
from discord.app_commands import CommandTree
from discord.ext.commands import Bot
from discord.ext.commands import Context


# Intents
intents:                    Intents = discord.Intents.default()
intents.members:            bool = True
intents.presences:          bool = True
intents.message_content:    bool = True

# ==========================================================================
# ================================ Ejecucion ===============================
# ==========================================================================

database:       DiscordDatabase = DiscordDatabase()
bot:            Bot = Bot(intents=intents, command_prefix=DISCORD_PREFIX)

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")

@bot.event
async def on_ready() -> None:
    await load_extensions()
    await bot.tree.sync()
    
    print("=========================================")
    print(f"Bot iniciado correctamente - {bot.user}")
    print("=========================================")

Yatesalude: dict[int | bool] = {}

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    contenido: str = None

    database.user_add(message.author)

    try:
        contenido = message.content.lower()
    except:
        pass
    
    
    if HOLA_DICT.get(contenido):
        mensaje: str = f"# ¡HOLA {message.author.name.upper()}! #"
        
        if Yatesalude.get(message.author.id):
            mensaje = f"Ya te salude cabron"
        elif message.author.id == 775371954852986891:
            mensaje = f"# PINCHES PUTOS PENDEJOS, PUTOS PENDEJOS"
        
        Yatesalude[message.author.id] = True
        
        await message.reply(mensaje)

    if QUE_DICT.get(contenido):
        # Crear un embed con titulo "so" y un a imagen ubicada en "img/so.jpg"

        embed: Embed = Embed(title=" ")
        embed.set_image(url="https://i.imgur.com/3ZD5yvb.jpg")

        await message.channel.send(embed=embed)

    elif RRA_DICT.get(contenido):
        embed: Embed = Embed(title="sos")
        embed.set_image(url="https://i.imgur.com/tn57RMC.png")

        await message.channel.send(embed=embed)

    elif contenido == "vos":

        embed: Embed = Embed(title="...")
        embed.set_image(url="https://i.imgur.com/jU3ug3z.png")

        await message.channel.send(embed=embed)

    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)