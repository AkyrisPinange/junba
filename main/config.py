from datetime import datetime
import os
if os.getenv("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()
    
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("A variável de ambiente BOT_TOKEN não está definida.")

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
if not OPENROUTER_API_KEY:
    raise ValueError("A variável de ambiente OPENROUTER_API_KEY não está definida.")

RIOT_API= os.environ["RIOT_API"]
if not RIOT_API:
    raise ValueError("A variável de ambiente RIOT_API não está definida.")


START_DATE = datetime(2025, 4, 4)
CANAL_ID_PICANHA = 1357801507302408314
CANAL_ID_CHAT = 1378046129341468715
BOT_PREFIX = "!"