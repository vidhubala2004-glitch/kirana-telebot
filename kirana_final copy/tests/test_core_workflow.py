from database import init_db, get_db
from seed import seed_products
from tools import inventory, billing, khata


def reset_database():
    with get_db() as db:
        db.execute("DELETE FROM khata_transactions")
        db.execute("DELETE FROM bill_items")
        db.execute("DELETE FROM bills")
        db.execute("DELETE FROM customers")
        db.execute("DELETE FROM products")
    seed_products()


def test_complete_khata_sale_flow():
    init_db(); reset_database()
    maggi = inventory.search_products("Maggi")[0]
    assert khata.add_credit("Rahul", 1000)["balance"] == 1000.0
    draft = billing.create_bill_draft("test-chat", "Rahul")
    assert draft["success"]
    assert billing.add_bill_item("test-chat", maggi["id"], 3)["success"]
    assert inventory.get_stock(maggi["id"])["quantity"] == 50.0
    result = billing.finalize_bill("test-chat", "KHATA", idempotency_key="test-sale-1")
    assert result["success"]
    assert inventory.get_stock(maggi["id"])["quantity"] == 47.0
    assert khata.get_customer_balance("Rahul")["balance"] == 952.96


def test_oversell_does_not_change_stock():
    init_db(); reset_database()
    maggi = inventory.search_products("Maggi")[0]
    billing.create_bill_draft("oversell", "Test")
    result = billing.add_bill_item("oversell", maggi["id"], 999)
    assert not result["success"]
    assert inventory.get_stock(maggi["id"])["quantity"] == 50.0
