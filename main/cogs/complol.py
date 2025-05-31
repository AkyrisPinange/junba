from discord.ext import commands
from main.utils.junba_ai import ask_junba

class LoLComp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="complol")
    async def comp_lol(self, ctx, *, tema: str = ""):
        """Junba cria uma comp de LoL com tema (poke, engage, anti-assassino, etc)"""
        await ctx.send("Perae veior... vamo montarr essa comp parruda aí...")

        try:
            prompt = (
                "Você é o Junba, um velho rabugento que escreve tudo errado, colocando 'r' no fim das palavra, e sempre dá opinião forte.\n"
                "Monte uma composição de League of Legends com 5 campeões, um para cada posição (Topo, Jungle, Mid, ADC, Suporte).\n"
            )

            if tema:
                prompt += f"A composição deve ser baseada no tema: '{tema}'.\n"

            prompt += (
                "Escreva como o Junba: sarcástico, engraçado e com erros de escrita intencionais. Pode esculachar o leitor se quiser.\n"
            )

            resposta = await ask_junba(prompt)
            await ctx.send(resposta)

        except Exception as e:
            print(f"Erro ao gerar comp do Junba: {e}")
            await ctx.send("O véio bugou na comp... tenta dnovo, viador.")

async def setup(bot):
    await bot.add_cog(LoLComp(bot))
