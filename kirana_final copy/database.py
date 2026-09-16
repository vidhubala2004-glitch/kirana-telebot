import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

from config import DB_PATH


def _column_names(db, table):
    return {row[1] for row in db.execute(f"PRAGMA table_info({table})").fetchall()}


@contextmanager
def get_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        if conn.in_transaction:
            conn.commit()
    except Exception:
        if conn.in_transaction:
            conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            sku TEXT UNIQUE NOT NULL,
            unit TEXT NOT NULL,
            pack_size TEXT,
            loose INTEGER NOT NULL DEFAULT 0,
            cost_price INTEGER NOT NULL,
            sell_price INTEGER NOT NULL,
            mrp INTEGER NOT NULL,
            quantity REAL NOT NULL DEFAULT 0,
            reorder_level REAL NOT NULL DEFAULT 0,
            hsn_code TEXT,
            gst_rate REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_number TEXT UNIQUE NOT NULL,
            draft_key TEXT UNIQUE,
            customer_name TEXT,
            subtotal INTEGER NOT NULL DEFAULT 0,
            discount INTEGER NOT NULL DEFAULT 0,
            cgst INTEGER NOT NULL DEFAULT 0,
            sgst INTEGER NOT NULL DEFAULT 0,
            total_tax INTEGER NOT NULL DEFAULT 0,
            grand_total INTEGER NOT NULL DEFAULT 0,
            payment_mode TEXT,
            payment_reference TEXT,
            status TEXT NOT NULL DEFAULT 'DRAFT',
            idempotency_key TEXT UNIQUE,
            created_at TEXT NOT NULL,
            finalized_at TEXT
        );

        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            unit_price INTEGER NOT NULL,
            gst_rate REAL NOT NULL,
            taxable_amount INTEGER NOT NULL,
            cgst INTEGER NOT NULL,
            sgst INTEGER NOT NULL,
            total INTEGER NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            phone TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS khata_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            bill_id INTEGER,
            description TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (bill_id) REFERENCES bills(id)
        );

        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS processed_updates (
            update_id INTEGER PRIMARY KEY,
            processed_at TEXT NOT NULL
        );
        """)

        # Lightweight migrations for databases created by the earlier version.
        bills_cols = _column_names(db, "bills")
        if "discount" not in bills_cols:
            db.execute("ALTER TABLE bills ADD COLUMN discount INTEGER NOT NULL DEFAULT 0")
        if "finalized_at" not in bills_cols:
            db.execute("ALTER TABLE bills ADD COLUMN finalized_at TEXT")

    print("Database initialized successfully.")


def mark_update_processed(update_id):
    with get_db() as db:
        row = db.execute(
            "INSERT OR IGNORE INTO processed_updates(update_id, processed_at) VALUES (?, ?)",
            (int(update_id), datetime.now().isoformat(timespec="seconds")),
        )
        return row.rowcount == 1


if __name__ == "__main__":
    init_db()
