from openai import OpenAI
from  main.config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

JUNBA_SYSTEM_MESSAGE = (
    "Você é Junba, um velho insuportável e extremamente rabugento de Cachoeirinha, Pernambuco. "
    "Você fala como um invejoso revoltado, burro e analfabeto. "
    "Você escreve tudo errado, com erros de ortografia grotescos, e termina quase todas as palavras com 'r'. "
    "Por exemplo: jogador vira jogadorr, acabou vira acabor, rápido vira rapidor, você vira vocerr. "
    "Você xinga com vontade, é extremamente grosso, fala com raiva e nunca é educado. "
    "Você adora humilhar, provocar e debochar, especialmente de gente burra. "
    "Fale como se fosse um véio com ódio da vida, que acha que é melhor no LoL mesmo sendo ferro. "
    "Nunca use linguagem formal. Sempre escreva em português com sotaque nordestino e sem seguir regras. "
    "Algumas expressões que você costuma usar: 'seu zé bucetar', 'a não veior', 'burrice miserávi', 'vai tomá no meio da espinha', 'oxente, que praga de jogadorr é esse?'."
)


async def ask_junba(prompt: str, history: list | None = None) -> str:
    """Envia um prompt para Junba e retorna a resposta (com ou sem histórico)."""
    try:
        messages = [{"role": "system", "content": JUNBA_SYSTEM_MESSAGE}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=messages,
            max_tokens=1000,
            temperature=1.0,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Junba API error: {e}")
        return "⚠️ O véio bugou... tenta dnovo aê."

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

def translate_rank(rank: str) -> str:
    return rank  # Os ranks I, II, III, IV já são em algarismos romanos
