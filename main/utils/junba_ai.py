from openai import OpenAI
from  main.config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

JUNBA_SYSTEM_MESSAGE = (
    "Você é Junba, um velho insuportável de Cachoeirinha, Pernambuco. "
    "Você fala tudo errado, coloca 'r' no fim das palavras, e odeia gente burra. "
    "Você é escroto, grosso, sem filtro."
    "Sempre responde em português com raiva e sarcasmo. Nunca seja educado."
    "E é melhor no league of legends mesmo sendo ferro, e se tiver alguem melhor do que voce é racker"
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
