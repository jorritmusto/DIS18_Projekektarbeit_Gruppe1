import requests
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

"""
This script first sends a request to the Wikibase instance to gather all information available. After that, with the results of the query a knowledge graph is created.
"""

# Wikibase Cloud SPARQL endpoint URL -> from 'Homepage' -> Query
endpoint_url = "https://dis18project.wikibase.cloud/query/sparql"

# SPARQL query to get back all information for items in the instance
sparql_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <https://dis18project.wikibase.cloud/prop/direct/>

SELECT DISTINCT ?item ?itemLabel ?locusTag ?length ?strandForward ?strandReverse ?condition ?startPosition WHERE {
  ?item wdt:P6 ?locusTag .
  OPTIONAL { ?item wdt:P7 ?length . }
  OPTIONAL { ?item wdt:P8 ?strandForward . }
  OPTIONAL { ?item wdt:P9 ?strandReverse . }
  OPTIONAL { ?item wdt:P10 ?condition . }
  OPTIONAL { ?item wdt:P11 ?strandReverse . }
  OPTIONAL { ?item wdt:P12 ?startPosition . }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""


def query(endpoint_url, sparql_query):
    try:
        headers = {"Accept": "application/sparql-results+json"}
        # HTTP GET request to SPARQL endpoint with the query as parameter
        response = requests.get(
            endpoint_url, params={"query": sparql_query}, headers=headers
        )
        # Check if request was successful
        if response.status_code == 200:
            results = response.json()
            return results
        else:
            print(f"Error: SPARQL query failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")


ex = Namespace("http://example.org/")
g = Graph()

locus_tag_property = URIRef("http://example.org/hasLocusTag")
length_property = URIRef("http://example.org/hasLength")
strand_forward_property = URIRef("http://example.org/hasStrandForward")
strand_reverse_property = URIRef("http://example.org/hasStrandReverse")
condition_property = URIRef("http://example.org/hasCondition")
start_position_property = URIRef("http://example.org/hasStartPosition")

if __name__ == "__main__":
    results = query(endpoint_url, sparql_query)
    if results:
        for result in results["results"]["bindings"]:
            item = result["item"]["value"] if "item" in result else None
            item_label = result["itemLabel"]["value"] if "itemLabel" in result else None
            locus_tag = result["locusTag"]["value"] if "locusTag" in result else None
            length = result["length"]["value"] if "length" in result else None
            strand_forward = (
                result["strandForward"]["value"] if "strandForward" in result else None
            )
            strand_reverse = (
                result["strandReverse"]["value"] if "strandReverse" in result else None
            )
            condition = result["condition"]["value"] if "condition" in result else None
            start_position = (
                result["startPosition"]["value"] if "startPosition" in result else None
            )

            item_uri = URIRef(item)
            g.add((item_uri, RDFS.label, Literal(item_label)))
            g.add((item_uri, locus_tag_property, Literal(locus_tag)))
            if length:
                g.add((item_uri, length_property, Literal(length)))
            if strand_forward:
                g.add((item_uri, strand_forward_property, Literal(strand_forward)))
            if strand_reverse:
                g.add((item_uri, strand_reverse_property, Literal(strand_reverse)))
            if condition:
                g.add((item_uri, condition_property, Literal(condition)))
            if start_position:
                g.add((item_uri, start_position_property, Literal(start_position)))

        # Turtle format is needed for simple display script
        serialized_graph = g.serialize(format="turtle")
        print(serialized_graph)
        with open("knowledge_graph.ttl", "w") as f:
            f.write(serialized_graph)
    else:
        print("No results returned.")
