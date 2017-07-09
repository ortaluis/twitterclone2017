from py2neo import Graph, Node, Relationship
import neo4j
graph = Graph("http://neo4j:123123@localhost:7474/db/data/")


graph.delete_all()


u1 = "Wagdi"
u2 = "Bob"

neo4j.add_node(u1)
neo4j.add_node(u2)

neo4j.add_rel(u1, u2)


neo4j.print_all()