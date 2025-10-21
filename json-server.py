import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
# from views import register_user, list_users
from views import create_user

class JSONServer(HandleRequests):
    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            response_body = list_users()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
    def do_POST(self):
        """Handle POST requests from a client"""
        # Parse the URL and get the primary key
        url = self.parse_url(self.path)
        # pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "users":
            # if pk == 0:
            new_id = create_user(request_body)
            if new_id:
                return self.response(
                    new_id, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                )
                
        return self.response(
            "Requested resource not found",
            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
        )

def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()