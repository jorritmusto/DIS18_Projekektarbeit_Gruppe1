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

The goal of this project is to build a wikibase cloud instance containing TSS data. The project is build according to the FAIR principles.

## What is TSS data? 

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

