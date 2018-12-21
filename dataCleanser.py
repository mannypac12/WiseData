## Pandas
## 수익률
## 

import pandas as pd
import numpy as np

class DataOpener:

    def __init__(self, file, dir="Data"):

        self.fullpath=f"{dir}\\{file}"
        
        
    def dataCols(self):

        return pd.read_excel(self.fullpath, skiprows=8, nrows=1).columns[1:]
    
    def TS_dataopener(self, sheetname):

        dt = pd.read_excel(self.fullpath,sheet_name=sheetname,skiprows=13).set_index('D A T E')
        dt.columns = self.dataCols()

        return dt

class FinancialAnlytics(DataOpener):

    # def __init__(self, file, *kwargs):
    #     return super().__init__(file, *kwargs)

    def rate_change(self, sheetname, num=1):
        
        ## If num 1 => 분기별
        ## If num 4 => 전년동기(분기)

        return super().TS_dataopener(sheetname).pct_change(num)

class PriceAnalytics(DataOpener):

    # def __init__(self, file, *kwargs):
    #     return super().__init__(file, *kwargs)

    def olhc(self, sheetnames=["수정시가", "수정고가", "수정주가", "수정저가"], num=1):
        
        prices = {}

        for sheet_nm in sheetnames:
            prices[sheet_nm] = super().TS_dataopener(sheet_nm)
        
        return prices

    def daily_price_rt(self):

        return self.olhc()["수정주가"].pct_change()

    def candle(self):

        org_dt = self.olhc()

        nan_dt = pd.isnull(org_dt["수정주가"])
        candle_dt = org_dt["수정주가"] >= org_dt["수정시가"]
        candle_dt[nan_dt] = np.nan
        
        def convertToBool(x):

            if x == 0: 
                return False
            elif x == 1:
                return True
            else:
                return np.nan

        return candle_dt.applymap(convertToBool)

    def SMPmovAvg(self, windows=5):

        return self.olhc()["수정주가"].rolling(windows).mean()

    def EXPmovAvg(self, span=5):

        return self.olhc()["수정주가"].ewma(span).mean()        
    
    def channel_breakout(self, windows=20):
        org_dt = self.olhc()["수정주가"]
        
        return org_dt == org_dt.rolling(windows).max()

    def brc_chan_breakout(self, windows=20):

        ## 음봉은 시가가 우선

        cls_org_dt = self.olhc()["수정주가"]
        opn_org_dt = self.olhc()["수정시가"]
        
        cls_org_dt[self.candle() == False] = opn_org_dt

        return cls_org_dt == cls_org_dt.rolling(windows).max()

        ## 보합시 양봉
        ## case    
objOne = PriceAnalytics(file="price.xlsm")        
test = objOne.brc_chan_breakout()
print(test.sum())




