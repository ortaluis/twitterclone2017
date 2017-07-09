from py2neo import Graph, Node, Relationship
from pymongo import MongoClient


graph = Graph("http://neo4j:123@localhost:7474/db/data/")


#graph.delete_all()
client = MongoClient('mongodb://localhost:27017/')

user1 = "olga"
user2 = "mohammed"
user3 = "luis"

o = Node("User", user=user1)
#graph.create(o)

g = Node("User", user=user2)
#graph.create(g)

following = Relationship(o,"follows", g)
graph.create(following)







