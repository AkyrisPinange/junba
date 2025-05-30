import discord
from discord.ext import commands
import asyncio
from main.config import BOT_PREFIX, BOT_TOKEN


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("main.cogs.day_counter")
        await bot.load_extension("main.cogs.gpt_chat")
        await bot.load_extension("main.cogs.ranklol")
        await bot.start(BOT_TOKEN)

asyncio.run(main())
