import os, json
from discord.ext import commands
from main.utils.riot_api import get_account, get_summoner_id, get_ranked_data
from main.utils.riot_utils import translate_tier  # se quiser traduzir o tier

class LoLSave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="salvarrank")
    async def salvar_rank(self, ctx, *, riot_id: str):
        """Salva os dados de rank (Solo/Duo e Flex) de um jogador"""
        await ctx.send("Perae veior... vamo salvá essa vergonha no file.")

        try:
            if "#" not in riot_id:
                await ctx.send("Manda o nome certor, tipo Zezin#BR1, jumentor.")
                return

            game_name, tag = riot_id.split("#")
            puuid = get_account(game_name, tag)

            if not puuid:
                await ctx.send("Num achei esse veior não. Vê se digitou certo.")
                return

            summoner_id = get_summoner_id(puuid)
            if not summoner_id:
                await ctx.send("Esse aí num joga nem tutorial, veior.")
                return

            ranked_data = get_ranked_data(summoner_id)
            if not ranked_data:
                await ctx.send(f"O `{riot_id}` nem joga ranqueada, veior. Vai plantar batata.")
                return

            # Indexar por tipo de fila
            ranked = {entry["queueType"]: entry for entry in ranked_data}

            solo = ranked.get("RANKED_SOLO_5x5")
            flex = ranked.get("RANKED_FLEX_SR")

            def parse_data(entry):
                return {
                    "tier": translate_tier(entry["tier"]),
                    "rank": entry["rank"],
                    "lp": entry["leaguePoints"],
                    "wins": entry["wins"],
                    "losses": entry["losses"],
                    "winrate": round((entry["wins"] / (entry["wins"] + entry["losses"])) * 100)
                }

            data = {
                "nome": riot_id,
                "solo": parse_data(solo) if solo else None,
                "flex": parse_data(flex) if flex else None
            }

            os.makedirs("data/players/tier", exist_ok=True)
            file_path = f"data/players/tier/{riot_id.replace('#', '_')}.json"
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

            elo_chart_cog = self.bot.get_cog("EloChart")
            if elo_chart_cog:
                await elo_chart_cog.process_elo_ranking()

            await ctx.send(f"Ranks de `{riot_id}` salvos com sucesso, veiorr.")



        except Exception as e:
            print(f"Erro ao salvar rank: {e}")
            await ctx.send("Deu ruim, veior... tenta mais tarde.")


async def setup(bot):
    await bot.add_cog(LoLSave(bot))
