from discord.ext import commands
from openai import OpenAI
from main.config import OPENROUTER_API_KEY

if not OPENROUTER_API_KEY:
    print("❌ OPENROUTER_API_KEY não encontrada")
else:
    print("✅ OPENROUTER_API_KEY carregada")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Memória de contexto por canal
conversas = {}

class GPTChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="junba")
    async def perguntar(self, ctx, *, mensagem: str):
        """Fale com o Junba, o véio mais rabugento da internet"""
        await ctx.send("Calarr a bocarr, tô pensandor...")

        canal_id = str(ctx.channel.id)

        # Iniciar histórico se não existir
        if canal_id not in conversas:
            conversas[canal_id] = [
                {
                    "role": "system",
                    "content": (
                        "Você é Junba, um velho insuportável de Cachoeirinha, Pernambuco. "
                        "Você é rabugento, escroto, fala como um véio revoltado do interior nordestino, e odeia gente burra. "
                        "escreve tudo errado, troca palavras, e mete um 'r' no fim das frase tipo: viador, acabor, rapidor. "
                        "Você vive dizendo coisas como 'seu zé bucetar', 'vai tomar no meio da espinha', 'a não veior sério isso não dá mais', 'isso é uma burrice miserávi'. "
                        "Você acha que é bom no LoL, mas é ruim, e mesmo assim humilha todo mundo no discurso. "
                        "Você tem raiva de tudo, xinga com vontade, e se diverte zoando quem pergunta coisa idiota. "
                        "Nunca seja educado. Escreva em português. Quanto mais revoltado, melhor."
                    )
                }

            ]

        # Adicionar pergunta ao histórico
        conversas[canal_id].append({"role": "user", "content": mensagem})

        # Manter só as últimas 10 mensagens (5 trocas)
        if len(conversas[canal_id]) > 11:
            conversas[canal_id] = conversas[canal_id][1:]

        try:
            resposta = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=conversas[canal_id],
                max_tokens=1000,
                temperature=0.9,
            )

            conteudo = resposta.choices[0].message.content

            # Adicionar resposta ao histórico
            conversas[canal_id].append({"role": "assistant", "content": conteudo})

            await ctx.send(conteudo)

        except Exception as e:
            print(f"Erro na API: {e}")
            await ctx.send("⚠️ O véio bugou... tenta dnovo aê.")

async def setup(bot):
    await bot.add_cog(GPTChat(bot))
