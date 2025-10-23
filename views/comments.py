import sqlite3
import json

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
            """,
            (postId,),
        )

        response = cursor.fetchall()

        comments = []
        for row in response:
            category = {"label": row["label"]}
            author = {"username": row["username"]}
            post = {"title": row["title"]}
            comment = {
                "id": row["commentId"],
                "content": row["content"],
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
            INSERT INTO Comments (post_id, author_id, content)
            VALUES (?, ?, ?)
            """,
            (body["post_id"], body["author_id"], body["content"]),
        )

        row_added = cursor.rowcount

    return True if row_added > 0 else False
