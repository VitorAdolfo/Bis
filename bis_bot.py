#Carregando bibliotecas
import discord
from discord.ext import commands

import os
import dotenv

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
    if not interaction.user.voice:
        await interaction.response.send_message("Entre em um canal rapaz!")
        return
    
    voice_channel = interaction.user.voice.channel
    
    #Verificando permissões do bot
    bot_permissions = voice_channel.permissions_for(interaction.guild.me)

    if not bot_permissions.view_channel:
        await interaction.response.send_message("Onde se encontra não posso nem ver!")
        return
    if not bot_permissions.connect:
        await interaction.response.send_message("Não fui permitido neste canal ai rapaz.")
        return
    if not bot_permissions.speak:
        await interaction.response.send_message("Fui probido de expressar minha linda voz!")
        return

    await interaction.response.send_message("Adentrando no canal!")
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    if voice:
        await voice.move_to(voice_channel)
    else:
        voice = await voice_channel.connect()

#Iniciando Bot
bot.run(bot_token)