import discord
from discord.ext import commands
import asyncio
from main.config import BOT_PREFIX, BOT_TOKEN
import threading
from flask import Flask

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)
app = Flask("junba")

@app.route("/")
def home():
    return "Junba vivor, veior!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

# Roda o servidor Flask em paralelo
threading.Thread(target=run_web).start()


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("main.cogs.day_counter")
        await bot.load_extension("main.cogs.gpt_chat")
        await bot.start(BOT_TOKEN)

asyncio.run(main())
