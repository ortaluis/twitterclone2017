from py2neo import Graph, Node, Relationship
import neo4j
graph = Graph("http://neo4j:123123@localhost:7474/db/data/")


graph.delete_all()


u1 = "Wagdi"
u2 = "Olga"
u3 = "Luis"
u4 = "Bob"
u5 = "Mary"
u6 = "Rhul"
u7 = "Fadi"
u8 = "Newboy"
u10 = "alon"

#-------------------------creating nodes----------------------------
neo4j.add_node(u1)
neo4j.add_node(u2)
neo4j.add_node(u3)
neo4j.add_node(u4)
neo4j.add_node(u5)
neo4j.add_node(u6)
neo4j.add_node(u7)
neo4j.add_node(u8)
neo4j.add_node(u10)

#---------------------------creating Relationships -------------------
neo4j.add_rel(u1, u2)

neo4j.add_rel(u1, u3)

neo4j.add_rel(u2, u4)

neo4j.add_rel(u2, u5)

neo4j.add_rel(u3, u6)

neo4j.add_rel(u3, u7)

neo4j.add_rel(u7, u8)

#---------------------- anothers Neo4j Methods ----------------------


#neo4j.sugg(u1)
#neo4j.print_rel_nodes()
#neo4j.related_nodes(u1)
#neo4j.print_all()