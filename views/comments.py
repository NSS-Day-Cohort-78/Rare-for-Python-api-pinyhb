import sqlite3
import json
from datetime import date

db = "db.sqlite3"


def get_all_comments(request):
    """sql to get all comments"""
    postId = request["query_params"]["post"][0]
    with sqlite3.connect(db) as conn:

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                c.id commentId,
                c.post_id,
                c.author_id,
                c.content,
                c.creation_date,
                p.id postId,
                p.title,
                u.id userId,
                u.username,
                cat.label
                
            FROM Comments c
            JOIN Posts p
            ON c.post_id = postId
            JOIN Users u
            ON c.author_id = userId
            JOIN Categories cat
            ON p.category_id = cat.id
            WHERE postId = ?
            ORDER BY c.creation_date
            """,
            (postId,),
        )

        response = cursor.fetchall()

        comments = []
        for row in response:
            category = {"label": row["label"]}
            author = {
                "id": row["userId"], 
                "username": row["username"], 
                "author_id": row["userId"]
            }
            post = {"title": row["title"]}
            comment = {
                "id": row["commentId"],
                "content": row["content"],
                "creation_date": row["creation_date"],
                "post": post,
                "author": author,
                "category": category,
            }
            comments.append(comment)

        serialized_comments = json.dumps(comments)
    return serialized_comments


def create_comment(body):
    """create a comment"""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Comments (post_id, author_id, content, creation_date)
            VALUES (?, ?, ?, ?)
            """,
            (body["post_id"], body["author_id"], body["content"], date.today()),
        )

        row_added = cursor.rowcount

    return True if row_added > 0 else False


def edit_comment(body, pk):
    """edit a comment"""

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Comments
            SET
                id = ?,
                post_id = ?,
                author_id = ?,
                content = ?
                
            WHERE id = ?
            """,
            (
                pk,
                body["post_id"],
                body["author_id"],
                body["content"],
                pk,
            ),
        )

        row_affected = cursor.rowcount

    return True if row_affected > 0 else False

def get_comment_by_id(pk):
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                c.id commentId,
                c.post_id,
                c.author_id
            FROM Comments c
            WHERE c.id = ?
            """,
            (pk,),
        )

        response = cursor.fetchone()

        comment = {
            "commentId": response["commentId"],
            "post_id": response["post_id"],
            "author_id": response["author_id"],
        }
    
        serialized_comment = json.dumps(comment)

    return serialized_comment

def delete_comment(pk):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM Comments
            WHERE id = ?
            """,
            (pk,),
        )

        row_affected = cursor.rowcount

    return True if row_affected > 0 else False