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
                p.id post_reaction_id,
                COUNT(p.reaction_id) as count

            FROM Reactions r
            LEFT JOIN PostReactions p
            ON reactionId = p.reaction_id AND p.post_id =?
            GROUP BY reactionId
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
                "count": row["count"],
            }
            reactions.append(reaction)

        serialized_reactions = json.dumps(reactions)

    return serialized_reactions
