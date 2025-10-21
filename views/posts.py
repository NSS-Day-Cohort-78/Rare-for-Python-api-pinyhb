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
            SELECT
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved,
                u.first_name,
                u.last_name,
                u.email,
                u.bio
            FROM Posts p
            JOIN Users u
            ON u.id = p.user_id
            """
        )
        response = cursor.fetchall()
        posts = []

        for row in response:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)
    return serialized_posts
