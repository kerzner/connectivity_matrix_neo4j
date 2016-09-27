import py2neo as neo
from tulip import *
import tulippaths as tp

neo.authenticate('localhost:7474', 'neo4j', 'marclab')
neo_graph = neo.Graph('http://localhost:7474/db/data')

neo_graph.delete_all()

tulip_graph = tlp.loadGraph("data/network.tlp")

#tulip_hull = tulip_graph.getDoubleProperty("hull area")
#tulip_locations = tulip_graph.getDoubleProperty("locations")
tulip_structure = tulip_graph.getStringProperty("StructureURL")
tulip_to_neo_dict = {}

# Create neo4j nodes for each of the tulip nodes
for tulip_node in tulip_graph.getNodes():
    node_id = int(tp.utils.getNodeId(tulip_node, tulip_graph))

    node_type = tp.utils.getNodeType(tulip_node, tulip_graph)

#    node_locations = tulip_locations[tulip_node]
#    node_hull = tulip_hull[tulip_node]
    node_structure = tulip_structure[tulip_node]

#     neo_node = neo.Node("CELL",
#                         node_id,
#                         node_type,
#                         label=node_type,
#                         id=node_id,
#                        locations=node_locations,
#                        hull=node_hull,
#                         structure=node_structure)

    neo_node = neo.Node("CELL",
                        node_id,
                        node_type,
                        label=node_type,
                        id=node_id,
                        structure=node_structure)

    tulip_to_neo_dict[tulip_node] = neo_node

# Create neo4j edges for each of the tulip edges
tulip_edge_type = tulip_graph.getStringProperty("edgeType")
tulip_linked_structures = tulip_graph.getStringProperty("LinkedStructures")
neo_edges = []
for tulip_edge in tulip_graph.getEdges():
    tulip_source = tulip_graph.source(tulip_edge)
    tulip_target = tulip_graph.target(tulip_edge)
    id = tulip_edge.id

    edge_type = tulip_edge_type[tulip_edge]
    edge_linked_structures = tulip_linked_structures[tulip_edge]

    neo_source = tulip_to_neo_dict[tulip_source]
    neo_target = tulip_to_neo_dict[tulip_target]

    neo_edge = neo.Relationship(neo_source, "SYNAPSE", neo_target, type=edge_type, structures=edge_linked_structures, id=id)
    neo_edges.append(neo_edge)

for item in tulip_to_neo_dict.values() + neo_edges:
    neo_graph.create(item)
