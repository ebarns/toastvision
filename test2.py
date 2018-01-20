"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
import codecs
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import os
import binascii
import struct
import base64
from SimpleCV import *


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        PAGE = urllib.urlopen("../test.html")
        self._set_headers()
        self.wfile.write(PAGE.read())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print(self.headers)
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        data_string = post_data.split(":")[1][2:-3]
        im = base64.decodestring(data_string)
        image_result = open('../deer_decode.jpg', 'wb')  # create a writable image and write the decoding result
        image_result.write(im)
        image_result.close()

        browser_Image = Image("./deer_decode.png")
        browser_Image.show()

        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(8000))
    else:
        run()
