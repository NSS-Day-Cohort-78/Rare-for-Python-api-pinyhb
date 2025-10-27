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


def get_tag_by_id(pk):
    """get a tag"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM Tags
            WHERE id = ?
            """,
            (pk,),
        )

        response = cursor.fetchone()

        serialized_tag = json.dumps(dict(response))

    return serialized_tag


def update_tag(pk, body):
    """update a tag"""
    with sqlite3.connect(db) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Tags
                SET 
                id = ?,
                label = ?
                
            WHERE id = ?
            """,
            (
                body["id"],
                body["label"],
                pk,
            ),
        )

        row_affected = cursor.rowcount

    return True if row_affected > 0 else False
