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
mapping_df = pd.read_csv('mapping_table.csv', sep = ";")

df_list = []

for index, row in mapping_df.iterrows():
    file_name = row["name of excel file"]
    sheet_name = row["name of sheet"]
    header = int(row["header in row number"])

    # read in excel file 
    df = pd.read_excel("data/" + file_name, sheet_name = sheet_name, header = header, engine = 'openpyxl')

    # unify column names 
    df.rename(columns={row["TSS position called"]: 'position_of_tss', 
                       row["locus tag called"]: 'locus_tag', 
                       row["strand called"]: 'strand', 
                       row["product description of gene called"]: 'product', 
                       row["systematic id called"]: 'systematic_id', 
                       row["gene name called"]: 'gene_name',
                       row["start called"]: 'location_of_start',
                       row["end called"]: 'location_of_end',
                       row["PubMed ID called"]: 'pubmed_id',
                       row["SL1344 identifier called"]: 'sl1344_id',
                       row["length called"]: 'length'
                       },inplace=True)

    
    # add not exisiting columns to dataframe and fill with None 
    headers = ['position_of_tss',
               'locus_tag', 
               'strand', 
               'product', 
               'systematic_id', 
               'gene_name', 
               'location_of_start', 
               'location_of_end', 
               'pubmed_id',
               'sl1344_id',
               'length']
    
    for header in headers:
        if not header in df.columns:
            df[header] = None


    # remove unnecessary columns 
    df = df[['position_of_tss', 
             'locus_tag',
                'strand', 
               'product', 
               'systematic_id', 
               'gene_name', 
               'location_of_start', 
               'location_of_end', 
               'pubmed_id',
               'sl1344_id',
               'length']]
    

    # Werte in column "Strand" müssen noch vereinheitlich werden 
    


    
    #concatinate dfs 
    df_list.append(df)

    df = pd.concat(df_list)
    

print(df)


"""
<transcription start site> <has position> <38>
<transcription start site> <has locus tag> <b0001> 
"""


"""
URIS

transcription start site = https://www.wikidata.org/wiki/Q2449354
locus tag = https://www.wikidata.org/wiki/Q106227

"""

#transcription_start_site = URIRef('http://www.wikidata.org/entity/Q12418')
#position = Literal(38)

#g = Graph()

#g.bind("test", PROV)

#g.add(transcription_start_site, PROV.atlocation, position)

