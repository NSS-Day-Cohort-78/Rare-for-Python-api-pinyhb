"""Post Views"""

import sqlite3
import json

db = "db.sqlite3"


def get_posts():
    """Get Posts"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM Posts
            """
        )
        response = cursor.fetchall()
        posts = []

        for row in response:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)
    return serialized_posts
