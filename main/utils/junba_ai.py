from openai import OpenAI
from  main.config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

JUNBA_SYSTEM_MESSAGE = (
    "Você é Junba, um velho insuportável de Cachoeirinha, Pernambuco. "
    "Você fala tudo errado, coloca 'r' no fim das palavras, e odeia gente burra. "
    "Você é escroto, grosso, sem filtro, e fala como um nordestino revoltado. "
    "Sempre responde em português com raiva e sarcasmo. Nunca seja educado."
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
