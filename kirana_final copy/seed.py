from datetime import datetime

from database import init_db, get_db


PRODUCTS = [
    {
        "name": "Aashirvaad Atta 5kg",
        "brand": "Aashirvaad",
        "sku": "ATT-AASH-5KG",
        "unit": "kg",
        "pack_size": "5kg",
        "loose": 0,
        "cost_price": 22000,
        "sell_price": 25000,
        "mrp": 25000,
        "quantity": 20,
        "reorder_level": 5,
        "hsn_code": "1101",
        "gst_rate": 5,
    },

    {
        "name": "Tata Salt 1kg",
        "brand": "Tata",
        "sku": "SALT-TATA-1KG",
        "unit": "kg",
        "pack_size": "1kg",
        "loose": 0,
        "cost_price": 2500,
        "sell_price": 2800,
        "mrp": 2800,
        "quantity": 30,
        "reorder_level": 8,
        "hsn_code": "2501",
        "gst_rate": 5,
    },

    {
        "name": "Amul Butter 100g",
        "brand": "Amul",
        "sku": "BUT-AMUL-100G",
        "unit": "packet",
        "pack_size": "100g",
        "loose": 0,
        "cost_price": 5200,
        "sell_price": 6200,
        "mrp": 6200,
        "quantity": 15,
        "reorder_level": 5,
        "hsn_code": "0405",
        "gst_rate": 12,
    },

    {
        "name": "Fortune Sunflower Oil 1L",
        "brand": "Fortune",
        "sku": "OIL-FORT-1L",
        "unit": "litre",
        "pack_size": "1L",
        "loose": 0,
        "cost_price": 12000,
        "sell_price": 13500,
        "mrp": 14500,
        "quantity": 20,
        "reorder_level": 5,
        "hsn_code": "1512",
        "gst_rate": 5,
    },

    {
        "name": "Maggi 70g",
        "brand": "Nestle",
        "sku": "MAGGI-70G",
        "unit": "packet",
        "pack_size": "70g",
        "loose": 0,
        "cost_price": 1200,
        "sell_price": 1400,
        "mrp": 1400,
        "quantity": 50,
        "reorder_level": 10,
        "hsn_code": "1902",
        "gst_rate": 12,
    },

    {
        "name": "Parle-G",
        "brand": "Parle",
        "sku": "PARLE-G",
        "unit": "packet",
        "pack_size": "standard",
        "loose": 0,
        "cost_price": 500,
        "sell_price": 600,
        "mrp": 600,
        "quantity": 40,
        "reorder_level": 10,
        "hsn_code": "1905",
        "gst_rate": 5,
    },

    {
        "name": "Surf Excel",
        "brand": "Surf Excel",
        "sku": "SURF-EXCEL",
        "unit": "packet",
        "pack_size": "standard",
        "loose": 0,
        "cost_price": 6500,
        "sell_price": 7500,
        "mrp": 8000,
        "quantity": 15,
        "reorder_level": 5,
        "hsn_code": "3402",
        "gst_rate": 18,
    },

    {
        "name": "Loose Sugar",
        "brand": "Local",
        "sku": "SUGAR-LOOSE",
        "unit": "kg",
        "pack_size": "loose",
        "loose": 1,
        "cost_price": 4000,
        "sell_price": 4500,
        "mrp": 4500,
        "quantity": 50,
        "reorder_level": 10,
        "hsn_code": "1701",
        "gst_rate": 0,
    },

    {
        "name": "Loose Rice",
        "brand": "Local",
        "sku": "RICE-LOOSE",
        "unit": "kg",
        "pack_size": "loose",
        "loose": 1,
        "cost_price": 4500,
        "sell_price": 5200,
        "mrp": 5200,
        "quantity": 60,
        "reorder_level": 15,
        "hsn_code": "1006",
        "gst_rate": 0,
    },

    {
        "name": "Toor Dal",
        "brand": "Local",
        "sku": "DAL-TOOR",
        "unit": "kg",
        "pack_size": "loose",
        "loose": 1,
        "cost_price": 10000,
        "sell_price": 11500,
        "mrp": 11500,
        "quantity": 30,
        "reorder_level": 8,
        "hsn_code": "0713",
        "gst_rate": 0,
    },
]


def seed_products():

    init_db()

    with get_db() as db:

        for product in PRODUCTS:

            db.execute(
                """
                INSERT OR IGNORE INTO products
                (
                    name,
                    brand,
                    sku,
                    unit,
                    pack_size,
                    loose,
                    cost_price,
                    sell_price,
                    mrp,
                    quantity,
                    reorder_level,
                    hsn_code,
                    gst_rate,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    product["name"],
                    product["brand"],
                    product["sku"],
                    product["unit"],
                    product["pack_size"],
                    product["loose"],
                    product["cost_price"],
                    product["sell_price"],
                    product["mrp"],
                    product["quantity"],
                    product["reorder_level"],
                    product["hsn_code"],
                    product["gst_rate"],
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

    print("Products seeded successfully.")


if __name__ == "__main__":
    seed_products()
