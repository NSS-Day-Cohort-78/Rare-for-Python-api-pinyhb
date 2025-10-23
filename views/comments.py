import sqlite3
import json

db = "db.sqlite3"


def get_all_comments():
    """sql to get all comments"""
    with sqlite3.connect(db) as conn:

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content
            FROM Comments c
            """
        )

        response = cursor.fetchall()

        comments = []
        for row in response:
            comments.append(dict(row))

        serialized_comments = json.dumps(comments)
    return serialized_comments
