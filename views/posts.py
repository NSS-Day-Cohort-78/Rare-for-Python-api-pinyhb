"""Post Views"""

import sqlite3
import json
from datetime import datetime

db = "db.sqlite3"


def get_posts():
    """Get Posts"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                p.id postId,
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
                u.bio,
                u.id userId,
                c.id categoryId,
                c.label 
            FROM Posts p
            JOIN Users u
            ON userId = p.user_id
            JOIN Categories c
            ON p.category_id = categoryId
            ORDER BY p.publication_date DESC
            """
        )
        response = cursor.fetchall()

        posts = []

        for row in response:
            user = {
                "id": row["userId"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "bio": row["bio"],
            }

            category = {"id": row["categoryId"], "label": row["label"]}

            post = {
                "id": row["postId"],
                "category": category,
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
                "user": user,
            }
            posts.append(post)

        serialized_posts = json.dumps(posts)
    return serialized_posts


def get_post_by_id(pk):
    """get a single post"""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                p.id postId,
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
                u.bio,
                u.id userId,
                u.username,
                c.id categoryId,
                c.label 
            FROM Posts p
            JOIN Users u
            ON userId = p.user_id
            JOIN Categories c
            ON p.category_id = categoryId
            WHERE postId = ?
            """,
            (pk,),
        )

        response = cursor.fetchone()

        user = {
            "id": response["userId"],
            "first_name": response["first_name"],
            "last_name": response["last_name"],
            "email": response["email"],
            "bio": response["bio"],
            "username": response["username"],
        }

        category = {"id": response["categoryId"], "label": response["label"]}

        post = {
            "id": response["postId"],
            "category": category,
            "title": response["title"],
            "publication_date": response["publication_date"],
            "image_url": response["image_url"],
            "content": response["content"],
            "approved": response["approved"],
            "user": user,
        }
        serialized_post = json.dumps(post)

    return serialized_post


def delete_post(pk):

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM Posts
            WHERE id = ?
            """,
            (pk,),
        )

        row_affected = cursor.rowcount

    return True if row_affected > 0 else False


def update_post(pk, post_data):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Posts
                SET
                    title = ?,
                    category_id = ?,
                    content = ?
            WHERE id = ?
            """,
            (post_data["title"], post_data["category_id"], post_data["content"], pk),
        )

        rows_affected = cursor.rowcount

    return True if rows_affected > 0 else False

def create_post(post):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES (?, ?, ?, ?, ?, ?, 1)
        """,(
            post['user_id'],
            post['category_id'],
            post['title'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            post['image_url'],
            post['content']
        ))

        new_post_id = db_cursor.lastrowid
        response = json.dumps({
            'id': new_post_id,
            'success': True
        })

    return response

def list_categories():
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT c.id, c.label FROM Categories c
        """)

        query_results = db_cursor.fetchall()

        categories = []
        for row in query_results:
            categories.append(dict(row))

        serialized_categories = json.dumps(categories)

    return serialized_categories
