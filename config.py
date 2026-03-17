import os
from dotenv import load_dotenv

# путь к .env (чтобы 100% работало)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# токены
BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_ID = os.getenv("MANAGER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME")

# бизнес данные
COMPANY_NAME = os.getenv("COMPANY_NAME", "КИТАЙСКИЙ ПАРТНЕР")
CARGO_TIME = os.getenv("CARGO_TIME", "20 дней")
WHITE_TIME = os.getenv("WHITE_TIME", "40 дней")

# проверки (чтобы сразу ловить ошибки)
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

if not MANAGER_ID:
    raise ValueError("❌ MANAGER_ID не найден в .env")

# приводим к числу
MANAGER_ID = int(MANAGER_ID)