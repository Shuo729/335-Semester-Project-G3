import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(graph):
    """
    Visualizes the graph using NetworkX and Matplotlib.
    """
    nx.draw(graph, with_labels=True, node_color="lightcoral", node_size=2000, font_size=12)
    plt.show()
