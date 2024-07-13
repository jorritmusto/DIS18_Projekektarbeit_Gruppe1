import pandas as pd 
import sys
from itertools import count

from sparql_ import * 

import requests
import json

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

# counter is used to produce the QIDs 
# counter = count(5)


def qid_generator(df):
    df["qid"] = None
    df["qid"] = df["qid"].apply(lambda x: "Q" + str(next(counter)))
    return df



#############################################################################################################################
################################################# PREREQUESITES #############################################################
#############################################################################################################################


# the following properties have to be created beforehand in the Wikibase Instance
# 1. P1: has length 




#############################################################################################################################
################################################# Preperation ###############################################################
#############################################################################################################################

# read in excel sheet 
df = pd.read_excel("data/zjb999093409sd1.xlsx", sheet_name = "TSS Map MasterTable", header = 2, engine = 'openpyxl')
#print(df)



# relevant columns for gene dataframe 
df_genes = df[["Locus_tag", "Product", "GeneLength"]]


# relevant columns for TSS dataframe 
df_tss = df[["Pos", "Strand", "detected", "Locus_tag"]]




#############################################################################################################################
################################################# Creation TSS ITEM #########################################################
#############################################################################################################################


df_tss_item = pd.DataFrame({'qid': [""], 'Len': ["TSS"], 'Aen': ["Transcription Start Site"], 'Den': ["This is the description what is meant by TSS"]})

#df_tss_item = qid_generator(df_tss_item)

#df_tss_item["qid"][0]

#tss_item = df_tss_item["qid"][0]

df_tss_item.to_csv("data/quick_statements/tss_item.csv", sep = ",", index = False)


#sys.exit()

#############################################################################################################################
################################################# Preperation GENES #########################################################
#############################################################################################################################


# group by to delete duplicates
df_genes = df_genes.groupby(["Locus_tag", "Product", "GeneLength"]).head(1).reset_index(drop = True)


# assign QID to the genes 
#df_genes = qid_generator(df_genes)

#UPDATE: the QID can not be created by us they are created automatically when uploading 

df_genes["qid"] = None


df_genes = df_genes[["qid", "Locus_tag", "Product", "GeneLength"]]


# creates statement: <b0001> (thr operon leader peptide) <has length> <66>
df_genes = df_genes.rename(columns = {"Locus_tag": "Len", "Product": "Den", "GeneLength": "P3"})

df_genes["P3"] = df_genes["P3"].apply(lambda x: '"' + str(int(x))+ '"')


df_genes.to_csv("data/quick_statements/qs_genes.csv", sep = ",", index = False)


#############################################################################################################################
################################################# Preperation TSS ###########################################################
#############################################################################################################################


# 1. Quickstatement: <name of TSS (pos + strand)> (description) <is instance of> <TSS (QID)> <has position> <is on strand> <relates to> <q10 (b001)>

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



results = query(endpoint_url, sparql_query)

qid = []
label = []


for result in results["results"]["bindings"]:
    qid.append(result["qid"]["value"]) if "qid" in result else None
    label.append(result["label"]["value"]) if "label" in result else None


df = pd.DataFrame(
    {'QID': qid,
     'Len': label,
    })

df["Len"] = df["Len"].apply(lambda x: str(x).replace("b001", "b0001"))



# merge dataframe to get the qid of the genes 
df_tss = df_genes.merge(df, how = "left", on = "Len")

print(df)

print(df_genes)


print(df_tss)

#df_tss = df_tss[["Pos", "Strand", "detected", "Len"]]


sys.exit()
















"""
    - In this section the TSS are modeled: The name of the TSS are assembled by its position + "_" + strand
    - a qid is created automaticaaly for each TSS  
    - moreover there will be statements about the position and strand the TSS is located 
    - another statement will point out under which condition the TSS was detected 
    - Also the information in which gene the TSS was detected is given 

    Example: <34_+> <has position 34> <is on strand +> <relates to Q1> <detected under condition LB_2.0>
"""

# qid is set automatically when uploading csv file 
df["qid"] = None


#Len -> Label of the Item in english based on the position and strand of TSS 
df["Len"] = df["Pos"].astype(str) + "_" + df["Strand"].astype(str)


# Den -> Description in english has to be adjusted (has to be more precise probably)
df["Den"] = "TSS"


# drop all rows where TSS was not detected under one of the three conditions 
df = df[df.detected != 0]


# rename columns with our property IDs: P1 = has position, P2 = is on Strand, P3 = relates to, P4 = detected under condition 
df = df.rename(columns = {"Pos": "P1", "Strand": "P2", "Condition": "P4"})



df = df[["qid", "Len", "Den", "P1", "P2", "P3", "P4"]]

#df.to_csv("data/quick_statements_TSS.csv", sep = ",", index = False)




"""
    - In this section the genes are modeled: The name of the gene is the locu_tag 
    - a qid is created by this script. Later the quick statments of the TSS refers to this genes
    - there will be statements about the locus_tag and the length of this gene 
"""


# remove duplicates 
df_genes = df_genes[["Locus_tag", "Product", "GeneLength"]]

df_genes = df_genes.groupby(["Locus_tag", "Product", "GeneLength"]).head(1).reset_index(drop = True)



# assign QID to the genes 
df_genes["qid"] = None

df_genes["qid"] = df_genes.index +1

df_genes["qid"] = df_genes["qid"].apply(lambda x: "Q" + str(x))



# create items ( P5 = has locus_tag, P6 = has length)
df_genes = df_genes.rename(columns = {"Product": "Den", "GeneLength": "P6", "Locus_tag": "P5"})




