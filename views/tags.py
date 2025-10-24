import sqlite3
import json

db = "db.sqlite3"


def get_all_tags():
    """get all tags"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM Tags
            ORDER BY label
            """
        )

        response = cursor.fetchall()

        tags = []
        for row in response:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)
    return serialized_tags
