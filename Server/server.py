from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Hello, world!')

PORT = int(os.environ.get("PORT", "8080"))
httpd = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()