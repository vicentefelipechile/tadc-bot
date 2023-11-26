# ==========================================================================
# ===================== Discord Bot (TADC) - Main File =====================
# ==========================================================================

print("=========================================")
print("Inicializando bot...")
print("=========================================")

import os
import dotenv
import time
dotenv.load_dotenv()

DISCORD_TOKEN:          str = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX:         str = os.getenv("DISCORD_PREFIX")
MEDIA_PATH:             str = os.getenv("MEDIA_PATH")

GUILD_ID:               int = int(os.getenv("GUILD_ID"))
GENERAL_ID:             int = int(os.getenv("GENERAL_ID"))

QUE_DICT: dict[str | bool] = {
    "que": True,
    "qe": True,
    "q": True,
    "k": True,
    "ke": True,
}

RRA_DICT: dict[str | bool] = {
    "rra": True,
    "ra": True,
}

HOLA_DICT: dict[str | bool] = {
    "hola": True,
    "hla": True,
    "ola": True,
    "holi": True,
    "oli": True,
}

ADIOS_DICT: dict[str | bool] = {
    "adios": True,
    "chau": True,
    "chao": True,
    "bye": True,
    "bai": True,
    "nos vemos": True,
    "nos vemo": True,
    "nos vemoz": True,
    "no vemos": True,
    "no vemo": True,
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
from discord import Member
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
            mensaje = f"# Te quiero zamuz"
        
        Yatesalude[message.author.id] = True
        
        await message.reply(mensaje)

    if QUE_DICT.get(contenido):
        # Crear un embed con titulo "so" y un a imagen ubicada en "img/so.jpg"

        embed: Embed = Embed(title=" ")
        embed.set_image(url=MEDIA_PATH + "img/so.jpg")

        await message.channel.send(embed=embed)

    elif RRA_DICT.get(contenido):
        embed: Embed = Embed(title="sos")
        embed.set_image(url=MEDIA_PATH + "img/sos.png")

        await message.channel.send(embed=embed)

    elif contenido == "vos":

        embed: Embed = Embed(title="...")
        embed.set_image(url=MEDIA_PATH + "img/vos.png")

        await message.channel.send(embed=embed)
    
    elif ADIOS_DICT.get(contenido):
        embed: Embed = Embed(title="Hola").set_image(url=MEDIA_PATH + "img/hola.png")
        
        await message.reply(embed=embed)
        
        
    # Si el mensaje contiene una imagen, obtener la resolucion de la imagen, si la imagen esta entre el rango 65x65 y 300x300 enviar un embed respondiendo: "¿Que no habia en hd?"
    if message.attachments:
        for attachment in message.attachments:
            if attachment.height and attachment.width:
                if 65 < attachment.height < 300 and 65 < attachment.width < 300:
                    embed: Embed = Embed(title="¿Que no habia en hd?").set_image(url=MEDIA_PATH + "img/hd.jpeg")
                    
                    await message.reply(embed=embed)
                    break
    
        

    await bot.process_commands(message)


@bot.event
async def on_member_join(member: Member) -> None:
    # Detectar si el servidor es igual al servidor de discord (GUILD_ID)
    
    if member.guild.id != GUILD_ID:
        return
    
    embed: Embed = Embed(title=f"¡Bienvenido {member.name} al servidor de El Asombroso Circo digital!")
    
    Imagen: str = MEDIA_PATH + "img/welcome/normal.png"
    # Si la fecha actual es diciembre se enviara un mensaje con la imagen MEDIA_PATH + "img/welcome/navidad.png"
    if time.localtime().tm_mon == 12:
        Imagen = MEDIA_PATH + "img/welcome/navidad.png"
    
    embed.set_image(url=Imagen)

    await bot.get_channel(GENERAL_ID).send(embed=embed)


bot.run(DISCORD_TOKEN)