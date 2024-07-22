import pandas as pd
import os
from get_qid import get_qids
import luigi


class CreateInitialItemsTask(luigi.Task):

    folder = "data/quick_statements/initial_items/"

    Len = "TEST"

    Aen= "Transcription Start Site"

    Den = "This is the description what is meant by TSS"
    

    def output(self):
        return luigi.LocalTarget("data/test2.txt")
    

    def run(self):


        folder = "data/quick_statements/initial_items/"

        Len = "TEST"

        Aen= "Transcription Start Site"

        Den = "This is the description what is meant by TSS"



        # create folder for inital statements
        if not os.path.isdir(folder):
            os.mkdir(folder)


        df = get_qids()



        def create_statments_df(Len, Aen, Den):
            df =pd.DataFrame(
                {
                    "qid": [""],
                    "Len": [Len],
                    "Aen": [Aen],
                    "Den": [Den]
                }
            )
            return df 



        if not df['label'].str.contains(Len).any():
        
            df_tss_item = create_statments_df(Len = Len, Aen = Aen, Den = Den)
            df_tss_item.to_csv(folder + "tss_item.csv", sep = ",", index = False)

        
        with self.output().open("w") as output_file:
            output_file.write("Done...")
