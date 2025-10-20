"""Main Server"""

from http.server import HTTPServer
from nss_handler import Handler, status
from views import get_posts
from views import login_user


class Json_Server(Handler):
    """GET, POST, PUT, DELETE"""

    def do_GET(self):
        """GET requests"""

        response = self.parse(self.path)
        pk = response["pk"]

        if response["requested"] == "posts":
            if pk > 0:
                pass
            else:
                request = get_posts()
                self.response(request, status.HTTP_200_OK.value)


def main():
    """open the server"""
    host = ""
    port = 8088
    HTTPServer((host, port), Json_Server).serve_forever()


if __name__ == "__main__":
    main()
