import pandas as pd

def excel(input_excel_path, columns_to_delete, output_csv_path):
    df = pd.read_excel(input_excel_path)
    df.drop(columns=columns_to_delete, inplace=True, errors='ignore')
    df.to_csv(output_csv_path, index=False)

def parse_to_quickstatements(csv_path, quickstatements_path):
    df = pd.read_csv(csv_path)
    
    quickstatements = []
    for index, row in df.iterrows():
        pos = row.get('Pos', '')
        strand = row.get('Strand', '')
        condition = row.get('Condition', '')
        locus_tag = row.get('Locus_tag', '')
        gene_length = row.get('GeneLength', '')

        strand_info = 'forward' if strand == '+' else 'reverse' if strand == '-' else 'unknown'
        item_name = f"TSS_{pos}_{strand_info}"

        if pos:
            quickstatements.append(f"CREATE")
            quickstatements.append(f"LAST|Len|\"{item_name}\"")
            quickstatements.append(f"LAST|P2|\"{pos}\"")
        if strand:
            if strand == '+':
                quickstatements.append(f"LAST|P8|\"{strand}\"")
            elif strand == '-':
                quickstatements.append(f"LAST|P11|\"{strand}\"")
        if locus_tag:
            quickstatements.append(f"LAST|P6|\"{locus_tag}\"")
        if gene_length:
            quickstatements.append(f"LAST|P7|\"{gene_length}\"")
        if condition:
            quickstatements.append(f"LAST|P10|\"{condition}\"")

    with open(quickstatements_path, 'w') as file:
        for statement in quickstatements:
            file.write(f"{statement}\n")

if __name__ == "__main__":
    input_excel_path = '/Users/viktoriahellmann/dev/DIS18_Projekektarbeit_Gruppe1/data/zjb999093409sd11.xlsx'
    columns_to_delete = ['Primary', 'Secondary']
    output_csv_path = '/Users/viktoriahellmann/dev/DIS18_Projekektarbeit_Gruppe1/data/csv/output_csv_file.csv'
    quickstatements_path = '/Users/viktoriahellmann/dev/DIS18_Projekektarbeit_Gruppe1/data/quickstatements.txt'

    excel(input_excel_path, columns_to_delete, output_csv_path)
    parse_to_quickstatements(output_csv_path, quickstatements_path)
