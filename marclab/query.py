import py2neo as neo
from tulip import *
import tulippaths as tp

neo.authenticate('localhost:7474', 'neo4j', 'marclab')
neo_graph = neo.Graph('http://localhost:7474/db/data')

results = neo_graph.cypher.execute(""
                                   "MATCH p = (n)-[r:SYNAPSE]->(m)"
                                   "RETURN p "
                                   "LIMIT 10 ")

print results