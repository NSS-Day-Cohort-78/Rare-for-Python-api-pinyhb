import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import create_user, login_user

class JSONServer(HandleRequests):

    def do_POST(self):
        url = self.parse_url(self.path)
        pk = ["pk"]

        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            if url["pk"] == 0:
                successfully_added = create_user(request_body)
                if successfully_added:
                    return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "login":
            response = login_user(request_body)
            return self.response(response, status.HTTP_200_SUCCESS.value)
        else:
            return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()
