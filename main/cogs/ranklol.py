import requests
from discord.ext import commands
from main.config import RIOT_API
from main.utils.junba_ai import  ask_junba
from  main.utils.riot_utils import translate_tier

REGIAO = "br1"
ROUTE_REGION = "americas"  # usado para o endpoint de account-v1

class LoLRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ranklol")
    async def ranklol(self, ctx, *, riot_id: str):
        """Junba descobre o rank do cidadão no LoL com nome e tag"""
        await ctx.send("Perae, veior... vamo vê essa vergonha aí.")

        try:
            if "#" not in riot_id:
                await ctx.send("Manda o nome certor, tipo Zezin#BR1, jumentor.")
                return

            game_name, tag = riot_id.split("#")

            # 1. Buscar ID da conta
            account_url = f"https://{ROUTE_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag}"
            headers = {"X-Riot-Token": RIOT_API}
            account_res = requests.get(account_url, headers=headers).json()

            if "puuid" not in account_res:
                await ctx.send("Num achei esse veior não. Vê se digitou certo.")
                return

            puuid = account_res["puuid"]

            # 2. Buscar Summoner ID
            summoner_url = f"https://{REGIAO}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
            summoner_res = requests.get(summoner_url, headers=headers).json()

            if "id" not in summoner_res:
                await ctx.send("Esse aí num joga nem tutorial, veior.")
                return

            summoner_id = summoner_res["id"]

            # 3. Buscar dados de rank
            rank_url = f"https://{REGIAO}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
            rank_res = requests.get(rank_url, headers=headers).json()

            if not rank_res:
                await ctx.send(f"O `{riot_id}` nem joga ranqueada, veior. Vai plantar batata.")
                return

            solo = next((r for r in rank_res if r["queueType"] == "RANKED_SOLO_5x5"), None)
            if not solo:
                await ctx.send(f"O `{riot_id}` só joga URF e acha que é pro-player, viador.")
                return

            tier = solo["tier"]
            rank = translate_tier(solo["rank"])
            lp = solo["leaguePoints"]
            wins = solo["wins"]
            losses = solo["losses"]
            winrate = round((wins / (wins + losses)) * 100)

            prompt = (
                f"Analise esse jogador de LoL:\n"
                f"- Nome: {riot_id}\n"
                f"- Elo: {tier} {rank}\n"
                f"- PDL: {lp}\n"
                f"- Vitórias: {wins}\n"
                f"- Derrotas: {losses}\n"
                f"- Winrate: {winrate}%\n\n"
                "Fale como Junba. Seja grosso, revoltado, e escreva como um véio nordestino desbocado."
            )

            resposta = await ask_junba(prompt)

            await ctx.send(resposta)


        except Exception as e:
            print(f"Erro na API da Riot: {e}")
            await ctx.send("Erro na API da Riot, veior. Tenta mais tarder.")

async def setup(bot):
    await bot.add_cog(LoLRank(bot))
