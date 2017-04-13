"""
The MIT License (MIT)

Copyright (c) 2017 Funky7Monkey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from os import curdir
from os.path import join as pjoin
from json import dump

from http.server import BaseHTTPRequestHandler, HTTPServer

class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.headers)
        if self.path == "/favicon.ico":
            self.send_response(200)
        elif self.path.startswith('/oauth'):
            self.send_response(200)
            datapart = self.path.split('?')[1]
            data = dict((r.split('=')[0],r.split('=')[1]) for r in datapart.split('&')[1:])

            with open("store.json", 'w') as fh:
                dump(data, fh)
            with open("home.html") as page:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(page.read().encode())
        else:
            self.send_response(200)
            with open("home.html") as page:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(page.read().encode())
            data = dict((r.split('=')[0],r.split('=')[1]) for r in self.path.split('&')[1:])
            with open("store.json", 'w') as f:
                dump(data, f)

    def do_POST(self):
        length = self.headers['content-length']
        data = self.rfile.read(int(length))

        with open("store.json", 'w') as fh:
            fh.write(data.decode())

        self.send_response(200)

def server(port):
    server = HTTPServer(('', port), StoreHandler)
    return server
