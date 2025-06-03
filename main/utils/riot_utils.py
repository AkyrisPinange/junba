def translate_tier(tier: str) -> str:
    tier_map = {
        "IRON": "FERRO",
        "BRONZE": "BRONZE",
        "SILVER": "PRATA",
        "GOLD": "OURO",
        "PLATINUM": "PLATINA",
        "EMERALD": "ESMERALDA",
        "DIAMOND": "DIAMANTE",
        "MASTER": "MESTRE",
        "GRANDMASTER": "GRÃO-MESTRE",
        "CHALLENGER": "DESAFIANTE"
    }
    return tier_map.get(tier.upper(), tier)

