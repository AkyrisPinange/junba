from discord.ext import commands
import random

class LoLTeam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="times")
    async def sortear_times(self, ctx, *, jogadores: str):
        """Divide jogadores em dois times aleatórios e esculacha quem ficar de fora."""
        nomes = [nome.strip() for nome in jogadores.split(",") if nome.strip()]

        if len(nomes) < 2:
            await ctx.send("Bota pelo menos dois, jumentor.")
            return

        random.shuffle(nomes)
        excluido = None

        if len(nomes) % 2 != 0:
            excluido = nomes.pop()

        meio = len(nomes) // 2
        time1 = nomes[:meio]
        time2 = nomes[meio:]

        resposta = "🛠️ Sorteio feito, veiorr... olha essa pelada:\n\n"

        resposta += "🔵 Time 1:\n"
        resposta += "\n".join(f"- {jogador}" for jogador in time1) + "\n\n"

        resposta += "🔴 Time 2:\n"
        resposta += "\n".join(f"- {jogador}" for jogador in time2) + "\n"

        if excluido:
            resposta += f"\n❌ Ficou de fora: {excluido}\n"
            resposta += f"{excluido}, vai assistirr e parar de feedarr."

        await ctx.send(resposta)

async def setup(bot):
    await bot.add_cog(LoLTeam(bot))
