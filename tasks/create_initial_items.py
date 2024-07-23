import pandas as pd
import os
from get_qid import get_qids, get_special_item_qid
import luigi
import logging


class CreateInitialItemsTask(luigi.Task):
    

    def output(self):
        return luigi.LocalTarget(("data/{}.txt").format(__class__.__name__))
    

    def run(self):

        #directory in which the initial statements should be stored
        folder = "data/quick_statements/initial_items/"

        # create folder for inital statements
        if not os.path.isdir(folder):
            os.mkdir(folder)


        # get qids of already existing items
        df = get_qids()



        ###############################################################################
        #################### Create initial item TSS ##################################
        ###############################################################################

        #label of the item
        len_tss = "Transcription Start Site"

        # alias of the item
        aen_tss = "TSS"

        # description of the item 
        den_tss = "Transcription start sites (TSS) is the location where the first DNA nucleotide is transcribed into RNA."

        # check if the item already exists -> if not: create the statements
        if not df['label'].str.contains(len_tss).any():
        
            df_tss_item = self.create_statments_df(Len = len_tss, Aen = aen_tss, Den = den_tss)
            df_tss_item.to_csv(folder + "item_tss.csv", sep = ",", index = False)

        # if item already exists -> write a message that the item already exists + qid      
        else:
            qid = get_special_item_qid(len_tss, df)
            with open('data/quick_statements/initial_items/tss.txt', "w") as output_file:
                output_file.write(("Item {} already exists with qid: {}").format(len_tss, qid))



        ###############################################################################
        #################### Create initial item Gene #################################
        ###############################################################################
        
        #label of the item
        len_gene = "Gene"

        # alias of the item if exists
        aen_gene = "DNA segment"

        # description of the item
        den_gene = "The molecular gene is a sequence of nucleotides in DNA that is transcribed to produce a functional RNA"
                
        # check if the item already exists -> if not: create the statements
        if not df['label'].str.contains(len_gene).any():
        
            df_gene_item = self.create_statments_df(Len = len_gene, Aen = aen_gene, Den = den_gene)
            df_gene_item.to_csv(folder + "item_gene.csv", sep = ",", index = False)

        # if item already exists -> write a message that the item already exists + qid      
        else:
            qid = get_special_item_qid(len_gene, df)
            with open('data/quick_statements/initial_items/gene.txt', "w") as output_file:
                output_file.write(("Item {} already exists with qid: {}").format(len_gene, qid))



        ###############################################################################
        #################### Create initial items conditions ##########################
        ###############################################################################
                
        # 1. M63_0.4
                
        #label of the item
        len_M63_04 = "M63_0.4"

        # alias of the item if exists
        aen_M63_04 = ""

        # description of the item
        den_M63_04 = "condition under which a TSS was detected"
                
        # check if the item already exists -> if not: create the statements
        if not df['label'].str.contains(len_M63_04).any():
        
            df_M63_04 = self.create_statments_df(Len = len_M63_04, Aen = aen_M63_04, Den = den_M63_04)
            print(df_M63_04)
            # drop alias column 
            df_M63_04 = df_M63_04.drop("Aen", axis='columns')
            #df_M63_04.to_csv(folder + "item_M63_04.csv", sep = ",", index = False)

        # if item already exists -> write a message that the item already exists + qid      
        else:
            qid = get_special_item_qid(len_M63_04, df)
            with open('data/quick_statements/initial_items/M63_04.txt', "w") as output_file:
                output_file.write(("Item {} already exists with qid: {}").format(len_M63_04, qid))  



        # 2. LB_0.4
                
        #label of the item
        len_LB_04 = "LB_0.4"

        # alias of the item if exists
        aen_LB_04 = ""

        # description of the item
        den_LB_04 = "condition under which a TSS was detected"
                
        # check if the item already exists -> if not: create the statements
        if not df['label'].str.contains(len_LB_04).any():
        
            df_LB_04 = self.create_statments_df(Len = len_LB_04, Aen = aen_LB_04, Den = den_LB_04)

            # drop alias column 
            df_LB_04 = df_LB_04.drop("Aen", axis='columns')
            #df_LB_04.to_csv(folder + "item_LB_04.csv", sep = ",", index = False)

        # if item already exists -> write a message that the item already exists + qid      
        else:
            qid = get_special_item_qid(len_LB_04, df)
            with open('data/quick_statements/initial_items/LB_04.txt', "w") as output_file:
                output_file.write(("Item {} already exists with qid: {}").format(len_LB_04, qid))





        # 3. LB_2.0
                
        #label of the item
        len_LB_20 = "LB_2.0"

        # alias of the item if exists
        aen_LB_20 = ""

        # description of the item
        den_LB_20 = "condition under which a TSS was detected"
                
        # check if the item already exists -> if not: create the statements
        if not df['label'].str.contains(len_LB_20).any():
        
            df_LB_20 = self.create_statments_df(Len = len_LB_20, Aen = aen_LB_20, Den = den_LB_20)

            # drop alias column 
            df_LB_20 = df_LB_20.drop("Aen", axis='columns')
            #df_LB_20.to_csv(folder + "item_LB_20.csv", sep = ",", index = False)

        # if item already exists -> write a message that the item already exists + qid      
        else:
            qid = get_special_item_qid(len_LB_20, df)
            with open('data/quick_statements/initial_items/LB_20.txt', "w") as output_file:
                output_file.write(("Item {} already exists with qid: {}").format(len_LB_20, qid))

    
        # concat condition dfs and write as csv
        df_conditions = pd.concat([df_M63_04, df_LB_04, df_LB_20])
        df_conditions.to_csv(folder + "item_condition.csv", sep = ",", index = False)


        
        with self.output().open("w") as output_file:
            output_file.write("Task Done...")




    def create_statments_df(self, Len, Aen, Den):
        """
            this function creates a dataframe, which is used to create quick statements for the initial 
            items 
        """
        df =pd.DataFrame(
            {
                "qid": [""],
                "Len": [Len],
                "Aen": [Aen],
                "Den": [Den]
            }
        )
        return df
    


#if __name__ == '__main__':
#     luigi.build([CreateInitialItemsTask()], workers=1, local_scheduler=True)