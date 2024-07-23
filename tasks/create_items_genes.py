import pandas as pd
import luigi
from create_initial_items import CreateInitialItemsTask
from get_qid import *

class CreateItemsGenesTask(luigi.Task):
    
    
    def requires(self):
        return CreateInitialItemsTask()
    

    def output(self):
        return luigi.LocalTarget(("data/{}.txt").format(__class__.__name__))
    

    def run(self):

        # read in excel sheet 
        df = pd.read_excel("data/input_files/zjb999093409sd1.xlsx", sheet_name = "TSS Map MasterTable", header = 2, engine = 'openpyxl')


        # relevant columns for gene dataframe 
        df_genes = df[["Locus_tag", "Product", "GeneLength"]]


        # group by to delete duplicates
        df_genes = df_genes.groupby(["Locus_tag", "Product", "GeneLength"]).head(1).reset_index(drop = True)

        # adds column qid. qid is created automatically by wikibase
        df_genes["qid"] = None

        # only keep important colmns
        df_genes = df_genes[["qid", "Locus_tag", "Product", "GeneLength"]]


        # creates statement: <b0001> (thr operon leader peptide) <has length> <66>
        df_genes = df_genes.rename(columns = {"Locus_tag": "Len", "Product": "Den", "GeneLength": "P7"})


        # adds quotes to the gene lengths  
        df_genes["P7"] = df_genes["P7"].apply(lambda x: '"' + str(int(x))+ '"')


        #adds <is instance of> <gene>
        df_qids = get_qids()

        gene = "Gene"

        # get qid of item Gene
        try: 
            qid = get_special_item_qid(label=gene,df= df_qids)
        except Exception as e:
            print("Please create item 'Gene' first within the inital statment task")


        #adds <is instance of> <gene>
        df_genes["P13"] = qid

        # write quickstatements as csv
        df_genes.to_csv("data/quick_statements/genes/qs_genes.csv", sep = ",", index = False)



        with self.output().open("w") as output_file:
            output_file.write("Done...")





#if __name__ == '__main__':
#     luigi.build([CreateItemsGenesTask()], workers=1, local_scheduler=True)