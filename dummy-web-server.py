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
        #Response auf brower request
        self._set_headers()

        print self.path

        #What to do if a user enter in a browser just: http://localhost
        if self.path == "/":
            last_username = self.r_server.get('last_username')
            numberOfUsers = self.r_server.get('counter')
            #resultNumberOfUsers = self.r_server.hget('usersNumber', 'numberOfUsers')

            print 'Test: %s' + numberOfUsers

            if not last_username:
                last_username = "EMPTY"

            with open('index.html', 'r') as myfile:
                data=myfile.read().replace('#last_username#',last_username)
                #data=myfile.read().replace('#usersNumber#',numberOfUsers)
                self.wfile.write(data)

        elif self.path == "/help":
            self.wfile.write("This is an example help page!")

        elif self.path == "/sign-up":
            last_username = self.r_server.get('last_username')

            if not last_username:
                last_username = "EMPTY"

            with open('sign-up.html', 'r') as myfile:
                data=myfile.read().replace('#last_username#',last_username)
                self.wfile.write(data)

        else:
            self.wfile.write("Page not found!")


    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # what to do with the submitted data from the user
        self._set_headers()
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        self.r_server.set('counter', 1)

        #If the data belongs to a form with this tag.. (that was defined in index.html- the data of do_GET)    
        if(self.path == "/submit-exist"):
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)

            with open('my-twitter.html', 'r') as myfile:
                data=myfile.read()
                self.wfile.write(data)


        elif(self.path == "/submit-username"):
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)

            self.r_server.set('last_username', parsed_data['username'][0])
            self.r_server.set('last_password', parsed_data['password'][0])

            self.r_server.set(parsed_data['username'][0],parsed_data['password'][0])
            print 'previous set the value: ' + self.r_server.get(parsed_data['username'][0])

            self.r_server.hset('users', parsed_data['username'][0],parsed_data['password'][0] )
            print 'the value for this key in the hash is %s:'% self.r_server.hget('users',parsed_data['username'][0] )

            self.r_server.incr('counter',1)

            with open('username-received.html', 'r') as myfile:
                data=myfile.read()
                data=data.replace('#username#', parsed_data['username'][0])
                data=data.replace('#password#', parsed_data['password'][0])
                self.wfile.write(data)


        elif self.path == "/submit-login":
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)

            #self.numberOfUsers += 1
            #self.r_server.hset('usersNumber', 'numberOfUsers' ,self.numberOfUsers)
            #print 'the number of users is %s:'% self.r_server.hget('usersNumber', 'numberOfUsers')

            with open('login-received.html', 'r') as myfile:
                data=myfile.read()
                data=data.replace('#name#', parsed_data['name'][0])
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
