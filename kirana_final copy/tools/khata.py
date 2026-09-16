from datetime import datetime
from database import get_db
from tools.inventory import paise_to_rupees, rupees_to_paise

DEPOSIT = "DEPOSIT"
PURCHASE = "PURCHASE"
REFUND = "REFUND"


def _get_customer(db, name):
    return db.execute("SELECT * FROM customers WHERE LOWER(name)=LOWER(?)", (name.strip(),)).fetchone()


def _get_or_create_customer(db, name):
    name = name.strip()
    if not name:
        raise ValueError("Customer name cannot be empty.")
    customer = _get_customer(db, name)
    if customer:
        return customer
    cur = db.execute(
        "INSERT INTO customers(name, created_at) VALUES (?, ?)",
        (name, datetime.now().isoformat(timespec="seconds")),
    )
    return db.execute("SELECT * FROM customers WHERE id=?", (cur.lastrowid,)).fetchone()


def _balance_paise(db, customer_id):
    row = db.execute(
        """
        SELECT COALESCE(SUM(CASE
            WHEN transaction_type IN ('DEPOSIT','REFUND') THEN amount
            WHEN transaction_type = 'PURCHASE' THEN -amount
            ELSE 0 END),0) AS balance
        FROM khata_transactions WHERE customer_id=?
        """,
        (customer_id,),
    ).fetchone()
    return int(row["balance"] or 0)


def get_customer_balance(name):
    with get_db() as db:
        customer = _get_customer(db, name)
        if not customer:
            return {"success": False, "error": f"No wallet exists for {name}."}
        balance = _balance_paise(db, customer["id"])
    return {"success": True, "customer": customer["name"], "balance": paise_to_rupees(balance)}


def add_credit(customer_name, amount_rupees, description="Wallet deposit"):
    """Backward-compatible name: records a prepaid-wallet deposit."""
    amount = rupees_to_paise(amount_rupees)
    if amount <= 0:
        return {"success": False, "error": "Deposit amount must be positive."}
    with get_db() as db:
        customer = _get_or_create_customer(db, customer_name)
        db.execute(
            """INSERT INTO khata_transactions(customer_id, transaction_type, amount, description, created_at)
               VALUES (?, 'DEPOSIT', ?, ?, ?)""",
            (customer["id"], amount, description, datetime.now().isoformat(timespec="seconds")),
        )
        balance = _balance_paise(db, customer["id"])
    return {"success": True, "customer": customer["name"], "deposited": paise_to_rupees(amount), "balance": paise_to_rupees(balance)}


def record_payment(customer_name, amount_rupees, description="Wallet deposit"):
    """Backward-compatible API: a customer payment adds money to the prepaid wallet."""
    return add_credit(customer_name, amount_rupees, description)


def consume_wallet(db, customer_name, amount_paise, bill_id=None, description="Purchase"):
    """Debit a customer's wallet inside an existing DB transaction."""
    customer = _get_customer(db, customer_name)
    if not customer:
        return {"success": False, "error": f"No wallet exists for {customer_name}."}
    balance = _balance_paise(db, customer["id"])
    if amount_paise > balance:
        return {
            "success": False,
            "error": f"Insufficient Khata balance. Available ₹{paise_to_rupees(balance):.2f}, required ₹{paise_to_rupees(amount_paise):.2f}.",
            "balance": paise_to_rupees(balance),
        }
    db.execute(
        """INSERT INTO khata_transactions(customer_id, transaction_type, amount, bill_id, description, created_at)
           VALUES (?, 'PURCHASE', ?, ?, ?, ?)""",
        (customer["id"], amount_paise, bill_id, description, datetime.now().isoformat(timespec="seconds")),
    )
    new_balance = balance - amount_paise
    return {"success": True, "customer": customer["name"], "debited": paise_to_rupees(amount_paise), "balance": paise_to_rupees(new_balance)}


def add_refund(customer_name, amount_rupees, bill_id=None, description="Refund"):
    amount = rupees_to_paise(amount_rupees)
    if amount <= 0:
        return {"success": False, "error": "Refund amount must be positive."}
    with get_db() as db:
        customer = _get_or_create_customer(db, customer_name)
        db.execute(
            """INSERT INTO khata_transactions(customer_id, transaction_type, amount, bill_id, description, created_at)
               VALUES (?, 'REFUND', ?, ?, ?, ?)""",
            (customer["id"], amount, bill_id, description, datetime.now().isoformat(timespec="seconds")),
        )
        balance = _balance_paise(db, customer["id"])
    return {"success": True, "customer": customer["name"], "refunded": paise_to_rupees(amount), "balance": paise_to_rupees(balance)}


def list_customers(limit=50):
    with get_db() as db:
        rows = db.execute("SELECT id,name,phone FROM customers ORDER BY name LIMIT ?", (int(limit),)).fetchall()
        result = []
        for row in rows:
            result.append({"id": row["id"], "name": row["name"], "phone": row["phone"], "balance": paise_to_rupees(_balance_paise(db, row["id"]))})
    return result
