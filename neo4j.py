#from neo4jrestclient.client import GraphDatabase
from py2neo import Graph, Node, Relationship
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')





#setup connection

graph = Graph("http://neo4j:123123@localhost:7474/db/data/")

graph.delete_all()

w = Node("Person", name=" Wagdi ")
graph.create(w)

l = Node("Person", name="Luis")
graph.create(l)

o = Node("Person", name="Olga")
graph.create(o)



alice = Node("Person", name="Alice")
bob = Node("Person", name="Bob")

alice_knows_bob = Relationship(alice, "KNOWS", bob)
graph.create(alice_knows_bob)

graph.run("CREATE (c:Person {name:{N}}) RETURN c", {"N": "Carol"})
for record in graph.run("CREATE (d:Person {name:'Dave'}) RETURN d"):
    print(record)

for record in graph.run("MATCH (p:Person) RETURN p.name AS name"):
    print(record[0])

#for record in graph.run("MATCH (p:Person) RETURN p.name AS name"):
  #  print(record.name)

graph.create(Relationship(w, "friend", l))
graph.create(Relationship(w, "friend", o))
graph.create(Relationship(l, "friend", w))
-------------------------------------------














