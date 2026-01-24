import discord
from discord.ext import commands, tasks
from gtts import gTTS
import os

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---  RECORDATORIO POR HORA ---
@tasks.loop(hours=1.0)
async def recordatorio_llave():
    # Busca un canal llamado 'general' o usa el primero disponible para el recordatorio
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="general")
        if channel:
            await channel.send("⏰ **RECORDATORIO :** ¡No olvides revisar y cerrar bien todas las llaves de agua! 💧")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    if not recordatorio_llave.is_running():
        recordatorio_llave.start()

def crear_mp3(texto, nombre):
    tts = gTTS(text=texto, lang="es")
    tts.save(nombre)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    texto_usuario = message.content.lower().strip().replace("!", "")

    # --- MENÚ PRINCIPAL ---
    if texto_usuario == "agua":
        await message.channel.send(
            "💧 **Menú de Cuidado del Agua**\n"
            "Escribe una opción:\n"
            "🟢 **ahorro**\n"
            "🟢 **fugas**\n"
            "🟢 **basura**\n"
            "🟢 **reciclar**\n"
            "🟢 **campañas**\n"
            "🔵 **recoleccion** (Lluvia y Rocío)\n"
            "🔵 **tanques** (Limpieza y Mantenimiento)"
        )
        return

    # --- DATOS ---
    datos = {
        
        "recoleccion": (
            "Para lluvia, usa canaletas en techos hacia tanques. Para rocío, usa mallas atrapanieblas o superficies metálicas frías.",
            "https://ecohabitar.org/aprovechamiento-de-agua-de-lluvia/"
        ),
        "tanques": (
            "Limpia tus tanques cada 6 meses con agua y un poco de cloro. Manténlos siempre tapados para evitar mosquitos y algas.",
            "https://cruzroja.org.ar/blog/como-limpiar-el-tanque-de-agua-guia-para-desinfectar-paso-a-paso/"
        ),
        "ahorro": ("Cerrar el grifo ahorra 12 litros por minuto.", 
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

        await message.channel.send(f"🌱 **{texto_usuario.upper()}**\n{mensaje}")
        await message.channel.send(url_imagen)

        if os.path.exists(nombre_audio):
            await message.channel.send(file=discord.File(nombre_audio))
            os.remove(nombre_audio)

    await bot.process_commands(message)
bot.run("TOKEN ")

