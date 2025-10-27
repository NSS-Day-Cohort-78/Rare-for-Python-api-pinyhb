import sqlite3
import json

db = "db.sqlite3"

def get_all_post_tags():
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                t.id tagId,
                t.label,
                pt.post_id,
                p.id postId,
                p.title postTitle
            FROM PostTags pt
            JOIN Tags t
            ON t.id = pt.tag_id
            LEFT JOIN Posts p
            ON pt.post_id = p.id
            """
        )

        response = cursor.fetchall()

        post_tags = []

        for row in response:
            post = {
                "id": row["postId"],
                "title": row["postTitle"],
            }

            tag = {
                "id": row["tagId"],
                "label": row["label"],
            }

            post_tag = {
                "post": post,
                "tag": tag,
            }

            post_tags.append(post_tag)
    
        serialized_pt = json.dumps(post_tags)

    return serialized_pt
