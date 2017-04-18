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
import time

import socket

from http.server import BaseHTTPRequestHandler, HTTPServer

data = {}
fn = ''

class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global data
        global fn
        if self.path == "/favicon.ico":
            self.close_connection = False
            self.send_response(200)
        else:
            if fn == self.path.split('&')[0][:-1]:
                data = dict((r.split('=')[0], r.split('=')[1])
                            for r in self.path.split('&')[1:])
                self.send_response(200)
                with open("home.html") as page:
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(page.read().encode())
            else:
                self.close_connection = False

class server:
    def __init__(self, port, identifier):
        global fn
        fn = '/' + identifier
        self.s = HTTPServer(('', port), StoreHandler)

    def getData(self):
        global data
        self.s.handle_request()
        return data
