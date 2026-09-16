# Kirana AI Store Assistant

Telegram + OpenAI Agents SDK + SQLite + FastAPI.

## Core workflow

1. `/start` -> New Bill
2. Customer -> Product -> Quantity -> add another product
3. Choose Cash / UPI / Khata Wallet
4. Confirm sale
5. Stock is rechecked and deducted atomically
6. Bill/payment transaction is stored
7. PDF invoice is generated and sent

You can also just talk to the bot in plain language: receiving stock, adding
products, editing a bill mid-build, checking stock and low-stock, khata
deposits/balances, daily sales, invoices, and weekly analysis decks are all
handled by the AI agent using the store database.

Khata is a prepaid wallet:
- Deposit ₹1000 -> balance ₹1000
- Purchase ₹300 -> balance ₹700
- Purchase ₹500 -> balance ₹200

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate       # macOS/Linux
   .venv\Scripts\Activate.ps1      # Windows
   pip install -r requirements.txt
   ```

2. Create your own `.env` from the template and fill in your keys:

   ```bash
   cp .env.example .env
   ```

   Never commit your real `.env`.

## Run

Start the Telegram bot:

```bash
python app.py
```

Start the web UI and Telegram bot together:

```bash
python run.py
```

The web UI runs at http://localhost:8000.

Run only one Telegram polling process for the bot token. A second process
using the same token causes Telegram `409 Conflict`.

## Database

The SQLite database is created automatically in `data/kirana.db` and older
databases receive lightweight schema migrations for `discount` and
`finalized_at`.

## Tests

```bash
python -m pytest tests/test_core_workflow.py test_khata.py
```