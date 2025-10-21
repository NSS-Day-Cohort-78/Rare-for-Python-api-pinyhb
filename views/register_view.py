import sqlite3
import json

def list_users():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            *
        FROM Users
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        users=[]
        for row in query_results:
            users.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_users = json.dumps(users)

    return serialized_users

def register_user(user_data):
    with sqlite3.connect("./db.sqlite3") as conn:    
        # Query docks directly from the database
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT id FROM Users")

        db_cursor.execute(
            """
            INSERT INTO Users (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, 1)
            """,
            (user_data['first_name'], user_data['last_name'], user_data['email'], user_data['bio'], user_data['username'], user_data['password'])
        )
        new_id = db_cursor.lastrowid
        conn.commit()

    return new_id if new_id else False