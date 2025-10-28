import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return 
        valid boolean of True and the user's id as the token
        If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_all_users():

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                *
            FROM Users
            ORDER BY username
            """
        )

        response = cursor.fetchall()

        users = []
        for row in response:
            users.append(dict(row))

        serialized_users = json.dumps(users)
    return serialized_users


def get_user(pk):

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                *
            FROM Users
            WHERE id = ?
            """,
            (pk,),
        )

        response = cursor.fetchone()

        user = json.dumps(dict(response))
    return user

def add_new_subscription(subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES (?, ?, ?)
        """,
            (
                subscription["follower_id"],
                subscription["author_id"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
        )

        new_subscription_id = db_cursor.lastrowid
        response = json.dumps({"id": new_subscription_id, "success": True})

    return response

def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                *
            FROM Subscriptions
            ORDER BY created_on DESC
            """
        )

        response = cursor.fetchall()

        subscriptions = []
        for row in response:
            subscriptions.append(dict(row))

        serialized_subscriptions = json.dumps(subscriptions)
    return serialized_subscriptions