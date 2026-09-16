import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
GENERATED_DIR = BASE_DIR / "generated"

INVOICE_DIR = GENERATED_DIR / "invoices"
REPORT_DIR = GENERATED_DIR / "reports"

DATA_DIR.mkdir(exist_ok=True)
GENERATED_DIR.mkdir(exist_ok=True)
INVOICE_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

DB_PATH = DATA_DIR / "kirana.db"

def validate_config():
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("YOUR_"):
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing or invalid in .env")
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("YOUR_"):
        print("Warning: OPENAI_API_KEY is missing or invalid; app will use local rule-based fallback responses.")
