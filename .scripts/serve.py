from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT / "api"))
sys.path.insert(0, str(ROOT))

import Functions
from handlers import execute_function, get_all_metadata


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/functions":
            self._send_json(get_all_metadata(Functions))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/functions":
            data = json.loads(self.rfile.read(int(self.headers["Content-Length"])).decode())
            self._send_json(execute_function(Functions, data))
        else:
            self.send_error(404)

    def _send_json(self, data):
        if not isinstance(data, (str, bytes)):
            data = json.dumps(data)
        if not isinstance(data, bytes):
            data = data.encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json;charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


server_address = ('', 5000)
httpd = HTTPServer(('', 5000), Handler)
httpd.serve_forever()
