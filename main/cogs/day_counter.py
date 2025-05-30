import discord
from discord.ext import commands, tasks
from main.config import CANAL_ID_PICANHA
from main.utils.date_tools import days_from_begin

class DayCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.atualizar_menu.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.atualizar_menu.is_running():
            self.atualizar_menu.start()

    @tasks.loop(hours=24)
    async def atualizar_menu(self):
        canal = self.bot.get_channel(CANAL_ID_PICANHA)
        print(f"Canal obtido: {canal}")

        if canal is None:
            print("❌ Canal não encontrado.")
            return

        embed = discord.Embed(
            title="📅 Dias sem a Picanha Prometida 🥩 ",
            description=f"Estamos no **Dia {days_from_begin()}** desde a falsa promessa!",
            color=discord.Color.blue()
        )
        await canal.send(embed=embed)


    @commands.command()
    async def dia(self, ctx):
        """Mostra o dia atual da jornada"""
        await ctx.send(f"📅 Estamos no **Dia {days_from_begin()}**!")

async def setup(bot):
    await bot.add_cog(DayCounter(bot))
