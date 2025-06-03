import requests
from main.config import RIOT_API

REGIAO = "br1"
ROUTE_REGION = "americas"

HEADERS = {"X-Riot-Token": RIOT_API}

def get_account(game_name, tag):
    url = f"https://{ROUTE_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag}"
    res = requests.get(url, headers=HEADERS).json()
    return res.get("puuid")

def get_summoner_id(puuid):
    url = f"https://{REGIAO}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    res = requests.get(url, headers=HEADERS).json()
    return res.get("id")

def get_ranked_data(summoner_id):
    url = f"https://{REGIAO}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    res = requests.get(url, headers=HEADERS).json()
    return res