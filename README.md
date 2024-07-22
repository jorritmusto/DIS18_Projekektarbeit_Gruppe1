[ToDos: 
Git-Repo:

öffentliches Repo auf GitHub mit folgendem Inhalt:
- Ziel und grundlegende Vorgehensweise (Concept Map/ Dokumentation)
- Installationsanleitung inkl. Abhängigkeiten (setup.py, requirements.txt, etc) bei Nutzung von Docker Container auch Dockerfiles
Workflows, Datenfluss
- ggf. Code-Beispiele (Ausschnitt)
- OSI-kompatible OpenSource-Lizenz (BSD, MIT, ISC, GPL)
zusätzlich sinnvoll:
- Ablage eines Snapshots auf Zenodo
- Code mit black formattieren
- Dokumentation mit Dokumentationssystem wie mkdoks oder spinx erstellen und als GitHub-Page hosten
- Das Python Project Template für Cookiecutter nutzen]

# DIS18_Projekektarbeit_Gruppe1

## Project Goal

The goal of this project is to build a wikibase cloud instance containing data generated from sequencing. We aimed to transform TSS data into a knowledge graph. The project is build according to the FAIR principles.

Objectives
- Data Extraction: Extract data from sequencing outputs, specifically focusing on Transcriptional Start Sites (TSS).
- Data Transformation: Convert the extracted data into RDF (Resource Description Framework) format suitable for a knowledge graph.
- Knowledge Graph Creation: Populate a knowledge graph using the transformed data, utilizing either a custom Wikibase instance or Wikidata.

The steps to do so would be: 

1. Create an Instance
2. Define & create properties in Wikibase Cloud Instance
3. Import Data: prepare data & create a CSV for bulk uploads using QickStatements in Wikibase Cloud Instance
4. Query the data using SPARQL
5. Use this data to create a Knowledge Graph (preferably using Python)
6. Use a tool like Neo4j to visualize these graphs

## What is TSS data? 

A transcription start site (TSS) is the location where the first DNA nucleotide is transcribed into RNA. It is difficult to determine the exact position of the TSS using bioinformatics, but experimental methods can be used to locate it, notably high throughput sequencing. (France Génomique. 2024. Online available: https://www.france-genomique.org/technological-expertises/regulome/mapping-of-transcription-start-sites-tss/?lang=en)

Our data contains the following information on TSS: 

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


## What's in this repository

[WIP] In this project, data generated from sequencing data will be transferred to a knowledge graph. For this we use an Wikibase cloud instance. The instance can be reached with the following link: https://dis18project.wikibase.cloud
Besides this, you'll fine some data to (semi-)automatically fill this instance. Additionally, you'll find some TSS data (SOURCE) thats used for the example usage section. 

In the Wikibase Cloud Instance, you'll find the following properties: 

1. has locus tag (P6) [String]
2. has length - (P7) [String]
3. has strand (forward) - (P8) [String]
4. has strand (reverse) - (P9) [String]
5. has condition (P10) [String]
6. has strand reverse - (P11) [String]
7. has start position - (P12) [String]

The other properties are deprecated.


## Setup

First, you need to clone this repository to your local dev environment. To do so, use git clone and the options given by github. After that, you can access these files in the following order: 

- XXX: to convert the excel file to a XXX file. 
- YYY: 
- ZZZ: 
- sparql_statement.py: to get back every QUID + Label from the items in the Wikibase Cloud. 

## Example Usage 

1. xxx
2. yyy
3. zzz

## Learnings

To build this instance we gathered some learnings we want to display in this section. 
At first, we weren't sure on how to get data as statements into the Cloud Instance. At first, we tried using pandas for reading the excel file and rdflib to create a knowledge graph. The excel file were split manually into an edges and a nodes section and code looked like this: 

```python
  excel_nodes = pd.read_excel('data/nodes_zjb999093409sd1.xlsx')
  excel_edges = pd.read_excel('data/edges_zjb999093409sd1.xlsx')
  g.serialize(destination='output_graph.ttl', format='turtle')
```

This attempt didn't work because we had a false understanding on what knowledge graphs would be. We had several attempts on this. 

After giving up on this, we tried creating statements in our cloud instance manually, which worked good. At first, we started to set up some properties and items. With these we wanted to form statements. Here we learnt that it's essential to use the right data type in the properties. 
From there we tried using Quick Statements. Here we learnt that they need to have a specific syntax to work, a csv file worked best for us. (Guidance on this can be found here: https://www.wikidata.org/wiki/Help:QuickStatements)

