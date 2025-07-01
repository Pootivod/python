from multiprocessing import Process
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import os

load_dotenv("./configs/.env")
PORT = int(os.getenv("PORT", 8000))

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received request for {self.path}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")

class Server:
    def __init__(self, port=PORT):
        self.port = port
        self.server = HTTPServer(('0.0.0.0', self.port), HttpHandler)

    def start(self):
        print(f"Starting server on port {self.port}...")
        self.server.serve_forever()

if __name__ == '__main__':
    server = Server()
    server.start()