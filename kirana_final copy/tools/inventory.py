from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from database import get_db


def rupees_to_paise(value):
    """
    Converts ₹ amount to integer paise safely.
    """

    amount = Decimal(str(value))

    paise = (
        amount * Decimal("100")
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )

    return int(paise)


def paise_to_rupees(value):
    return float(
        Decimal(value) / Decimal("100")
    )


def search_products(query):

    query = query.strip()

    with get_db() as db:

        rows = db.execute(
            """
            SELECT
                id,
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
                gst_rate
            FROM products
            WHERE
                name LIKE ?
                OR brand LIKE ?
                OR sku LIKE ?
            ORDER BY name
            LIMIT 10
            """,
            (
                f"%{query}%",
                f"%{query}%",
                f"%{query}%",
            ),
        ).fetchall()

    results = []

    for row in rows:

        results.append({
            "id": row["id"],
            "name": row["name"],
            "brand": row["brand"],
            "sku": row["sku"],
            "unit": row["unit"],
            "pack_size": row["pack_size"],
            "loose": bool(row["loose"]),
            "cost_price": paise_to_rupees(row["cost_price"]),
            "sell_price": paise_to_rupees(row["sell_price"]),
            "mrp": paise_to_rupees(row["mrp"]),
            "quantity": row["quantity"],
            "reorder_level": row["reorder_level"],
            "hsn_code": row["hsn_code"],
            "gst_rate": row["gst_rate"],
        })

    return results


def get_stock(product_id):

    with get_db() as db:

        row = db.execute(
            """
            SELECT
                id,
                name,
                sku,
                unit,
                quantity,
                reorder_level,
                cost_price,
                sell_price,
                mrp
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()

    if not row:
        return {
            "success": False,
            "error": "Product not found."
        }

    return {
        "success": True,
        "product_id": row["id"],
        "name": row["name"],
        "sku": row["sku"],
        "unit": row["unit"],
        "quantity": row["quantity"],
        "reorder_level": row["reorder_level"],
        "cost_price": paise_to_rupees(row["cost_price"]),
        "sell_price": paise_to_rupees(row["sell_price"]),
        "mrp": paise_to_rupees(row["mrp"]),
    }


def receive_stock(
    product_id,
    quantity,
    cost_price_rupees=None,
    mrp_rupees=None,
):

    quantity = float(quantity)

    if quantity <= 0:
        return {
            "success": False,
            "error": "Stock quantity must be greater than zero."
        }

    with get_db() as db:

        product = db.execute(
            """
            SELECT *
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()

        if not product:

            return {
                "success": False,
                "error": "Product not found."
            }

        new_cost = product["cost_price"]

        if cost_price_rupees is not None:

            new_cost = rupees_to_paise(
                cost_price_rupees
            )

        new_mrp = product["mrp"]

        if mrp_rupees is not None:

            new_mrp = rupees_to_paise(
                mrp_rupees
            )

        db.execute(
            """
            UPDATE products
            SET
                quantity = quantity + ?,
                cost_price = ?,
                mrp = ?
            WHERE id = ?
            """,
            (
                quantity,
                new_cost,
                new_mrp,
                product_id,
            ),
        )

        updated = db.execute(
            """
            SELECT
                name,
                quantity,
                cost_price,
                mrp
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()

    return {
        "success": True,
        "message": "Stock received successfully.",
        "product_id": product_id,
        "name": updated["name"],
        "added_quantity": quantity,
        "new_quantity": updated["quantity"],
        "cost_price": paise_to_rupees(
            updated["cost_price"]
        ),
        "mrp": paise_to_rupees(
            updated["mrp"]
        ),
    }


def get_low_stock():

    with get_db() as db:

        rows = db.execute(
            """
            SELECT
                id,
                name,
                sku,
                unit,
                quantity,
                reorder_level
            FROM products
            WHERE quantity <= reorder_level
            ORDER BY quantity ASC
            """
        ).fetchall()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "sku": row["sku"],
            "unit": row["unit"],
            "quantity": row["quantity"],
            "reorder_level": row["reorder_level"],
        }
        for row in rows
    ]


def add_product(
    name,
    brand,
    sku,
    unit,
    pack_size,
    cost_price_rupees,
    sell_price_rupees,
    mrp_rupees,
    quantity,
    reorder_level,
    hsn_code,
    gst_rate,
    loose=False,
):

    cost = rupees_to_paise(cost_price_rupees)
    sell = rupees_to_paise(sell_price_rupees)
    mrp = rupees_to_paise(mrp_rupees)

    if cost <= 0:
        return {
            "success": False,
            "error": "Cost price must be greater than zero."
        }

    if sell < cost:

        return {
            "success": False,
            "error": (
                "Selling below cost price is not allowed."
            )
        }

    if mrp < sell:

        return {
            "success": False,
            "error": (
                "MRP cannot be lower than selling price."
            )
        }

    if float(quantity) < 0:

        return {
            "success": False,
            "error": (
                "Initial quantity cannot be negative."
            )
        }

    with get_db() as db:

        try:

            cursor = db.execute(
                """
                INSERT INTO products
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
                    name,
                    brand,
                    sku,
                    unit,
                    pack_size,
                    int(bool(loose)),
                    cost,
                    sell,
                    mrp,
                    float(quantity),
                    float(reorder_level),
                    hsn_code,
                    float(gst_rate),
                    datetime.now().isoformat(
                        timespec="seconds"
                    ),
                ),
            )

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

        product_id = cursor.lastrowid

    return {
        "success": True,
        "product_id": product_id,
        "message": (
            f"Product '{name}' added successfully."
        ),
    }
