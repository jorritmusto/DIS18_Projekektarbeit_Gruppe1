import pandas as pd
import luigi
from create_initial_items import CreateInitialItemsTask


class CreateItemsGenesTask(luigi.Task):
    
    
    def requires(self):
        return CreateInitialItemsTask()
    

    def output(self):
        return luigi.LocalTarget("data/test.txt")
    

    def run(self):

        # read in excel sheet 
        df = pd.read_excel("data/input_files/zjb999093409sd1.xlsx", sheet_name = "TSS Map MasterTable", header = 2, engine = 'openpyxl')
        #print(df)



        # relevant columns for gene dataframe 
        df_genes = df[["Locus_tag", "Product", "GeneLength"]]



        # group by to delete duplicates
        df_genes = df_genes.groupby(["Locus_tag", "Product", "GeneLength"]).head(1).reset_index(drop = True)

        # adds column qid. qid is created automatically by wikibase
        df_genes["qid"] = None


        df_genes = df_genes[["qid", "Locus_tag", "Product", "GeneLength"]]


        # creates statement: <b0001> (thr operon leader peptide) <has length> <66>
        df_genes = df_genes.rename(columns = {"Locus_tag": "Len", "Product": "Den", "GeneLength": "P3"})


        # adds quotes to the gene lengths  
        df_genes["P3"] = df_genes["P3"].apply(lambda x: '"' + str(int(x))+ '"')


        #adds <is instance of> <gene>
        df_genes["P4"] = "Q26"


        df_genes.to_csv("data/quick_statements/qs_genes.csv", sep = ",", index = False)



        with self.output().open("w") as output_file:
            output_file.write("Done...")



if __name__ == '__main__':
     luigi.build([CreateItemsGenesTask()], workers=5, local_scheduler=True)