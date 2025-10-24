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


def get_category_by_id(pk):
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                *
            FROM Categories c
            WHERE c.id = ?
            """,
            (pk,),
        )
        query_results = cursor.fetchone()

        serialized_category = json.dumps(dict(query_results))

    return serialized_category


def create_category(body):
    """create a new category"""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Categories (label) VALUES (?)
            """,
            (body["label"],),
        )

        row_added = cursor.rowcount

    return True if row_added > 0 else False


def delete_category(pk):

    with sqlite3.connect(db) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM Categories
            WHERE id = ?
            """,
            (pk,),
        )

        row_affected = cursor.rowcount

    return True if row_affected > 0 else False


def update_category(pk, category_data):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Categories
                SET
                    label = ?
            WHERE id = ?
            """,
            (category_data["label"], pk),
        )

        rows_affected = cursor.rowcount

    return True if rows_affected > 0 else False
