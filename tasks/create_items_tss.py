import luigi
import pandas as pd
from get_qid import get_qids, get_special_item_qid
import sys
from create_items_genes import CreateItemsGenesTask


class CreateItemsTssTask(luigi.Task):
    
    
    def requires(self):
        return CreateItemsGenesTask()
    

    def output(self):
        return luigi.LocalTarget("data/hello.txt")
    

    def run(self):


        df_qids = get_qids()

        df_tss = pd.read_excel("data/input_files/zjb999093409sd1.xlsx", sheet_name = "TSS Map MasterTable", header = 2, engine = 'openpyxl')

        # qid is set automatically when uploading csv file 
        df_tss["qid"] = None


        #Len -> Label of the Item in english based on the position and strand of TSS 
        df_tss["Len"] = df_tss["Pos"].astype(str) + "_" + df_tss["Strand"].astype(str)


        # Den -> Description in english has to be adjusted (has to be more precise probably)
        df_tss["Den"] = "TSS"


        # drop all rows where TSS was not detected under one of the three conditions 
        df_tss = df_tss[df_tss.detected != 0]


        # rename columns with our property IDs: P1 = has position, P2 = is on Strand, P3 = relates to, P5 = detected under condition 
        df_tss = df_tss.rename(columns = {"Pos": "P1", "Strand": "P2", "Condition": "P5"})

        #get qid of TSS 
        tss = "TSS"

        qid = get_special_item_qid(label=tss,df= df_qids)


        #add "P4" = "is instance of" to the dataframe 
        df_tss["P4"] = qid

        df_tss = df_tss[["qid", "Len", "Den", "P1", "P2", "P4", "P5", "Locus_tag"]]

        #helper has to be removed later 
        df_qids["label"] = df_qids["label"].apply(lambda x: str(x).replace("b001", "b0001"))

        df_tss = df_tss.merge(df_qids, how = "left", left_on= "Locus_tag", right_on = "label")

        df_tss = df_tss.rename(columns = {"QID": "P3"})

        df_tss = df_tss[["qid", "Len", "Den", "P1", "P2", "P3", "P4", "P5"]]

        df_tss.to_csv("data/quick_statements/qs_tss.csv", sep = ";", )

        with self.output().open("w") as output_file:
            output_file.write("Done...")


        

if __name__ == '__main__':
     luigi.build([CreateItemsTssTask()], workers=1, local_scheduler=True)