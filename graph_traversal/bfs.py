import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs(graph, start):
    """
    Performs BFS traversal of the graph starting from the given node.
    """
    visited = set()
    queue = deque([start])
    traversal_order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            traversal_order.append(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)

    return traversal_order

def visualize_bfs(graph, start):
    """
    Visualizes BFS traversal of the graph.
    """
    traversal_order = bfs(graph, start)
    print(f"BFS Traversal Order: {traversal_order}")

    # Shorten node labels for display
    labels = {node: shorten_label(node) for node in graph.nodes}

    nx.draw(graph, labels=labels, with_labels=True,
            node_color="lightblue", node_size=2000, font_size=10)
    plt.show()

def shorten_label(label, max_len=30):
    """
    Shortens label to max_len characters.
    """
    return label if len(label) <= max_len else label[:max_len] + "..."