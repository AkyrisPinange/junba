import os
import json
from main.utils.riot_api import get_account, get_summoner_id, get_ranked_data
from main.utils.riot_utils import translate_tier

def fetch_and_save_player_data(riot_id: str) -> dict | None:
    """Busca dados atualizados do jogador e salva no arquivo de tier."""
    if "#" not in riot_id:
        return None

    game_name, tag = riot_id.split("#")
    puuid = get_account(game_name, tag)
    if not puuid:
        return None

    summoner_id = get_summoner_id(puuid)
    if not summoner_id:
        return None

    ranked_data = get_ranked_data(summoner_id)
    if not ranked_data:
        return None

    # Separar solo e flex
    ranked = {entry["queueType"]: entry for entry in ranked_data}
    solo = ranked.get("RANKED_SOLO_5x5")
    flex = ranked.get("RANKED_FLEX_SR")

    def parse(entry):
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
        "solo": parse(solo) if solo else None,
        "flex": parse(flex) if flex else None
    }

    os.makedirs("data/players/tier", exist_ok=True)
    file_path = f"data/players/tier/{riot_id.replace('#', '_')}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return data


def update_all_players():
    """Atualiza os dados de todos os jogadores salvos em data/players/tier/"""
    path = "data/players/tier"
    if not os.path.exists(path):
        return

    for file in os.listdir(path):
        if file.endswith(".json"):
            riot_id = file.replace("_", "#").replace(".json", "")
            fetch_and_save_player_data(riot_id)
