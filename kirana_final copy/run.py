import sys
import os
import asyncio
import logging
import uvicorn
from multiprocessing import Process

from config import OPENAI_API_KEY, TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("kirana-runner")


def run_web_server():
    print("==================================================")
    print("🚀 STARTING KIRANA AI WEB UI SERVER (http://localhost:8000)")
    print("==================================================")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)


def run_telegram_bot():
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("YOUR_"):
        print("⚠️ TELEGRAM_BOT_TOKEN is placeholder or not configured in .env.")
        print("Skipping Telegram Bot polling loop. Web UI is fully operational!")
        return

    print("==================================================")
    print("🤖 STARTING KIRANA AI TELEGRAM BOT POLLING LOOP")
    print("==================================================")
    try:
        from app import main as telegram_main
        telegram_main()
    except Exception as e:
        logger.error(f"Telegram Bot launch error: {e}")


def main():
    print("==================================================")
    print("🛒 KIRANA AI STORE ASSISTANT UNIFIED SYSTEM")
    print("==================================================")

    web_process = Process(target=run_web_server)
    web_process.start()

    telegram_process = Process(target=run_telegram_bot)
    telegram_process.start()

    try:
        web_process.join()
        telegram_process.join()
    except KeyboardInterrupt:
        print("\nStopping Kirana AI services...")
        web_process.terminate()
        telegram_process.terminate()
        sys.exit(0)


if __name__ == "__main__":
    main()
