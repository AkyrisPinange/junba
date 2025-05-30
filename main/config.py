from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
START_DATE = datetime(2025, 4, 4)
CANAL_ID_PICANHA = 1357801507302408314
CANAL_ID_CHAT = 1378046129341468715
BOT_PREFIX = "!"
