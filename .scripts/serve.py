from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import json
import sys
import os

from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT / "api"))
sys.path.insert(0, str(ROOT))

import Functions
from handlers import execute_function, get_all_metadata

def _getPageHtml(devMode = False) -> str:
    pageHtmlFormat = """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>Custom Functions</title>
    <link rel="stylesheet" href="https://static2.sharepointonline.com/files/fabric/office-ui-fabric-core/9.6.1/css/fabric.min.css">
    <script src="https://{0}/agave/external/react-16-12-0/umd/react.development.js"></script>
    <script src="https://{0}/agave/external/react-dom-16-12-0/umd/react-dom.development.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.5/require.min.js"></script>
    <script type="text/javascript" src="https://appsforoffice.microsoft.com/lib/1.1/hosted/office.debug.js"></script>
    <script type="text/javascript" src="https://{0}/agave/custom-function-forwarder.bundle.js"></script>
</head>
    <body>
        <div id="DivApp">
        </div>
        <div id="DivLog">
        </div>
    </body>
</html>
    """
    if devMode:
        host = "localhost:8080"
    else:
        host = "exceljupyter.azurewebsites.net"
    return pageHtmlFormat.format(host)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/functions?invoke="):
            _, _, payload = self.path.partition("?invoke=")
            data = json.loads(unquote(payload))
            self._send_json(execute_function(Functions, data))
        elif self.path == "/functions":
            self._send_json(get_all_metadata(Functions))
        elif self.path == "/functions.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html;charset=utf-8")
            devMode = False
            if bool(os.getenv("EXCEL_DEVMODE")):
                devMode = True
            pageHtml = _getPageHtml(devMode=devMode).encode()
            self.send_header("Content-Length", str(pageHtml))
            self.end_headers()
            self.wfile.write(pageHtml)
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


httpd_address = ['localhost', 5000]
if len(sys.argv) >= 2:
    if sys.argv[1] in {"-h", "-?"}:
        print("Usage: python3 .scripts/serve.py [HOST=localhost [PORT=5000]]")
        sys.exit(1)

    httpd_address[0] = sys.argv[1]
if len(sys.argv) >= 3:
    httpd_address[1] = int(sys.argv[2])

httpd = HTTPServer(('localhost', 5000), Handler)
httpd.serve_forever()
