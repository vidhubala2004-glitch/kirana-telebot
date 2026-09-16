from database import init_db, get_db
from tools.khata import add_credit, get_customer_balance


def test_prepaid_wallet():
    init_db()
    with get_db() as db:
        db.execute("DELETE FROM khata_transactions")
        db.execute("DELETE FROM customers")
    assert add_credit("Rahul", 1000)["balance"] == 1000.0
    assert add_credit("Rahul", 250)["balance"] == 1250.0
    assert get_customer_balance("Rahul")["balance"] == 1250.0
