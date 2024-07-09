import requests

# Wikibase Cloud SPARQL endpoint URL -> from 'Homepage' -> Query
endpoint_url = "https://dis18project.wikibase.cloud/query/sparql"

# SPARQL query to get back the qids with the labels, Limit can be changed as needed
sparql_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?qid ?label
WHERE {
  ?item ?p ?o .
  FILTER(regex(str(?item), "^https://dis18project.wikibase.cloud/entity/Q"))
  OPTIONAL { ?item rdfs:label ?label }
  BIND(REPLACE(STR(?item), "^.*Q", "Q") AS ?qid)
}
LIMIT 10
"""

def query(endpoint_url, sparql_query):
    try:
        # Define HTTP headers
        headers = {
            "Accept": "application/sparql-results+json"
        }
        
        # Make HTTP GET request to SPARQL endpoint with the query as parameter
        response = requests.get(endpoint_url, params={"query": sparql_query}, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            results = response.json()
            return results
        else:
            print(f"Error: SPARQL query failed with status code {response.status_code}")
    
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")

# Main execution
if __name__ == "__main__":
    # Execute the SPARQL query
    results = query(endpoint_url, sparql_query)
    
    if results:
        # Process the results
        for result in results["results"]["bindings"]:
            qid = result["qid"]["value"] if "qid" in result else None
            label = result["label"]["value"] if "label" in result else None
            print(f"QID: {qid}, Label: {label}")
    else:
        print("No results returned.")
