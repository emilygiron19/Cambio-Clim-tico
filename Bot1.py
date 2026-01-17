import discord
from discord.ext import commands
from gtts import gTTS
import os

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

def crear_mp3(texto, nombre):
    tts = gTTS(text=texto, lang="es")
    tts.save(nombre)

# COMANDO PRINCIPAL
@bot.command()
async def hola(ctx):
    texto = (
        "El agua potable es esencial para la vida. "
        "Escribe una opción para aprender más: "
        "ahorro, fugas, basura, reciclar o campañas."
    )
    audio = "agua.mp3"
    crear_mp3(texto, audio)

    await ctx.send(
        "💧 **Cuidado del agua potable**\n\n"
        "Escribe una opción para aprender más:\n"
        "🟢 **ahorro**\n"
        "🟢 **fugas**\n"
        "🟢 **basura**\n"
        "🟢 **reciclar**\n"
        "🟢 **campañas**"
    )
    await ctx.send(file=discord.File(audio))
    os.remove(audio)

# RESPUESTAS INTERACTIVAS
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Limpieza de texto (quita el ! y espacios)
    texto_usuario = message.content.lower().strip().replace("!", "")

    # Diccionario con mensajes y ENLACES DE GOOGLE/INTERNET
    datos = {
        "ahorro": (
            "Cerrar el grifo mientras te lavas los dientes o enjabonas los platos ahorra hasta 12 litros por minuto.",
            "https://satecma.es/wp-content/uploads/2018/03/ahorrar-agua.jpg"
        ),
        "fugas": (
            "Una gotera pequeña puede desperdiciar miles de litros al año. ¡Repara tus tuberías!",
            "https://i0.wp.com/hidrotecnia.com/wp-content/uploads/2021/05/fuga-agua.jpg"
        ),
        "basura": (
            "No tires basura ni químicos en el desagüe; todo eso termina contaminando nuestros ríos.",
            "https://cnnespanol.cnn.com/wp-content/uploads/2021/06/210608121404-01-plastic-pollution-ocean-restricted-full-169.jpg"
        ),
        "reciclar": (
            "Reciclar el aceite usado y separar los plásticos evita que los residuos lleguen a las fuentes de agua.",
            "https://blog.retema.es/uploads/noticias/imagenes/63c52e42095f7.jpg"
        ),
        "campañas": (
            "Unirse a grupos de limpieza y educación ambiental ayuda a proteger el futuro del planeta.",
            "https://elperiodicodesaltillo.com/wp-content/uploads/2023/06/limpieza-rio.jpg"
        )
    }

    if texto_usuario in datos:
        mensaje, url_imagen = datos[texto_usuario]
        nombre_audio = f"{texto_usuario}.mp3"

        crear_mp3(mensaje, nombre_audio)

        # 1. Enviamos el texto
        await message.channel.send(f"🌱 **{texto_usuario.upper()}**\n{mensaje}")
        
        # 2. Enviamos la imagen como un enlace (Discord la mostrará automáticamente)
        await message.channel.send(url_imagen)

        # 3. Enviamos el audio
        if os.path.exists(nombre_audio):
            await message.channel.send(file=discord.File(nombre_audio))
            os.remove(nombre_audio)

    await bot.process_commands(message)

bot.run("MTQxODk4ODA4NDI3MTM4MjUzOA.GV_Gm4.dQC9uOeBx9YSidHJpZZhdOFRKFgtStir3uqLs4")