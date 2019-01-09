import pandas as pd
from FileOpener.CSVReader.CSVReader import CSVReader as csv

directory = 'CSVFile/FinancialData/Korea'
filename = 'DIV_OR_NOT_KSE.csv'

# test = pd.read_csv(f"{directory}/{filename}", skiprows = 1)

print(csv.financial_reader(filename, directory))