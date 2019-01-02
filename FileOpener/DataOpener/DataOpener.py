import pandas as pd
import numpy as np
from datetime import datetime

class GenDataOpener:

    zerotonan = lambda x: np.nan if x == 0 else x

    def __init__(self, file, dir="Data"):
        
        self.dir = dir
        self.fullpath=f"{self.dir}\\{file}"
        
    def PF_dataCols(self, sheetname, sk_rows=8):

        return pd.read_excel(self.fullpath, sheet_name=sheetname,skiprows=sk_rows, nrows=1).columns[1:]

    def TS_dataopener(self, sheetname, idx_name='D A T E', skipr=13):

        ## For time series Data skipr: 13
        ## For cross-Sectional Data skipr: 12

        dt = pd.read_excel(self.fullpath,sheet_name=sheetname,skiprows=skipr).set_index(idx_name)
        # dt.columns = self.dataCols()

        return dt

    def drop_cols_opener(self, sheetname, drop_cols, skipr=13):
        
        dt = pd.read_excel(self.fullpath, sheet_name=sheetname, skiprows=skipr).drop(drop_cols, axis=1)

        return dt

## For Price Data / Financial Opener 
    ## columns are some stuff

## Price Data / Excel ()

class PriceDataOpener(GenDataOpener):

    def olhc(self, sheetnames=["수정시가", "수정고가", "수정주가", "수정저가"]):            
            ## 0 to NaN

        prices = {}

        for sheet_nm in sheetnames:
            prices[sheet_nm] = (self.TS_dataopener(sheet_nm)).applymap(GenDataOpener.zerotonan).dropna(axis=0, how='all')
            prices[sheet_nm].columns = self.PF_dataCols(sheet_nm)

        return prices['수정시가'], prices['수정고가'], prices['수정주가'], prices['수정저가'] 

class FinancialDataOpener(GenDataOpener):

    def opener(self, sheetnames=['KSE', 'KDQ'], idx_name='Name',skipr=12):

        file = {}
        
        for sheet_nm in sheetnames:
            file[sheet_nm] = ((self.TS_dataopener(sheet_nm, idx_name, skipr))
                                   .applymap(GenDataOpener.zerotonan)
                                   .dropna(axis=0, how='all'))
            file[sheet_nm].columns = ['Name', 'Period'] + list(self.PF_dataCols(sheet_nm, sk_rows=9)[2:])
            file[sheet_nm] = file[sheet_nm].T.iloc[2:]

        return file    

    

    def rate_change(self, sheetname, num=1):
    
    ## If num 1 => 분기별
    ## If num 4 => 전년동기(분기)

        return super().TS_dataopener(sheetname).pct_change(num)

class StockInfoDataOpener(GenDataOpener):

    def opener(self, sheetnames=['KSE', 'KDQ'], idx_name='Code',skipr=12):

        file = {}
        
        for sheet_nm in sheetnames:
            file[sheet_nm] = (self.TS_dataopener(sheet_nm, idx_name, skipr)).applymap(GenDataOpener.zerotonan).dropna(axis=0, how='any')

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

class MarketCapOpener(GenDataOpener):

    ## FileSet 불러서 Data 호출 뒤
    ## Update
    
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

    def market_cap_opener(self, sheetname=['KSE', 'KDQ'], idx_name='D A T E', skipr=13):

        file = {}

        for sheet_nm in sheetname:
            temp = ((self.TS_dataopener(sheet_nm))
                                  .applymap(GenDataOpener.zerotonan)
                                  .dropna(axis=0, how='all'))
            temp.columns = self.PF_dataCols(sheet_nm)                                  
            file[sheet_nm] = temp.mean(axis=0).rank(ascending=False).apply(MarketCapOpener.marketcap)
            
            file[sheet_nm].to_csv(f"Data\MarketCap\{temp.index[-1].year}_{sheet_nm}.csv")                                             

        # return file

    ## Open Data
    ## 

class DateTimeOpener(GenDataOpener):

    def mkcap_change_date(self, sheetname='exp_date', drop_cols='D A T E', skipr=13):

        dt = self.drop_cols_opener(sheetname, drop_cols, skipr).T
        
        return pd.to_datetime(dt[0].apply(str)) + pd.DateOffset(1)





    

    ## 1. Month 12 1 2 then Average
        ## Year Diff then How
        ## Then Average Market Cap
    ## 2. Rank
        ## If the stuff is nan
            ## Discard
            ## Remained One
                ## 100: 대형주 101~300: 중형주 301 이하: 소형주
            ## 3월 둘째주 금요일부터 반영

    ## Str 저장보다는
        ## 1: 대형주, 2:중형주, 3: 소형주
    
        

    



        
    ## OpenFile

        ## Sector 

        ## Delisted

        ##
    
    # def Sect_Opener(self, sheetnames=['KSE', 'KDQ'], idx_name='Code', folder_name='Sector',skipr=12):
        
    #     for sheet_nm in sheetnames:
    #         ((self.TS_dataopener(sheet_nm, idx_name, skipr)).applymap(StockInfoDataOpener.zerotonan).dropna(axis=0, how='any')).to_csv(f'{self.dir}\{folder_name}\{sheet_nm}.csv')
    #         print(f"{sheet_nm}.csv saved in {folder_name}")


