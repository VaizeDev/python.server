from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from datetime import datetime


class DemoServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

    def do_GET(self):
        print(f"GET request: {self.path}")

        if self.path == "/api/time":
            self.send_json({
                "serverTime": datetime.now().strftime("%H:%M:%S"),
                "message": "This is answer from the Python server."
            })
            return

        super().do_GET()

    def do_POST(self):
        print(f"POST request: {self.path}")

        if self.path == "/api/greet":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, status=400)
                return

            name = data.get("name", "my friend")

            self.send_json({
                "message": f"Hello, {name}! This message is from the server."
            })
            return

        self.send_json({"error": "Not found"}, status=404)

    def send_json(self, data, status=200):
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    server = ThreadingHTTPServer((host, port), DemoServer)

    print(f"Server started: http://{host}:{port}")
    server.serve_forever()