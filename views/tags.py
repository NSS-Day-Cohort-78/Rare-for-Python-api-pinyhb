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


def delete_tag(pk):
    """delete a tag"""
    with sqlite3.connect(db) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM Tags
            WHERE id = ?
            """,
            (pk,),
        )
        row_affected = cursor.rowcount

    return True if row_affected > 0 else False


def create_tag(body):
    """create a tag"""
    with sqlite3.connect(db) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Tags (label) Values (?)
            """,
            (body["label"],),
        )
        row_affected = cursor.rowcount

    return True if row_affected > 0 else False


def get_post_tags(pk):
    """get tags for a post"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM PostTags
            WHERE post_id =?
            """,
            (pk,),
        )

        response = cursor.fetchall()

        tags = []
        for row in response:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)
    return serialized_tags


def add_post_tag(body):
    """add a tag to a post"""
    with sqlite3.connect(db) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO PostTags (post_id, tag_id)
            VALUES (?, ?)
            """,
            (body["post_id"], body["tag_id"]),
        )
        row_affected = cursor.rowcount

    return True if row_affected > 0 else False

def delete_post_tag(pk):
    """delete a tag from a post"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM PostTags
            WHERE id = ?
            """,
            (pk,),
        )
        row_affected = cursor.rowcount

    return True if row_affected > 0 else False
