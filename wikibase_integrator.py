from wikidataintegrator import wdi_core


query = """ SELECT ?disease ?diseaseLabel ?doid 
WHERE {
  ?disease wdt:P699 ?doid . 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} LIMIT 5
"""


wdi_core.WDFunctionsEngine.execute_sparql_query(query)