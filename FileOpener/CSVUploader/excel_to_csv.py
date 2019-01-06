from FileOpener.DataOpener.DataOpener import PriceDataOpener, FinancialDataOpener, StockInfoDataOpener
from Fileset import fileset

## All file to csv
## Upload the file then append it to csv



PriceDataOpener(dir='../../Data', file='price.xlsm').olhc()

