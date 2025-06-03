import os
import json
import datetime
from discord.ext import commands, tasks
import discord
TIER_EMOJIS = {
    "FERRO": "🪨", "BRONZE": "🥉", "PRATA": "🥈", "OURO": "🥇",
    "PLATINA": "💎", "ESMERALDA": "🍀", "DIAMANTE": "🔷",
    "MESTRE": "🧠", "GRÃO-MESTRE": "🔥", "DESAFIANTE": "👑"
}
TIER_MAP = {
    "FERRO": 1, "BRONZE": 2, "PRATA": 3, "OURO": 4,
    "PLATINA": 5, "ESMERALDA": 6, "DIAMANTE": 7,
    "MESTRE": 8, "GRÃO-MESTRE": 9, "DESAFIANTE": 10
}
RANK_MAP = {"IV": 0, "III": 1, "II": 2, "I": 3}

RANK_CHANNEL_ID = 1379572040977088644

def calculate_elo_score(tier, rank, lp):
    return TIER_MAP.get(tier.upper(), 0) * 4 + RANK_MAP.get(rank.upper(), 0) + (lp / 100)

def format_elo(data):
    if data:
        tier = data["tier"].upper()
        icon = TIER_EMOJIS.get(tier, "")
        return f"{icon} {data['tier'].title()} {data['rank']} ({data['lp']} LP) - {data['winrate']}% WR"
    return "Não joga nem ARAM, veiorr."

class DummyCtx:
    def __init__(self, bot):
        self.bot = bot

    async def send(self, *args, **kwargs):
        pass  # Ignora respostas fora do canal fixo

class EloChart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_ranking.start()

    def cog_unload(self):
        self.daily_ranking.cancel()

    @commands.command(name="graficoelos")
    async def elo_chart(self, ctx):
        await self.process_elo_ranking()

    @tasks.loop(hours=24)
    async def daily_ranking(self):
        await self.process_elo_ranking()

    @daily_ranking.before_loop
    async def before_daily_ranking(self):
        await self.bot.wait_until_ready()

    async def process_elo_ranking(self):
        players = []
        today = datetime.date.today().strftime("%Y-%m-%d")
        path = "data/players/tier"
        if not os.path.exists(path):
            return

        for file in os.listdir(path):
            if file.endswith(".json"):
                with open(os.path.join(path, file)) as f:
                    data = json.load(f)
                    solo = data.get("solo")
                    flex = data.get("flex")
                    nome = data.get("nome")

                    elo_solo = calculate_elo_score(solo["tier"], solo["rank"], solo["lp"]) if solo else 0

                    # Salvar histórico
                    historico_path = f"data/players/historico/{file}"
                    os.makedirs("data/players/historico", exist_ok=True)

                    entry = {
                        "date": today,
                        "nome": nome,
                        "solo": solo,
                        "flex": flex
                    }

                    if os.path.exists(historico_path):
                        with open(historico_path) as hist_file:
                            hist_data = json.load(hist_file)
                    else:
                        hist_data = []

                    if not any(d["date"] == today for d in hist_data):
                        hist_data.append(entry)
                        with open(historico_path, "w") as hist_file:
                            json.dump(hist_data, hist_file, indent=2)

                    players.append({
                        "nome": nome,
                        "solo": solo,
                        "flex": flex,
                        "elo_solo": elo_solo
                    })

        if not players:
            return

        players.sort(key=lambda x: x["elo_solo"], reverse=True)


        embed = discord.Embed(
            title=f"📊 Ranking de Elo - {datetime.date.today().strftime('%d/%m/%Y')}",
            description="Digiter '!salvarrank name#tagline' ou '!graficoelos' para atualizar o graficor",
            color=discord.Color.blue()
        )

        for i, p in enumerate(players, start=1):
            solo = format_elo(p["solo"])
            flex = format_elo(p["flex"])
            embed.add_field(
                name=f"{i}. {p['nome']}",
                value=f"**Solo/Duo:** {solo}\n**Flex:** {flex}",
                inline=False
            )

        canal = self.bot.get_channel(RANK_CHANNEL_ID)
        if canal:
            await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EloChart(bot))
