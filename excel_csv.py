import pandas as pd

def excel(input_excel_path, columns_to_delete, output_csv_path):
    df = pd.read_excel(input_excel_path)
    df.drop(columns=columns_to_delete, inplace=True, errors='ignore')
    df.to_csv(output_csv_path, index=False)

# Example usage
if __name__ == "__main__":
    input_excel_path = '/Users/viktoriahellmann/dev/DIS18_Projekektarbeit_Gruppe1/data/zjb999093409sd11.xlsx'
    columns_to_delete = ['Primary', 'Secondary']
    output_csv_path = '/Users/viktoriahellmann/dev/DIS18_Projekektarbeit_Gruppe1/data/csv/output_csv_file.csv'

    excel(input_excel_path, columns_to_delete, output_csv_path)
