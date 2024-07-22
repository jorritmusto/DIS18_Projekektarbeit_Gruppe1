import requests
import pandas as pd
import json


def get_qids():

    """
        This function returns a daframe with all qids and labels of our wibase cloud instance
    """

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
    """
    qid = []
    label = []
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
            for result in results["results"]["bindings"]:
                qid.append(result["qid"]["value"]) if "qid" in result else None
                label.append(result["label"]["value"]) if "label" in result else None
                df = pd.DataFrame(
                    {'QID': qid,
                     'label': label,
                    })
                if df.empty:
                    print("No qids yet")

                df.to_csv("data/overview_qids.csv", sep =";", index = False)
            

            return df
        else:
            print(f"Error: SPARQL query failed with status code {response.status_code}")

    except Exception as e:
        print(f"Error executing SPARQL query: {e}")



def get_special_item_qid(label,df):
    """
        This function returns the qid for a given label of an item
    """
    for idx, elem in enumerate(df['label']):
        if str(elem) == label:
            qid = df['QID'][idx]
        else:
            print(("There is no qid yet for label: {}").format(label))
    return qid