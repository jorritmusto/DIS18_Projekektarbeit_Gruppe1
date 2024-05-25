import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace

# Load data
excel_nodes = pd.read_excel('data/nodes_zjb999093409sd1.xlsx')
excel_edges = pd.read_excel('data/edges_zjb999093409sd1.xlsx')

# Create an RDF graph
g = Graph()

# Define a namespace
EX = Namespace('http://example.org/')

# Bind the namespace to a prefix for easier querying
g.bind('ex', EX)

# Add nodes to the graph
for _, row in excel_nodes.iterrows():
    node_uri = URIRef(EX[row['pos_id']])
    g.add((node_uri, EX.strand, Literal(row['strand'])))
    g.add((node_uri, EX.locus_tag, Literal(row['locus_tag'])))
    g.add((node_uri, EX.product, Literal(row['product'])))
        # Add other TSS-specific properties as needed

# Add edges to the graph
for _, row in excel_edges.iterrows():
    source_uri = URIRef(EX[row['source_id']])
    target_uri = URIRef(EX[row['target_id']])
    relationship_uri = URIRef(EX[row['relationship']])
    g.add((source_uri, relationship_uri, target_uri))

# Serialize the graph to a file
g.serialize(destination='output_graph.ttl', format='turtle')



