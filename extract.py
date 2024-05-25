import pandas as pd
from rdflib import URIRef, BNode, Literal, Namespace, Graph, PROV

"""
Pos: The position of the TSS in the genome.											
Strand: The strand of the TSS in the genome.											
detCount: The number of genomes in which this TSS was detected in the RNAseq data.											
Condition: The biological condition to which the rest of the line relates.											
detected: Contains a '1' if the TSS was detected in this condition.											
enriched: Contains a '1' if the TSS is enriched in this condition.											
stepHeight: The expression height change at the position of the TSS. This relates to the number of reads starting at this position.											
stepFactor: The factor of height change at the position of the TSS.											
enrichmentFactor: The enrichment factor at the position of the TSS.											
classCount: The number of classes to which this TSS was assigned.											
Locus_tag: The locus tag of the gene to which the classification relates.											
Product: The product description of this gene.											
UTRlength: The length of the untranslated region between the TSS and the respective gene (nt). (Only applies to 'primary' and 'secondary' TSS.)											
GeneLength: The length of the gene (nt).											
Primary: Contains a '1' if the TSS was classified as 'primary' with respect to the gene stated in 'locusTag'.											
Secondary: Contains a '1' if the TSS was classified as 'secondary' with respect to the gene stated in 'locusTag'.											
Internal: Contains a '1' if the TSS was classified as 'internal' with respect to the gene stated in 'locusTag'.											
Antisense: Contains a '1' if the TSS was classified as 'antisense' with respect to the gene stated in 'locusTag'.											
Automated: Contains a '1' if the TSS was detected automatically.											
Manual: Contains a '1' if the TSS was annotated manually.											
Putative sRNA: Contains a '1' if the TSS might be related to a novel sRNA.											
Putative asRNA: Contains a '1' if the TSS might be related to an asRNA.											
Sequence −50 nt upstream + TSS (51nt): Contains the base of the TSS and the 50 nucleotides upstream of the TSS.											
Overlap with RegulonDB: Contains an X for all primary and secondary TSS that match a RegulonDB TSS classified as primary or secondary (according to our scheme) with a maximum distance of three nucleotides.
"""

# df = pd.read_excel('data/zjb999093409sd1.xlsx', sheet_name= 'TSS Map MasterTable', header=2, engine = 'openpyxl')

# print(df)


"""
<transcription start site> <has position> <38>
<transcription start site> <has locus tag> <b0001> 
"""


"""
URIS

transcription start site = https://www.wikidata.org/wiki/Q2449354
locus tag = https://www.wikidata.org/wiki/Q106227

"""

# transcription_start_site = URIRef('http://www.wikidata.org/entity/Q12418')
# position = Literal(38)

# Define RDF namespaces
nasp = Namespace("http://example.org/")
nasp_gene = Namespace("http://example.org/gene/")
nasp_length = Namespace("http://example.org/length/")
nasp_start = Namespace("http://example.org/start/")
nasp_end = Namespace("http://example.org/end/")

# Create an RDF graph
g = Graph()

# Add triples for DNA length, start point, end point, and locus tag
dna_length = nasp_length['dna_length']
start_point = nasp_start['start_point']
end_point = nasp_end['end_point']
locus_tag = nasp_gene['locus_tag']

g.add((dna_length, nasp['hasValue'], Literal(1000)))  # Example length
g.add((start_point, nasp['hasValue'], Literal(1)))    # Example start point
g.add((end_point, nasp['hasValue'], Literal(500)))    # Example end point
g.add((locus_tag, nasp['hasValue'], Literal("Gene123")))  # Example locus tag

# Serialize the RDF graph
serialized_rdf = g.serialize(format='turtle')

# Print the serialized RDF
print(serialized_rdf)
