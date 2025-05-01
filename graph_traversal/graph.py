import networkx as nx

def build_reference_graph(documents):
    """
    Build a graph where nodes are documents and references, and edges represent citations.
    """
    G = nx.Graph()

    # Add documents and their references to the graph
    for doc, refs in documents:
        G.add_node(doc)  # Document node
        for ref in refs:
            G.add_node(ref)  # Reference node
            G.add_edge(doc, ref)  # Connect document to reference

    return G