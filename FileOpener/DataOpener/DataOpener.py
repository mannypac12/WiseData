import pandas as pd
import numpy as np

class GenDataOpener:

    def __init__(self, file, dir="Data"):
        
        self.dir = dir
        self.fullpath=f"{self.dir}\\{file}"
        
    def PF_dataCols(self):

        return pd.read_excel(self.fullpath, skiprows=8, nrows=1).columns[1:]

    def TS_dataopener(self, sheetname, idx_name='D A T E', skipr=13):

        ## For time series Data skipr: 13
        ## For cross-Sectional Data skipr: 12

        dt = pd.read_excel(self.fullpath,sheet_name=sheetname,skiprows=skipr).set_index(idx_name)
        # dt.columns = self.dataCols()

        return dt

## For Price Data / Financial Opener 
    ## columns are some stuff

## Price Data / Excel ()

class PriceDataOpener(GenDataOpener):

    def olhc(self, sheetnames=["수정시가", "수정고가", "수정주가", "수정저가"], num=1):
            
            ## 0 to NaN

            zerotonan = lambda x: np.nan if x == 0 else x

            prices = {}

            for sheet_nm in sheetnames:
                prices[sheet_nm] = (self.TS_dataopener(sheet_nm)).applymap(zerotonan).dropna(axis=0, how='all')
                prices[sheet_nm].columns = self.PF_dataCols()

            return prices['수정시가'], prices['수정고가'], prices['수정주가'], prices['수정저가'] 

class FinancialDataOpener(GenDataOpener):

    def rate_change(self, sheetname, num=1):
    
    ## If num 1 => 분기별
    ## If num 4 => 전년동기(분기)

        return super().TS_dataopener(sheetname).pct_change(num)

class StockInfoDataOpener(GenDataOpener):

    def Sect_Opener(self, sheetnames=['KSE', 'KDQ'], idx_name='Code', folder_name='Sector',skipr=12):
    
        zerotonan = lambda x: np.nan if x == 0 else x
        
        for sheet_nm in sheetnames:
            ((self.TS_dataopener(sheet_nm, idx_name, skipr)).applymap(zerotonan).dropna(axis=0, how='any')).to_csv(f'{self.dir}\{folder_name}\{sheet_nm}.csv')
            print(f"{sheet_nm}.csv saved in {folder_name}")

    

