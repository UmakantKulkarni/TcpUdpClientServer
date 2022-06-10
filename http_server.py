#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import socket
import os
import json
import glob
import argparse
import logging

logger = logging.getLogger(__name__)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("Received request from ", self.client_address[0])
        content = "Hello there!"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))
    
    def do_HEAD(self):
        self._set_headers()



def run(server_class=HTTPServer, handler_class=S, ip='0.0.0.0', port=8080):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    sa = httpd.socket.getsockname()
    logger.info("Starting httpd on %s:%s", sa[0], sa[1])
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__, formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--ip', '-s', help = 'The host that the server socket should bind to.', default = "0.0.0.0")
    parser.add_argument('--port', '-p', help = 'The port that the server socket should bind to.', type = int, default = 8080)
    parser.add_argument('--verbose', '-v', help = "Increases the logging verbosity level.", action = 'count')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.INFO,
                        format = '%(asctime)s %(levelname)s %(message)s')
    run(ip=args.ip, port=args.port)