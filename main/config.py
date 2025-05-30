from datetime import datetime
import os
if os.getenv("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
START_DATE = datetime(2025, 4, 4)
CANAL_ID_PICANHA = 1357801507302408314
CANAL_ID_CHAT = 1378046129341468715
BOT_PREFIX = "!"
RIOT_API= os.environ["RIOT_API"]
