from datetime import datetime

from database import get_db


def set_preference(
    key,
    value
):

    key = key.strip()
    value = str(value).strip()

    if not key:
        return {
            "success": False,
            "error": "Preference key cannot be empty."
        }

    with get_db() as db:

        db.execute(
            """
            INSERT INTO preferences
            (
                key,
                value,
                updated_at
            )
            VALUES (?, ?, ?)

            ON CONFLICT(key)
            DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (
                key,
                value,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

    return {
        "success": True,
        "key": key,
        "value": value,
    }


def get_preference(key):

    with get_db() as db:

        row = db.execute(
            """
            SELECT key, value
            FROM preferences
            WHERE key = ?
            """,
            (key,),
        ).fetchone()

    if not row:

        return {
            "success": False,
            "error": (
                f"No preference stored for '{key}'."
            )
        }

    return {
        "success": True,
        "key": row["key"],
        "value": row["value"],
    }


def list_preferences():

    with get_db() as db:

        rows = db.execute(
            """
            SELECT key, value
            FROM preferences
            ORDER BY key
            """
        ).fetchall()

    return [
        {
            "key": row["key"],
            "value": row["value"],
        }
        for row in rows
    ]
