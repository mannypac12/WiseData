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

    def candle_prep_function(self):

        org_dt = self.olhc()
        candle = self.candle()

        return org_dt, candle

    def candle_size(self):

        ## If 양봉 / 수정주가.div(수정시가)
        ## elif 음봉 / 수정시가.div(수정주가)                

        org_dt, candle = self.candle_prep_function()
        
        ans_dt = org_dt['수정주가'].div(org_dt['수정시가'])
        ans_dt[candle == False] = org_dt['수정시가'].div(org_dt['수정주가'])

        return ans_dt

    def uptail_size(self):

        ## Uptail 의 크기
        ## If 양봉 / 수정고가.div(수정주가)
        ## else 음봉 / 수정고가.div(수정시가)        

        org_dt, candle = self.candle_prep_function()

        ans_dt = org_dt['수정고가'].div(org_dt['수정주가'])
        ans_dt[candle == False] = org_dt['수정고가'].div(org_dt['수정시가'])

        return ans_dt

    def downtail_size(self):

        ## Downtail 의 크기

        ## Uptail 의 크기
        ## If 양봉 / 수정시가.div(수정저가)
        ## else 음봉 / 수정주가.div(수정시가)        

        org_dt, candle = self.candle_prep_function()

        ans_dt = org_dt['수정시가'].div(org_dt['수정저가'])
        ans_dt[candle == False] = org_dt['수정주가'].div(org_dt['수정저가'])

        return ans_dt        

    def SMPmovAvg(self, windows=5):

        ## 모든 이동평균선 분석은 Simple Moving Average 로 대신함

        return self.olhc()["수정주가"].rolling(windows).mean()

    def EXPmovAvg(self, span=5):

        return self.olhc()["수정주가"].ewma(span).mean()        
    
    def channel_breakout(self, windows=20):
        org_dt = self.olhc()["수정주가"]
        
        return org_dt == org_dt.rolling(windows).max()

    def adj_price(self):

        ## if candle is red then 종가
        ## if candle is blue then 시가

        org_dt = self.olhc()
        candle  = self.candle()

        cls_org_dt = org_dt['수정주가']
        opn_org_dt = org_dt['수정시가']
        
        cls_org_dt[candle == False] = opn_org_dt

        return cls_org_dt
        
    def brc_chan_breakout(self, windows=20):

        ## 음봉은 시가가 우선
        cls_price = self.olhc()['수정주가']
        brk_price = self.adj_price().rolling(windows).max()

        return { 'brk_price': brk_price, 
                 'brk_price_signal': cls_price == brk_price }
    
    def MVA_divergence(self, windows=5):
        ## 5일 대비 이격
        adj_price = self.adj_price()
        comp_mva = self.SMPmovAvg(windows)

        return adj_price.div(comp_mva).div(1/100).dropna(how='all', axis=0)

    def MVA_diff(self, windows=5):

        return self.SMPmovAvg(windows).pct_change()

    def mva_cross(self, windows_short = 10, windows_long = 50): 

        SMPShort = self.SMPmovAvg(windows_short)
        SMPLong = self.SMPmovAvg(windows_long)

        prev_SMPShort = SMPShort.shift(1)
        prev_SMPLong = SMPLong.shift(1)

        gd_cross = (SMPShort <= SMPLong) & (prev_SMPShort >= prev_SMPLong)
        dth_cross = (SMPShort >= SMPLong) & (prev_SMPShort <= prev_SMPLong)

        return {'golden': gd_cross, 'death': dth_cross}

##

    ## 이격(%로 표시하기)
    ## 이격 공식: 



objOne = PriceAnalytics(file="price.xlsm")        
# test_one = objOne.brc_chan_breakout()
test_two = objOne.downtail_size()
print(test_two)
# print(test_two.sum())




