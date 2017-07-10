from py2neo import Graph, Node, Relationship



graph = Graph("http://neo4j:123123@localhost:7474/db/data/")



#---------- Add new Node --------------------


def add_node(user_name):
    if not graph.find_one("User","name",user_name):
        new_node = Node("User", name=user_name)
        graph.create(new_node)


#----------- Add Relationship --------------

def add_rel(node1, node2):

    aa = graph.find_one("User","name",node1)

    bb = graph.find_one("User", "name", node2)

    following = Relationship(aa, "follows", bb)
    graph.create(following)
    return


#---------Print Relationaled Nodes

def print_rel_nodes():
    res = graph.run("MATCH (n) WHERE size((n)--()) > 0 RETURN n");
    for r in res:
        print r


#----------Print All The Nodes ------

def print_all():
    for record in graph.run("MATCH (p:User) RETURN p.name AS name"):
        print(record[0])



#--------- Related nodes -----------

def related_nodes(user):

    a = user

    for record in graph.run("MATCH (director { name: {X} })--(User) RETURN User.name", X = a):
        print(record[0])

#----------------Suggition
def sugg(user):

    b = user
    tre = graph.run("MATCH (person:User)-[:follows]-(friend:User)-[:follows]-(foaf:User) WHERE  person.name = {z} AND NOT (person)-[:follows]-(foaf) RETURN foaf", z = b);
    for k in tre:
        print k

#---------------------------------------------------
