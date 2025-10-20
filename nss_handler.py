"""handle http status and url parsing"""

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler
from enum import Enum


class status(Enum):
    """Server response"""

    HTTP_200_OK = 200
    HTTP_201_SUCCESSFULLY_CREATED = 201
    HTTP_204_SUCCESS_NO_BODY = 204
    HTTP_CLIENT_ERROR_BAD_DATA = 400
    HTTP_CLIENT_ERROR_NOT_FOUND = 404
    HTTP_SERVER_ERROR = 500


class Handler(BaseHTTPRequestHandler):
    """set up url parse and handle requests"""

    def parse(self, path):
        url = urlparse(path)
        requested = url.path.split("/")[1]
        response_body = {"requested": requested, "queries": {}, "pk": 0}

        try:
            pk = url.path.split("/")[2]
            response_body["pk"] = int(pk)
        except (IndexError, ValueError):
            pass

        if url.query:
            queries = parse_qs(url.query)
            response_body["queries"] = queries

        return response_body

    def response(self, response_body, code):
        """HTTP RESPONSE"""

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response_body.encode("utf-8"))

    def do_OPTIONS(self):
        """do options"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.send_response(200)
