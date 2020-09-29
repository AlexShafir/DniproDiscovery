from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
from io import BytesIO

dummy = {

"'Latent reserves' within the Swiss NFI":"https://search.earthdata.nasa.gov/search/granules?p=C1931110427-SCIOPS",

"(U-Th)/He ages from the Kukri Hills of southern Victoria Land":"https://search.earthdata.nasa.gov/search/granules?p=C1214587974-SCIOPS"

}


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = BytesIO()
        response.write(str.encode(json.dumps(dummy)))
        self.wfile.write(response.getvalue())

PORT = int(os.environ.get("PORT", "8080"))
httpd = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()