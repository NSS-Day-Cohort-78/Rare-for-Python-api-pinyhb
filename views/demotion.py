import sqlite3
import json

db = "db.sqlite3"


def get_demotion_by_user(pk):
    """get a users demotion queue"""

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM DemotionQueue
            WHERE user_id = ?
            """,
            (pk,),
        )

        response = cursor.fetchone()

        serialized = json.dumps(dict(response))
    return serialized


def update_demotion(pk, body):

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        if "admin_id" in body:
            key = "admin_id"
            cursor.execute(
                """
            UPDATE DemotionQueue
            SET admin_id = ?
            WHERE user_id = ?
            """,
                (body[key], pk),
            )
        else:
            key = "approver_one_id"
            cursor.execute(
                """
            UPDATE DemotionQueue
            SET approver_one_id = ?
            WHERE user_id = ?
            """,
                (body[key], pk),
            )

        updated = cursor.rowcount
    return True if updated > 0 else False


def add_demotion(body):

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO DemotionQueue (user_id, admin_id, approver_one_id)
            VALUES (?, ?, ?)
            """,
            (body["user_id"], body["admin_id"], body["approver_one_id"]),
        )
        updated = cursor.rowcount
    return True if updated > 0 else False


def delete_demotion(pk):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM DemotionQueue
            WHERE id = ?
            """,
            (pk,),
        )
        updated = cursor.rowcount
    return True if updated > 0 else False
