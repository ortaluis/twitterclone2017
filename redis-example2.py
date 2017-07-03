import redis

r_server = redis.Redis('localhost') #this line creates a new Redis object and
                                    #connects to our redis server
r_server.set('olga', 'test') #with the created redis object we can
                                        #submits redis commands as its methods
                                        
print 'olga: ' + r_server.get('olga') # the previous set key is fetched
