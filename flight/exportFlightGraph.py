def getEdgeAttributes():
    edgeAttributes = []
    edgeAttributes.append({
        "Name": "ID",
        "DisplayName": "id",
        "Type": "int",
        "DataType": "index",
        "Unique": "true"
    })

    edgeAttributes.append({
        "Name": "SourceID",
        "DisplayName": "source id",
        "Type": "int",
        "DataType": "source-index",
        "Unique": "false"
    })

    edgeAttributes.append({
        "Name": "TargetID",
        "DisplayName": "target id",
        "Type": "int",
        "DataType": "target-index",
        "Unique": "true"
    })

    edgeAttributes.append({
        "Name": "TargetID",
        "DisplayName": "target id",
        "Type": "int",
        "DataType": "target-index",
        "Unique": "true"
    })

    edgeAttributes.append({
        "Name": "Type",
        "DisplayName": "edge type",
        "Type": "string",
        "DataType": "categorical",
        "Unique": "false"
    })

    edgeAttributes.append({
        "Name": "LinkedStructures",
        "DisplayName": "structures",
        "Type": "string",
        "DataType": "string",
        "Unique": "false"
    })

    return edgeAttributes


def getNodeAttributes():
    nodeAttributes = []

    nodeAttributes.append({
        "Name": "ID",
        "DisplayName": "id",
        "Type": "int",
        "DataType": "index",
        "Unique": "true"
    })

    nodeAttributes.append({
        "Name": "degree",
        "DisplayName": "degree",
        "Type": "int",
        "DataType": "quantitative",
        "Unique": "false"
    })

    nodeAttributes.append({
        "Name": "airport",
        "DisplayName": "airport",
        "Type": "string",
        "DataType": "id",
        "Unique": "true"
    })

    nodeAttributes.append({
        "Name": "state",
        "DisplayName": "state",
        "Type": "string",
        "DataType": "categorical",
        "Unique": "false"
    })

    nodeAttributes.append({
        "Name": "airport_id",
        "DisplayName": "airport_id",
        "Type": "int",
        "DataType": "categorical",
        "Unique": "trye"
    })

    nodeAttributes.append({
        "Name": "city_name",
        "DisplayName": "city",
        "Type": "string",
        "DataType": "categorical",
        "Unique": "false"
    })

    nodeAttributes.append({
        "Name": "market",
        "DisplayName": "market",
        "Type": "int",
        "DataType": "categorical",
        "Unique": "false"
    })

    return nodeAttributes


def graphToJson(graph):
    nodes = []
    edges = []
    airport = graph.getStringProperty("airport")
    state = graph.getStringProperty("state")
    airport_id = graph.getStringProperty("airport_id")
    city_name = graph.getStringProperty("city_name")
    market = graph.getStringProperty("market")

    for node in graph.getNodes():
        dictionary = {
            "ID": node.id,
            "airport": airport[node],
            "state": state[node],
            "airport_id": airport_id[node],
            "city_name": city_name[node].replace("\"", ""),
            "degree": graph.deg(node),
            "market": market[node]
        }
        print dictionary
        nodes.append(dictionary)

    for edge in graph.getEdges():
        source = graph.source(edge)
        target = graph.target(edge)
        dictionary = {
            "ID": edge.id,
            "SourceID": int(source.id),
            "TargetID": int(target.id),
        }
        edges.append(dictionary)

    nodeAttributes = getNodeAttributes()
    edgeAttributes = getEdgeAttributes()

    return {
        "nodeAttributes": nodeAttributes,
        "nodes": nodes,
        "edgeAttributes": edgeAttributes,
        "edges": edges
    }
