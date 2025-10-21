"""Main Server"""

from http.server import HTTPServer
import json
from nss_handler import HandleRequests, status
from views import get_posts
from views import create_user, login_user


class Json_Server(HandleRequests):
    """GET, POST, PUT, DELETE"""

    def do_GET(self):
        """GET requests"""

        response = self.parse_url(self.path)
        pk = response["pk"]

        if response["requested_resource"] == "posts":
            if pk > 0:
                pass
            else:
                request = get_posts()
                self.response(request, status.HTTP_200_SUCCESS.value)

    def do_POST(self):
        url = self.parse_url(self.path)
        pk = ["pk"]

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "users":
            new_id = create_user(request_body)
            if new_id:
                return self.response(
                    new_id, status.HTTP_201_SUCCESS_CREATED.value
                )
        elif url["requested_resource"] == "login":
            response = login_user(request_body)
            return self.response(response, status.HTTP_200_SUCCESS.value)
        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


def main():
    """open the server"""
    host = ""
    port = 8088
    HTTPServer((host, port), Json_Server).serve_forever()


if __name__ == "__main__":
    main()
