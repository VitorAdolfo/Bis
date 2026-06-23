#Carregando bibliotecas

#Bibliotecas para o discord
import discord
from discord.ext import commands

#Bibliotecas para o env
import os
import dotenv

#Biblioteca de manipulação de arquivos
import shutil

#Biblioteca para manipulação de processos
import asyncio

#Biblioteca para captura de audio
import yt_dlp


#Configurando parâmetros para busca
YTDLP_CONFIG = {
    "format":"bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "auto",
    "source_address":"0.0.0.0"
}
ytdlp = yt_dlp.YoutubeDL(YTDLP_CONFIG)

#Configurando parâmetros para reprodução de áudio
FFMPEG_CONFIG = {
    "before_options":"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


#Carregando informações
dotenv.load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

#Configurando permissões
bot_intents = discord.Intents.default()
bot_intents.message_content = True

#Criando Bot
bot = commands.Bot("/",intents=bot_intents)


#Funções auxiliares
def after_play_audio(error:discord.ClientException, bot_object:commands.Bot, server:discord.Guild):
    if error:
        print("[ERROR] Não foi possível iniciar o player")
        print(f"[MOTIVO] {error}")
    asyncio.run_coroutine_threadsafe(check_inactivity(bot_object, server),bot_object.loop)

async def check_inactivity(bot_object, server):
    await asyncio.sleep(30)
    voice_connection = discord.utils.get(bot_object.voice_clients,guild=server)
    if voice_connection and not voice_connection.is_playing():
        await voice_connection.disconnect()


#Eventos
@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.event
async def on_voice_state_update(member:discord.Member,before:discord.VoiceState,after:discord.VoiceState):
    voice = discord.utils.get(bot.voice_clients,guild=member.guild)
    if not voice:
        return
    
    if before.channel == voice.channel:
        if len([actual_member for actual_member in voice.channel.members if not actual_member.bot]) == 0:
            await voice.disconnect()


#Comandos do bot
@bot.tree.command(name="play",description="Toca um áudio ai")
async def play(interaction:discord.Interaction, user_search:str):
    #Verificando se ele esta em um canal de voz
    if not interaction.user.voice:
        await interaction.response.send_message("Entre primeiro em um canal rapaz!")
        return
    
    #Obtendo canal de voz onde o usuário esta
    actual_channel = interaction.user.voice.channel
    
    #Obtendo permissões do bot
    bot_permissions = actual_channel.permissions_for(interaction.guild.me)

    #Verificando e respondendo permissões
    if not bot_permissions.view_channel:
        await interaction.response.send_message("Onde se encontra não posso nem ver!")
        return
    if not bot_permissions.connect:
        await interaction.response.send_message("Não fui permitido neste canal ai rapaz.")
        return
    if not bot_permissions.speak:
        await interaction.response.send_message("Fui probido de expressar minha linda voz!")
        return

    #Procurando vídeo/áudio
    try:
        audio_info = ytdlp.extract_info(user_search,download=False)
        if "entries" in audio_info:
            audio_data = audio_info["entries"][0]
        else:
            audio_data = audio_info
        
        streaming_name = audio_data["title"]
        streaming_url = audio_data["url"]
    
    except Exception as error:
        await interaction.followup.send("Não pude encontrar isso meu filho, perdão...")
        print("[ERRO] Não foi possível encontrar o áudio")
        print(f"[MOTIVO] {error}")
        return

    #Respondendo usuário
    await interaction.response.send_message(f"Preparando batidão: {streaming_name}")

    #Procurando conexões de áudio naquele servidor
    voice_connection = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    #Entrando no canal de voz
    if voice_connection and voice_connection.channel != actual_channel:
        await voice_connection.move_to(actual_channel)
    elif not voice_connection:
        voice_connection = await actual_channel.connect(self_deaf=True, timeout=5.0)
    
    #Encontrando ffmpeg instalado
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        await interaction.followup.send("Estou com alguns problemas tecnicos aqui...")
        print("[ERRO] Caminho para o ffmpeg não foi encontrado")
        return

    #Interrompendo audio anterior
    if voice_connection.is_playing():
        voice_connection.stop()
    
    #Criando e tocando fonte de áudio
    audio_sorce = discord.FFmpegPCMAudio(executable=ffmpeg_path, source=streaming_url, **FFMPEG_CONFIG)
    voice_connection.play(audio_sorce, after=lambda error:after_play_audio(error,bot,interaction.guild))


#Iniciando Bot
bot.run(bot_token)