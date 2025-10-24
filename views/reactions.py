import sqlite3
import json

db = "db.sqlite3"


def get_post_reactions(id):
    """GET reactions from post id"""

    with sqlite3.connect(db) as conn:

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                r.id reactionId,
                r.label,
                r.image_url,
                p.post_id,
                p.reaction_id,
                p.user_id,
                p.id post_reaction_id
            FROM Reactions r
            JOIN PostReactions p
            ON reactionId = p.reaction_id
            WHERE p.post_id = ?
            """,
            (id,),
        )
        response = cursor.fetchall()

        reactions = []
        for row in response:
            post_reactions = {
                "id": row["post_reaction_id"],
                "user_id": row["user_id"],
                "reaction_id": row["reaction_id"],
                "post_id": row["post_id"],
            }
            reaction = {
                "id": row["reactionId"],
                "label": row["label"],
                "image_url": row["image_url"],
                "post_reactions": post_reactions,
            }
            reactions.append(reaction)

        serialized_reactions = json.dumps(reactions)

    return serialized_reactions
