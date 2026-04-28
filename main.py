import discord
import asyncio
import os
import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("TOKEN")
CANAL_DESTINO_ID = int(os.getenv("CANAL_DESTINO_ID"))
CANAL_GERAL_ID = int(os.getenv("CANAL_GENERAL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
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

            try:
                await message.delete()
            except Exception as e:
                print(f"Erro ao deletar: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)

@bot.command()
async def scan(ctx):
    await ctx.send("🔍 Iniciando varredura (últimos 7 dias)...")

    canal_destino = bot.get_channel(CANAL_DESTINO_ID)

    if not canal_destino:
        await ctx.send("❌ Canal de destino não encontrado.")
        return

    count = 0

    # pega data de 7 dias atrás
    after_date = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    async for message in ctx.channel.history(limit=None, after=after_date):
        if message.author.bot:
            continue

        if "https://gamersclub.com.br" in message.content:
            await canal_destino.send(
                f"📥 (Histórico)\n"
                f"📍 {message.channel.mention}\n"
                f"👤 {message.author.mention}\n"
                f"💬 {message.content}"
            )
            count += 1
            await asyncio.sleep(1)

    await ctx.send(f"✅ Finalizado! {count} mensagens encontradas.")
