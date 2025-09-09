import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///./hisob.db")
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Tashkent")
    DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "uz")
    DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "UZS")

settings = Settings()
