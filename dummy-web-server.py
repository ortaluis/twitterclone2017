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

from pymongo import MongoClient
from py2neo import Graph, Node
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import SocketServer
import redis

graph = Graph("http://neo4j:123123@localhost:7474/db/data/")




class S(BaseHTTPRequestHandler):

    r_server = redis.Redis('localhost')
    client = MongoClient('mongodb://localhost:27017/')

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    #and here are what a python web-server must do after someone write a page name in the browser
    def do_GET(self):
        #Response auf brower request
        self._set_headers()

        print self.path

        #What to do if a user enter in a browser just: http://localhost
        if self.path == "/":

            #self.r_server.delete('counter')

             # 2.you get them from redis..but wit: where did we defined "last-usermae?"
            last_username = self.r_server.get('last_username')
            #resultNumberOfUsers = self.r_server.hget('usersNumber', 'numberOfUsers')

           #1. defined by you..
            numberOfUsers ="0"
            
            if self.r_server.exists('counter'):
                numberOfUsers = self.r_server.get('counter')            
                print 'Test:' + numberOfUsers

            if not last_username:
                last_username = "EMPTY"

            #in order to post stuff on you page in html you can get them from..

            # so if you enter to your main page you need to open a html page called "index.html"
            with open('index.html', 'r') as myfile:
                #and replace the 2 variables that this page is wating for: (both you get from redis)
                data=myfile.read().replace('#last_username#',last_username)
                data=data.replace('#usersNumber#',numberOfUsers)
                self.wfile.write(data)

        elif self.path == "/help":
            self.wfile.write("This is an example help page!")

        elif self.path == "/sign-up":
            last_username = self.r_server.get('last_username')
            olga_password = self.r_server.hget('users', "olga")

            if olga_password == "1234":
               print 'right password'

            if not last_username:
                last_username = "EMPTY"

            with open('sign-up.html', 'r') as myfile:
                data=myfile.read().replace('#last_username#',last_username)
                self.wfile.write(data)

        else:
            self.wfile.write("Page not found!")


    def do_HEAD(self):
        self._set_headers()

    # so here are all your responess to..
    def do_POST(self):
        # ....what to do with the submitted data from the user (in those forms that appears inside the html pages)
        self._set_headers()
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data

        #If the data belongs to a form with this tag.. (that was defined in index.html- the data of do_GET)    
        if(self.path == "/submit-exist"):
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)

            if (parsed_data['password'][0] != self.r_server.hget('users',parsed_data['username'][0])):
                with open('username-NOTreceived.html', 'r') as myfile:
                    data=myfile.read()
                    self.wfile.write(data)
                return       
             #here you can add stuff to my-twiiter page..
            with open('my-twitter.html', 'r') as myfile:
                data=myfile.read()
                self.wfile.write(data)


       #submit-username is not a page in html but a form that is found in a html page called..sign-up.html
        elif(self.path == "/submit-username"):
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)

            if (parsed_data['password'][0] != parsed_data['repeat-password'][0]):
                with open('username-NOTreceived.html', 'r') as myfile:
                    data=myfile.read()
                    self.wfile.write(data)
                return       

            #like this example: you can set stuff in redis
            #'here!!' we defined a variable that we want later to use in a page in html..
            self.r_server.set('last_username', parsed_data['username'][0])

            self.r_server.set('last_password', parsed_data['password'][0])

            self.r_server.set(parsed_data['username'][0],parsed_data['password'][0])



            print 'previous key set the value: ' + self.r_server.get(parsed_data['username'][0])

            self.r_server.hset('users', parsed_data['username'][0],parsed_data['password'][0] )
            print 'the value for this key in the hash is %s:'% self.r_server.hget('users',parsed_data['username'][0] )

            
            if(not self.r_server.exists('counter')):
                self.r_server.set('counter',1)
            else:
                self.r_server.incr('counter',1)

            with open('username-received.html', 'r') as myfile:
                data=myfile.read()
                #you see here: variables username and password are replaced in a page called "username-received.html" with some variables
                # that are read from a form: what a form? see now..
                data=data.replace('#username#', parsed_data['username'][0])
                data=data.replace('#password#', parsed_data['password'][0])
                self.wfile.write(data)


        elif self.path == "/submit-login":
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            parsed_data = parse_qs(post_data)


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
