import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph

"""
This script can visualize a turtle knowledge graph file.
"""

# Load the RDF graph from the Turtle file
g = Graph()
g.parse("knowledge_graph.ttl", format="turtle")

nx_graph = nx.DiGraph()

for s, p, o in g:
    nx_graph.add_node(s, label=s.split("/")[-1])
    nx_graph.add_node(o, label=o.split("/")[-1] if isinstance(o, str) else str(o))
    nx_graph.add_edge(s, o, label=p.split("/")[-1])

pos = nx.spring_layout(nx_graph)
labels = nx.get_node_attributes(nx_graph, "label")
edge_labels = nx.get_edge_attributes(nx_graph, "label")

plt.figure(figsize=(12, 12))
nx.draw(
    nx_graph,
    pos,
    labels=labels,
    with_labels=True,
    node_size=3000,
    node_color="skyblue",
    font_size=10,
    font_weight="bold",
    edge_color="gray",
)
nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_color="red")

plt.savefig("knowledge_graph.png", format="png")

plt.show()
