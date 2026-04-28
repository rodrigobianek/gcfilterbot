import discord
import asyncio
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("TOKEN")
CANAL_DESTINO_ID = int(os.getenv("CANAL_DESTINO_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    if "https://gamersclub.com.br" in message.content:
        canal_destino = bot.get_channel(CANAL_DESTINO_ID)

        if canal_destino:
            await canal_destino.send(
                f"📥 Mensagem movida de {message.channel.mention}\n"
                f"👤 {message.author.mention}\n"
                f"💬 {message.content}"
            )

            # Opcional: apagar mensagem original
            # await message.delete()

    await bot.process_commands(message)

bot.run(TOKEN)

@bot.command()
async def scan(ctx):
    await ctx.send("🔍 Iniciando varredura...")

    canal_destino = bot.get_channel(CANAL_DESTINO_ID)

    count = 0

    async for message in ctx.channel.history(limit=None):
        if "https://gamersclub.com.br" in message.content:
            await canal_destino.send(
                f"📥 (Histórico)\n"
                f"👤 {message.author.mention}\n"
                f"💬 {message.content}"
            )
            count += 1

    await ctx.send(f"✅ Finalizado! {count} mensagens encontradas.")
    await asyncio.sleep(1)