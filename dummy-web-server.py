#!/usr/bin/env python
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
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import SocketServer
import redis

class S(BaseHTTPRequestHandler):

    r_server = redis.Redis('localhost')

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        print self.path

        if self.path == "/":
            last_username = self.r_server.get('last_username')

            if not last_username:
                last_username = "EMPTY"

            with open('index.html', 'r') as myfile:
                data=myfile.read().replace('#last_username#',last_username)
                self.wfile.write(data)
        elif self.path == "/help":
            self.wfile.write("This is an example help page!")
        else:
            self.wfile.write("Page not found!")


    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
       
        self._set_headers()
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data

        if(self.path == "/submit-username"):
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)

            self.r_server.set('last_username', parsed_data['username'][0])

            with open('username-received.html', 'r') as myfile:
                data=myfile.read()
                data=data.replace('#username#', parsed_data['username'][0])
                self.wfile.write(data)
        else:
            self.wfile.write("Form handler not found!")
        
def run(server_class=HTTPServer, handler_class=S, port=8080):    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
