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
            filename = self.path.split('&')[0][:-1]
            with open('temp'+filename, 'w') as f:
                dump(data, f)

    def do_POST(self):
        length = self.headers['content-length']
        data = self.rfile.read(int(length))

        with open("store.json", 'w') as fh:
            fh.write(data.decode())

        self.send_response(200)

server = HTTPServer(('', 3979), StoreHandler)
print("Starting server")
server.serve_forever()