"""Main Server"""

from http.server import HTTPServer
import json
from nss_handler import HandleRequests, status
from views import get_posts, get_post_by_id, delete_post, update_post, create_post, get_posts_by_tag
from views import create_user, login_user, get_all_users, get_user
from views import (
    get_categories,
    create_category,
    delete_category,
    get_category_by_id,
    update_category,
)
from views import (
    get_all_comments,
    create_comment,
    edit_comment,
    get_comment_by_id,
    delete_comment,
)
from views import (
    get_post_reactions,
    create_reaction,
    get_all_reactions,
    create_post_reaction,
)
from views import (
    get_all_tags,
    get_tag_by_id,
    update_tag,
    delete_tag,
    create_tag,
    get_post_tags,
)


class Json_Server(HandleRequests):
    """GET, POST, PUT, DELETE"""

    def do_GET(self):
        """GET requests"""

        response = self.parse_url(self.path)
        pk = response["pk"]

        if response["requested_resource"] == "posts":
            if pk > 0:
                request = get_post_by_id(pk)
                self.response(request, status.HTTP_200_SUCCESS.value)
            else:
                request = get_posts()
                self.response(request, status.HTTP_200_SUCCESS.value)

        if response["requested_resource"] == "categories":
            if pk > 0:
                request = get_category_by_id(pk)
                self.response(request, status.HTTP_200_SUCCESS.value)
            else:
                request = get_categories()
                return self.response(request, status.HTTP_200_SUCCESS.value)

        if response["requested_resource"] == "users":
            if pk > 0:
                request = get_user(pk)
                return self.response(request, status.HTTP_200_SUCCESS.value)
            else:
                request = get_all_users()
                return self.response(request, status.HTTP_200_SUCCESS.value)

        if response["requested_resource"] == "comments":
            if pk > 0:
                request = get_comment_by_id(pk)
                return self.response(request, status.HTTP_200_SUCCESS.value)
            else:
                request = get_all_comments(response)
                return self.response(request, status.HTTP_200_SUCCESS.value)
        if response["requested_resource"] == "post-reaction":
            if pk > 0:
                request = get_post_reactions(pk)
                return self.response(request, status.HTTP_200_SUCCESS.value)
        if response["requested_resource"] == "reactions":
            if pk > 0:
                pass
            else:
                request = get_all_reactions()
                return self.response(request, status.HTTP_200_SUCCESS.value)
        if response["requested_resource"] == "tags":
            if pk > 0:
                request = get_tag_by_id(pk)
                return self.response(request, status.HTTP_200_SUCCESS.value)
            else:
                request = get_all_tags()
                return self.response(request, status.HTTP_200_SUCCESS.value)
        if response["requested_resource"] == "post-tags":
            if pk > 0:
                request = get_post_tags(pk)
                return self.response(request, status.HTTP_200_SUCCESS.value)

    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "users":
            new_id = create_user(request_body)
            if new_id:
                return self.response(new_id, status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "login":
            response = login_user(request_body)
            return self.response(response, status.HTTP_200_SUCCESS.value)
        elif url["requested_resource"] == "posts":
            if url["pk"] == 0:
                response = create_post(request_body)
                return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "comments":
            response = create_comment(request_body)
            if response:
                return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "categories":
            response = create_category(request_body)
            if response:
                return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "reactions":
            response = create_reaction(request_body)
            if response:
                return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "post-reaction":
            response = create_post_reaction(request_body)
        elif url["requested_resource"] == "tags":
            response = create_tag(request_body)
            if response:
                return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_DELETE(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "posts":
            if pk > 0:
                response = delete_post(pk)
                if response:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "categories":
            if pk > 0:
                response = delete_category(pk)
                if response:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "comments":
            if pk > 0:
                response = delete_comment(pk)
                if response:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "comments":
            if pk > 0:
                response = delete_comment(pk)
                if response:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
        if url["requested_resource"] == "tags":
            if pk > 0:
                response = delete_tag(pk)
                if response:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)

    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "posts":
            if pk != 0:
                try:
                    successfully_updated = update_post(pk, request_body)
                    if successfully_updated:
                        return self.response(
                            "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                        )
                    else:
                        return self.response(
                            json.dumps({"error": "Post not found"}),
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )
                except Exception as e:
                    return self.response(
                        json.dumps({"error": str(e)}),
                        status.HTTP_500_SERVER_ERROR.value,
                    )
        if url["requested_resource"] == "comments":
            if pk != 0:

                successfully_updated = edit_comment(request_body, pk)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        if url["requested_resource"] == "edit-category":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                return self.response(
                    json.dumps({"error": "Category not found"}),
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )
        if url["requested_resource"] == "tags":
            if pk != 0:
                successfully_updated = update_tag(pk, request_body)

                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
                return self.response(
                    json.dumps({"error": "Tag not found"}),
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )


def main():
    """open the server"""
    host = ""
    port = 8088
    HTTPServer((host, port), Json_Server).serve_forever()


if __name__ == "__main__":
    main()
