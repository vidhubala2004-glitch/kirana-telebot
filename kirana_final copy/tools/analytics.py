from datetime import datetime, timedelta

from database import get_db
from tools.inventory import paise_to_rupees


def daily_sales(date_string=None):

    if date_string is None:

        date_string = datetime.now().strftime(
            "%Y-%m-%d"
        )

    with get_db() as db:

        summary = db.execute(
            """
            SELECT
                COUNT(*) AS bill_count,
                COALESCE(SUM(subtotal), 0)
                    AS subtotal,
                COALESCE(SUM(cgst), 0)
                    AS cgst,
                COALESCE(SUM(sgst), 0)
                    AS sgst,
                COALESCE(SUM(grand_total), 0)
                    AS total
            FROM bills
            WHERE status = 'FINALIZED'
            AND date(
                created_at,
                '+05:30'
            ) = ?
            """,
            (date_string,),
        ).fetchone()

        payment_rows = db.execute(
            """
            SELECT
                payment_mode,
                COUNT(*) AS count,
                COALESCE(
                    SUM(grand_total), 0
                ) AS amount
            FROM bills
            WHERE status = 'FINALIZED'
            AND date(
                created_at,
                '+05:30'
            ) = ?
            GROUP BY payment_mode
            """,
            (date_string,),
        ).fetchall()

        top_products = db.execute(
            """
            SELECT
                p.name,
                SUM(bi.quantity)
                    AS quantity,
                SUM(bi.total)
                    AS revenue
            FROM bill_items bi

            JOIN bills b
                ON b.id = bi.bill_id

            JOIN products p
                ON p.id = bi.product_id

            WHERE b.status = 'FINALIZED'

            AND date(
                b.created_at,
                '+05:30'
            ) = ?

            GROUP BY p.id

            ORDER BY revenue DESC

            LIMIT 10
            """,
            (date_string,),
        ).fetchall()

    return {
        "date": date_string,

        "bill_count": summary["bill_count"],

        "subtotal": paise_to_rupees(
            summary["subtotal"]
        ),

        "cgst": paise_to_rupees(
            summary["cgst"]
        ),

        "sgst": paise_to_rupees(
            summary["sgst"]
        ),

        "total": paise_to_rupees(
            summary["total"]
        ),

        "payments": [
            {
                "mode": row["payment_mode"],
                "count": row["count"],
                "amount": paise_to_rupees(
                    row["amount"]
                ),
            }
            for row in payment_rows
        ],

        "top_products": [
            {
                "name": row["name"],
                "quantity": row["quantity"],
                "revenue": paise_to_rupees(
                    row["revenue"]
                ),
            }
            for row in top_products
        ],
    }


def weekly_sales():

    today = datetime.now().date()

    start = today - timedelta(days=6)

    days = []

    current = start

    while current <= today:

        result = daily_sales(
            current.strftime("%Y-%m-%d")
        )

        days.append(result)

        current += timedelta(days=1)

    total_sales = sum(
        day["total"]
        for day in days
    )

    total_bills = sum(
        day["bill_count"]
        for day in days
    )

    return {
        "start_date": str(start),
        "end_date": str(today),
        "total_sales": total_sales,
        "total_bills": total_bills,
        "days": days,
    }
