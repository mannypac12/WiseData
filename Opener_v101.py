import pandas as pd
import numpy as np
from datetime import datetime

## When Initialize Quantiwise Excel 
## Settlement Should be unchecked

class DataOpener:

    zerotonan = lambda x: np.nan if x == 0 else x

    def __init__(self, file, dir='Data'):
        
        self.dir = dir
        self.fullpath=f"{self.dir}\\{file}"

class TimeSeriesOpener(DataOpener):

    def dataCols(self, sheetname):

        return pd.read_excel(self.fullpath, sheet_name=sheetname, skiprows=7, nrows=1).columns[1:]

    def TS_dataopener(self, sheetname, idx_name='D A T E', skipr=13):

        dt = pd.read_excel(self.fullpath,sheet_name=sheetname, skiprows=skipr).set_index('D A T E')
        dt.columns = self.dataCols(sheetname)

        return dt

class CrossSectionOpen(DataOpener):

    def dataCols(self, sheetname, sk_rows=9):
        
        cols = ['Code'] + list(pd.read_excel(self.fullpath, sheet_name=sheetname, skiprows=sk_rows, nrows=1).columns[2:])
        
        return cols

    def TS_dataopener(self, sheetname, col_sk_rows, skipr=12):

        dt = pd.read_excel(self.fullpath,sheet_name=sheetname,skiprows=skipr).drop('Name', axis=1)
        dt.columns = self.dataCols(sheetname, sk_rows=col_sk_rows)

        return dt

class PriceDataOpener(TimeSeriesOpener):

    def olhc(self, sheetnames=["수정시가", "수정고가", "수정주가", "수정저가"]):            
            ## 0 to NaN

        prices = {}

        for sheet_nm in sheetnames:
            prices[sheet_nm] = (self.TS_dataopener(sheet_nm)).applymap(DataOpener.zerotonan).dropna(axis=0, how='all')

        return prices['수정시가'], prices['수정고가'], prices['수정주가'], prices['수정저가']

class MarketCapOpener(TimeSeriesOpener):

    @staticmethod
    def marketcap(x):
    
        if x == np.NaN:
            return 0
        else:
            if x <= 100:
                return 1
            elif (x > 100) & (x < 301):
                return 2
            elif x > 301: 
                return 3

    def mkc_opener(self, sheetnames=['KSE', 'KDQ']):

        data = {}

        for sheet_nm in sheetnames:
            data[sheet_nm] = (self.TS_dataopener(sheet_nm)).applymap(DataOpener.zerotonan).dropna(axis=0, how='all')

        return data

class FinancialDataOpener(CrossSectionOpen):

    def fin_data_open(self, sheetnames=['KSE', 'KDQ']):

        data = {}

        for sheet_nm in sheetnames:
            data[sheet_nm] = ((self.TS_dataopener(sheet_nm, col_sk_rows=9)).applymap(DataOpener.zerotonan).dropna(axis=0, how='all')).T

        return data

class StockInfoDataOpener(CrossSectionOpen):

    def info_data_open(self, sheetnames=['KSE', 'KDQ'], col_sk_rows=9):

        data = {}

        for sheet_nm in sheetnames:
            data[sheet_nm] = ((self.TS_dataopener(sheet_nm, col_sk_rows=col_sk_rows))
                                   .applymap(DataOpener.zerotonan)
                                   .dropna(axis=0, how='all')).set_index('Code')

        return data
     

# print(PriceDataOpener('price.xlsm').olhc())

