import json
from py2neo import Graph, Path, Node, Relationship, authenticate
import exportFlightGraph

authenticate('localhost:7474', 'neo4j', 'neo')

graph = Graph('http://localhost:7474/db/data/')

print 'starting query!'
"""
results = graph.cypher.execute(""
                               "MATCH p = (n:California)-[r:FLIGHT*1..3]->(m)"
                               "WHERE ALL(n in nodes(p) where 1 = size(filter(m in nodes(p) where m = n)))"
                               #"AND m.state in ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont']"
                               "RETURN p,length(p) ORDER BY length(p) limit 50000")
"""

results = graph.cypher.execute(""
                               "MATCH p = (n:California)-[r:FLIGHT]->(m)"
                               "WHERE ALL(n in nodes(p) where 1 = size(filter(m in nodes(p) where m = n)))"
                               "RETURN p,length(p)")

for result in results:
    print result
    path = Path(result.p)
    for relationship in path.relationships:
       print relationship
    break

"""
nodes = []
g = tlp.newGraph()
node_property_names = ["airport", "state", "airport_id", "city_name", "market"]
edge_property_names = ["carrier", "airtime", "distance", "refs"]
edge_property_carrier = g.getStringProperty(edge_property_names[0])
edge_property_airtime = g.getDoubleProperty(edge_property_names[1])
edge_property_distance = g.getDoubleProperty(edge_property_names[2])
edge_property_refs = g.getStringProperty(edge_property_names[3])

print 'converting graph!'
node_properties = []
for p in node_property_names:
    node_properties.append(g.getStringProperty(p))
viewColor = g.getColorProperty("viewColor")
viewLabel = g.getStringProperty("viewLabel")
viewSize = g.getSizeProperty("viewSize")
def get_or_create_tulip_node(neo_node, g):
    property_airport = node_properties[0]
    for node in g.getNodes():
        if property_airport[node] == neo_node.properties["airport"]:
            return node
    node = g.addNode()

    for i in range(0, len(node_property_names)):
        node_properties[i][node] = str(neo_node.properties[node_property_names[i]])
    viewColor[node] = tlp.Color(50, 50, 50)
    viewLabel[node] = neo_node.properties["airport"]
    viewSize[node] = tlp.Size(1, 1, 1)
    return node

refs = []
def get_or_create_edge(neo_edge, source, target, g):
    if neo_edge.ref in refs:
        for edge in g.getEdges():
            if edge_property_refs[edge] == neo_edge.ref:
                return edge
    else:
        edge = g.addEdge(source, target)
        edge_property_carrier[edge] = neo_edge.properties[edge_property_names[0]]
        edge_property_distance[edge] = neo_edge.properties[edge_property_names[1]]
        edge_property_airtime[edge] = neo_edge.properties[edge_property_names[2]]
        edge_property_refs[edge] = str(neo_edge.ref)
        viewColor[edge] = tlp.Color(155, 155, 155)
        refs.append(neo_edge.ref)
        return edge


tPaths = []
for r in results:
    path = Path(r.p)
    tPath = tp.Path(g)
    for i in range(0, len(path.relationships)):
        neo_edge = path.relationships[i]
        source = get_or_create_tulip_node(neo_edge.start_node, g)
        target = get_or_create_tulip_node(neo_edge.end_node, g)
        edge = get_or_create_edge(neo_edge, source, target, g)
        tPath.addNode(source)
        tPath.addEdge(edge)

        if i == (len(path.relationships) - 1):
            tPath.addNode(target)
    tPaths.append(tPath)

for tPath in tPaths:
    if not tPath.isSane():
        print 'Bad path!'
print 'generating matrix'
matrix = tp.ConnectivityMatrix(g)
matrix.activateFromPaths(tPaths)

print 'dumping to json'
californiaToTexasMatrix = matrix.getAsJsonObject(True)
californiaToTexasGraph = exportFlightGraph.graphToJson(g)

output = open('mockFlights.js', 'w')
output.write("var flights = {};\n")
output.write("flights.californiaToTexasGraph = " + json.dumps(californiaToTexasGraph) + ";\n")
output.write("flights.californiaToTexasMatrix = " + json.dumps(californiaToTexasMatrix) + ";\n")

output.close()

tlp.saveGraph(g, "shit.tlp")
#print json.dumps()
tlpgui.createNodeLinkDiagramView(g)
"""

