import luigi
import pandas as pd
from get_qid import get_qids, get_special_item_qid
import sys
from create_items_genes import CreateItemsGenesTask

"""
This script defines a Luigi task that processes transcription start site (TSS) data from an Excel file,
formats it for quick statements, and prepares it for uploading to a Wikibase instance.
"""


class CreateItemsTssTask(luigi.Task):
    def requires(self):
        return CreateItemsGenesTask()

    def output(self):
        return luigi.LocalTarget(("data/{}.txt").format(__class__.__name__))

    def run(self):

        df_qids = get_qids()

        df_tss = pd.read_excel(
            "data/input_files/zjb999093409sd1.xlsx",
            sheet_name="TSS Map MasterTable",
            header=2,
            engine="openpyxl",
        )

        # qid is set automatically when uploading csv file
        df_tss["qid"] = None

        # Len -> Label of the Item in english based on the position and strand of TSS
        df_tss["Len"] = df_tss["Pos"].astype(str) + "_" + df_tss["Strand"].astype(str)

        # Den -> Description in english
        df_tss[
            "Den"
        ] = "Transcription Start Site: Label was assembled by the the position and strand of the TSS"

        # drop all rows where TSS was not detected under one of the three conditions
        df_tss = df_tss[df_tss.detected != 0]

        # add "" to Pos and Strand
        df_tss["Pos"] = df_tss["Pos"].apply(lambda x: '"' + str(int(x)) + '"')
        df_tss["Strand"] = df_tss["Strand"].apply(lambda x: '"' + str(x) + '"')

        # rename columns with our property IDs: P14 = has position, P15 = is on Strand, P16 = relates to, P17 = detected under condition
        df_tss = df_tss.rename(columns={"Pos": "P14", "Strand": "P15"})

        # get qid of TSS
        tss = "Transcription Start Site"

        try:
            qid = get_special_item_qid(label=tss, df=df_qids)
        except Exception as e:
            print("Please create Item for TSS as initial items first")

        # add "P13" = "is instance of" to the dataframe
        df_tss["P13"] = qid

        df_tss = df_tss[
            ["qid", "Len", "Den", "P13", "P14", "P15", "Condition", "Locus_tag"]
        ]

        # merge with df_quids to get the qids of the genes
        df_tss = df_tss.merge(
            df_qids, how="left", left_on="Locus_tag", right_on="label"
        )

        df_tss = df_tss.rename(columns={"QID": "P16"})

        # merge wirh df_qids to get the qid of conditions
        df_tss = df_tss.merge(
            df_qids, how="left", left_on="Condition", right_on="label"
        )

        df_tss = df_tss.rename(columns={"QID": "P17"})

        df_tss = df_tss[["qid", "Len", "Den", "P13", "P14", "P15", "P16", "P17"]]

        # since an item can be detected under more than one condition there are duplicates in our dataset, which leads to conflicts when inserting
        df_tss["count"] = df_tss.groupby("Len").cumcount() + 1

        ###############################################################################
        #################### Create first batch  TSS ##################################
        ###############################################################################

        # first batch: keep rows where count == 1 +
        df_tss_first_batch = df_tss[df_tss["count"] == 1]

        # drop column "count"
        df_tss_first_batch = df_tss_first_batch.drop(columns=["count"])

        df_tss_first_batch.to_csv(
            "data/quick_statements/tss/qs_tss_first_batch.csv", sep=",", index=False
        )

        ###############################################################################
        #################### Create second batch  TSS #################################
        ###############################################################################

        df_qids = get_qids()

        # second batch: keep rows where count == 2
        df_tss_second_batch = df_tss[df_tss["count"] == 2]

        df_tss_second_batch = df_tss_second_batch[["Len", "P17"]]

        # merge wirh df_qids to get the qid before created items
        df_tss_second_batch = df_tss_second_batch.merge(
            df_qids, how="left", left_on="Len", right_on="label"
        )

        df_tss_second_batch = df_tss_second_batch.rename(columns={"QID": "qid"})

        df_tss_second_batch = df_tss_second_batch[["qid", "P17"]]

        df_tss_second_batch.to_csv(
            "data/quick_statements/tss/qs_tss_second_batch.csv", sep=",", index=False
        )

        ###############################################################################
        #################### Create third batch  TSS ##################################
        ###############################################################################

        df_qids = get_qids()

        # second batch: keep rows where count == 2
        df_tss_third_batch = df_tss[df_tss["count"] == 3]

        df_tss_third_batch = df_tss_third_batch[["Len", "P17"]]

        # merge wirh df_qids to get the qid before created items
        df_tss_third_batch = df_tss_third_batch.merge(
            df_qids, how="left", left_on="Len", right_on="label"
        )

        df_tss_third_batch = df_tss_third_batch.rename(columns={"QID": "qid"})

        df_tss_third_batch = df_tss_third_batch[["qid", "P17"]]

        df_tss_third_batch.to_csv(
            "data/quick_statements/tss/qs_tss_third_batch.csv", sep=",", index=False
        )

        with self.output().open("w") as output_file:
            output_file.write("Done...")


if __name__ == "__main__":
    luigi.build([CreateItemsTssTask()], workers=1, local_scheduler=True)
