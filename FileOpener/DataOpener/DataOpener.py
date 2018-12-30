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

    zerotonan = lambda x: np.nan if x == 0 else x

    def opener(self, sheetnames=['KSE', 'KDQ'], idx_name='Code',skipr=12):

        file = {}
        
        for sheet_nm in sheetnames:
            file[sheet_nm] = (self.TS_dataopener(sheet_nm, idx_name, skipr)).applymap(StockInfoDataOpener.zerotonan).dropna(axis=0, how='any')

        return file

    def sect_to_csv(self, folder_name='Sector', **kwargs):

        file = self.opener(**kwargs)

        for key in file.keys():
            file[key].to_csv(f'{self.dir}\{folder_name}\{key}.csv')

    def delist_to_csv(self, folder_name='Delist', **kwargs):

        file = self.opener(**kwargs)

        for key in file.keys():
            file[key]['상장폐지일']= pd.to_datetime(file[key]['상장폐지일'].astype(int).astype(str))
            file[key].to_csv(f'{self.dir}\{folder_name}\{key}.csv')



        
    ## OpenFile

        ## Sector 

        ## Delisted

        ##
    
    # def Sect_Opener(self, sheetnames=['KSE', 'KDQ'], idx_name='Code', folder_name='Sector',skipr=12):
        
    #     for sheet_nm in sheetnames:
    #         ((self.TS_dataopener(sheet_nm, idx_name, skipr)).applymap(StockInfoDataOpener.zerotonan).dropna(axis=0, how='any')).to_csv(f'{self.dir}\{folder_name}\{sheet_nm}.csv')
    #         print(f"{sheet_nm}.csv saved in {folder_name}")


