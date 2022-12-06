from http.server import BaseHTTPRequestHandler
from typing import List, Tuple


class ServerUtils:

    @staticmethod
    def writeResponse(RH: BaseHTTPRequestHandler, content: str,
                      code: int = 200, content_type: str = "application/json",
                      extra_headers: List[Tuple[str, str]] = None):

        if extra_headers is None:
            extra_headers = []

        RH.send_response(code)

        for xtra_header in extra_headers:
            RH.send_header(xtra_header[0], xtra_header[1])

        RH.send_header('Content-type', content_type)
        RH.end_headers()
        RH.wfile.write(content.encode("utf-8"))
