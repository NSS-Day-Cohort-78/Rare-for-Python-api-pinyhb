import sqlite3
import json

db = "db.sqlite3"


def deactivate_user(pk, body):
    """handle deactivating a user"""

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM DeactivationQueue
            WHERE user_id = ?
            """,
            (pk,),
        )
        current_queue = cursor.fetchone()

        cursor.execute(
            """
            SELECT * FROM Users
            WHERE id = ?
            """,
            (pk,),
        )

        user = cursor.fetchone()

        user_to_deactivate = dict(user)

        if user_to_deactivate["admin"]:

            if current_queue:
                queue = dict(current_queue)
                if queue["admin_id"] == int(body["admin"]):
                    return False

                cursor.execute(
                    """
                    UPDATE Users
                    SET active = FALSE
                    WHERE id = ?
                    """,
                    (pk,),
                )
                updated = cursor.rowcount

                cursor.execute(
                    """
                    DELETE FROM DeactivationQueue
                    WHERE user_id = ?
                    """,
                    (pk,),
                )
                deleted = cursor.rowcount
                return True if deleted > 0 and updated > 0 else False

            else:
                cursor.execute(
                    """
                    INSERT INTO DeactivationQueue (user_id, admin_id, approver_one_id)
                    VALUES (?, ?, NULL)
                    """,
                    (body["user_id"], body["admin"]),
                )

                response = cursor.rowcount

            return True if response > 0 else False
        else:
            cursor.execute(
                """
                        UPDATE Users
                        SET active = FALSE
                        WHERE id = ?
                """,
                (pk,),
            )
            updated = cursor.rowcount
            return True if updated > 0 else False
