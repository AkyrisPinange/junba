from discord.ext import commands

from main.services.riot_rank_service  import fetch_and_save_player_data

class LoLSave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="salvarrank")
    async def salvar_rank(self, ctx, *, riot_id: str):
        await ctx.send("Perae veior... vamo salvá essa vergonha no file.")
        data = fetch_and_save_player_data(riot_id)

        if not data:
            await ctx.send("Num achei o cidadão não ou deu erro na API, veior.")
            return

        elo_chart_cog = self.bot.get_cog("EloChart")
        if elo_chart_cog:
            await elo_chart_cog.process_elo_ranking()

        await ctx.send(f"Ranks de `{riot_id}` salvos com sucesso, veiorr.")



async def setup(bot):
    await bot.add_cog(LoLSave(bot))
