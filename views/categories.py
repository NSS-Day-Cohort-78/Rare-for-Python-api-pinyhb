"""Category Views"""

import sqlite3
import json

db = "db.sqlite3"


def get_categories():
    """get requests"""

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT c.id, c.label
            FROM Categories c
            """
        )

        response = cursor.fetchall()

        categories = []
        for row in response:
            categories.append(dict(row))

        serialized = json.dumps(categories)
    return serialized
