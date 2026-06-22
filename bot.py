#Carregando bibliotecas

#Bibliotecas para o discord
import discord
from discord.ext import commands

#Bibliotecas para o env
import os
import dotenv

#Biblioteca de manipulação de arquivos
import shutil

#Carregando informações
dotenv.load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

#Configurando permissões
bot_intents = discord.Intents.default()
bot_intents.message_content = True

#Criando Bot
bot = commands.Bot("/",intents=bot_intents)

#Comandos do Bot
@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="play",description="Toca um áudio ai")
async def play(interaction:discord.Interaction):
    #Verificando se ele esta em um canal de voz
    if not interaction.user.voice:
        await interaction.response.send_message("Entre primeiro em um canal rapaz!")
        return
    
    #Obtendo canal de voz do usuário
    voice_channel = interaction.user.voice.channel
    
    #Obtendo permissões do bot
    bot_permissions = voice_channel.permissions_for(interaction.guild.me)

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

    #Procurando conexões de áudio naquele servidor
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    #Respondendo usuário
    await interaction.response.send_message("Preparando batidão: tome.mp3")

    #Entrando no canal de voz
    if voice and voice.channel != voice_channel:
        await voice.move_to(voice_channel)
    elif not voice:
        voice = await voice_channel.connect(self_deaf=True, timeout=5.0)
    
    #Encontrando ffmpeg instalado
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        await interaction.followup.send("Estou com alguns problemas tecnicos aqui...")
        print("[ERRO] Caminho para o ffmpeg não foi encontrado")
        return

    #Caminho para o áudio de teste
    test_audio_path = "assets/tome.mp3"
    if voice.is_playing():
        voice.stop()
    
    #Criando e tocando fonte de áudio
    audio_sorce = discord.FFmpegPCMAudio(executable=ffmpeg_path, source=test_audio_path)
    voice.play(audio_sorce)

#Iniciando Bot
bot.run(bot_token)