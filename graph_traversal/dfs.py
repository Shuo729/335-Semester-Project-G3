import networkx as nx
import matplotlib.pyplot as plt

def dfs(graph, node, visited=None):
    """
    Performs Depth-First Search on the graph starting from the given node.
    """
    if visited is None:
        visited = set()

    visited.add(node)
    for neighbor in graph.neighbors(node):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

def visualize_dfs(graph, start):
    """
    Visualizes DFS traversal of the graph.
    """
    visited = set()
    dfs(graph, start, visited)

    print(f"DFS Traversal Order: {visited}")

    # Shorten node labels for display
    labels = {node: shorten_label(node) for node in graph.nodes}

    nx.draw(graph, labels=labels, with_labels=True,
            node_color="lightgreen", node_size=2000, font_size=10)
    plt.show()

def shorten_label(label, max_len=30):
    """
    Shortens label to max_len characters.
    """
    return label if len(label) <= max_len else label[:max_len] + "..."