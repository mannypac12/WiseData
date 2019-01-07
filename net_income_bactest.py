import pandas as pd
import numpy as np
from FileOpener.CSVReader.CSVReader import CSVReader as csv
## Price Data

prc_dir = 'CSVFile/Price/Korea/Stocks'
fin_dir = 'CSVFile/FinancialData/Korea'

price_data = csv.price_reader(filename = 'KOSPI_FROM_1998_close.csv', directory = prc_dir)
fin_data = csv.financial_reader(filename = 'NET_INCOME_KSE.csv', directory = fin_dir)



