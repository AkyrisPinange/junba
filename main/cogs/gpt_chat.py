from discord.ext import commands
from main.utils.junba_ai import ask_junba

# Memória por canal
conversations = {}

class GPTChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="junba")
    async def chat_with_junba(self, ctx, *, message: str):
        """Talk to Junba, the angry old man."""
        await ctx.send("Calarr a bocarr, tô pensandor...")

        channel_id = str(ctx.channel.id)

        # Inicia histórico se não existir
        if channel_id not in conversations:
            conversations[channel_id] = []

        # Adiciona mensagem do usuário
        conversations[channel_id].append({"role": "user", "content": message})

        # Limita tamanho do histórico
        if len(conversations[channel_id]) > 10:
            conversations[channel_id] = conversations[channel_id][-10:]

        # Chama Junba com histórico
        reply = await ask_junba(message, history=conversations[channel_id])

        # Salva resposta no histórico
        conversations[channel_id].append({"role": "assistant", "content": reply})

        await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(GPTChat(bot))
