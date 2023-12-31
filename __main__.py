# ==========================================================================
# ===================== Discord Bot (TADC) - Main File =====================
# ==========================================================================

print("=========================================")
print("Inicializando bot...")
print("=========================================")

import os
import random
import dotenv
import time
dotenv.load_dotenv()

DISCORD_TOKEN:          str = os.getenv("DISCORD_TOKEN")
DISCORD_PREFIX:         str = os.getenv("DISCORD_PREFIX")
MEDIA_PATH:             str = os.getenv("MEDIA_PATH")

GUILD_ID:               int = int(os.getenv("GUILD_ID"))
GENERAL_ID:             int = int(os.getenv("GENERAL_ID"))

HD_RESPONSE_X_MIN:        int = int(os.getenv("HD_RESPONSE_X_MIN"))
HD_RESPONSE_X_MAX:        int = int(os.getenv("HD_RESPONSE_X_MAX"))
HD_RESPONSE_Y_MIN:        int = int(os.getenv("HD_RESPONSE_Y_MIN"))
HD_RESPONSE_Y_MAX:        int = int(os.getenv("HD_RESPONSE_Y_MAX"))


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
    "oal": True,
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


COMO_DICT: dict[str | bool] = {
    "como": True,
    "cmo": True,
    "como?": True,
    "com?": True,
}



# ==========================================================================
# =============================== Bot Client ===============================
# ==========================================================================

# Librerias
import discord
from database.database_class import DiscordDatabase
from economy.economy_class import ModuloEconomia

# Clases
from discord import Embed
from discord import Intents
from discord import Member
from discord.ext.commands import Bot


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

bot.economy:    ModuloEconomia = ModuloEconomia()

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")
    
    # Cargar comandos de economia
    for filename in os.listdir("./economy"):
        if filename.endswith(".py"):
            if f"economy.{filename[:-3]}" in ("economy.economy_class", "economy.economy_enum"):
                continue
            await bot.load_extension(f"economy.{filename[:-3]}")

@bot.event
async def on_ready() -> None:
    await load_extensions()
    await bot.tree.sync()

    print("=========================================")
    print(f"Bot iniciado correctamente - {bot.user}")
    print("=========================================")
    
    # Canal = bot.get_channel(GENERAL_ID)
    # Mensaje = input("Mensaje: ")
    # await Canal.send(Mensaje)

Yatesalude: dict[int | bool] = {}
BLACKLIST: list[str] = [
    643099106419671041
]

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:              return

    database.user_add(message.author)
    if message.author.id in BLACKLIST:  return

    contenido: str = None
    try:                                contenido = message.content.lower()
    except:                             pass


    if random.randint(1, 80) <= 5:
        if not bot.economy.UserExists(message.author):
            bot.economy.CreateUser(message.author)
        
        # Se escoge una cantidad aleatoria de monedas entre 1 y 100
        monedas: int = random.randint(1, 100)
        
        # Se le añade la cantidad de monedas al usuario
        bot.economy.AddMoney(message.author, monedas)
        
        # Se le envia un mensaje al usuario
        await message.channel.send(f"¡{message.author.mention} has ganado {monedas} Digital Coins! <:Bubble:1167495005196263524>")
        


    if HOLA_DICT.get(contenido):
        mensaje: str = f"# ¡HOLA {message.author.name.upper()}!"
        
        if Yatesalude.get(message.author.id):           mensaje = f"Ya te salude cabron"
        elif message.author.id == 775371954852986891:   mensaje = f"Hola, supongo"
        
        Yatesalude[message.author.id] = True
        
        await message.reply(mensaje)

    if QUE_DICT.get(contenido):
        embed: Embed = Embed(title=" ").set_image(url=MEDIA_PATH + "img/so.jpg")
        await message.reply(embed=embed)


    elif RRA_DICT.get(contenido):
        embed: Embed = Embed(title="sos").set_image(url=MEDIA_PATH + "img/sos.png")
        await message.reply(embed=embed)


    elif contenido == "vos":
        embed: Embed = Embed(title="...").set_image(url=MEDIA_PATH + "img/vos.png")
        await message.reply(embed=embed)


    elif ADIOS_DICT.get(contenido):
        embed: Embed = Embed(title="Hola").set_image(url=MEDIA_PATH + "img/hola.png")
        await message.reply(embed=embed)


    elif COMO_DICT.get(contenido):
        embed: Embed = Embed(title="Verga").set_image(url=MEDIA_PATH + "img/verga.png")
        await message.reply(embed=embed)


    elif "te amo" in contenido:
        embed: Embed = Embed(title=" ").set_image(url=MEDIA_PATH + "img/teamo.png")
        await message.reply(embed=embed)


    elif contenido == "puto":
        await message.add_reaction("😢")


    elif message.attachments:
        for attachment in message.attachments:
            if attachment.height and attachment.width:
                if ( HD_RESPONSE_Y_MIN < attachment.height < HD_RESPONSE_Y_MAX ) and ( HD_RESPONSE_X_MIN < attachment.width < HD_RESPONSE_X_MAX ):
                    img = random.randint(1, 11)
                    img: str = MEDIA_PATH + f"img/hd/hd{img}.png"
                    
                    embed: Embed = Embed(title="FULL HD 4K").set_image(url=img)
                    
                    await message.reply(embed=embed)
                    break

    if message.channel.id == GENERAL_ID:
        if message.reference:
            mensaje: discord.Message = await message.channel.fetch_message(message.reference.message_id)
            print(f"{time.strftime('%H:%M:%S', time.localtime())} > {message.author.name.rjust(16)} : {(mensaje.content[:25] + '...').ljust(25)} - {message.content}")
        else:
            print(f"{time.strftime('%H:%M:%S', time.localtime())} > {message.author.name.rjust(16)} : {message.content}")

    if random.randint(1, 100) == 1:
        await message.channel.send("Simplemente no lo entiendo")


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