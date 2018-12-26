## Pandas
## 수익률
## 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## DataOpener(Stuff): olhc Opener

class DataOpener:

    def __init__(self, file, dir="Data"):

        self.fullpath=f"{dir}\\{file}"
        
    def dataCols(self):

        return pd.read_excel(self.fullpath, skiprows=8, nrows=1).columns[1:]
    
    def TS_dataopener(self, sheetname):

        dt = pd.read_excel(self.fullpath,sheet_name=sheetname,skiprows=13).set_index('D A T E')
        dt.columns = self.dataCols()

        return dt

    def olhc(self, sheetnames=["수정시가", "수정고가", "수정주가", "수정저가"], num=1):
        
        prices = {}

        for sheet_nm in sheetnames:
            prices[sheet_nm] = self.TS_dataopener(sheet_nm)
        
        return prices

class FinancialAnlytics(DataOpener):

    # def __init__(self, file, *kwargs):
    #     return super().__init__(file, *kwargs)

    def rate_change(self, sheetname, num=1):
        
        ## If num 1 => 분기별
        ## If num 4 => 전년동기(분기)

        return super().TS_dataopener(sheetname).pct_change(num)

class PriceDataCleanser(DataOpener):

    # def __init__(self, file, *kwargs):
    #     return super().__init__(file, *kwargs)

    # def olhc(self, sheetnames=["수정시가", "수정고가", "수정주가", "수정저가"], num=1):
        
    #     prices = {}

    #     for sheet_nm in sheetnames:
    #         prices[sheet_nm] = super().TS_dataopener(sheet_nm)
        
    #     return prices

    def daily_price_rt(self):

        return (self.olhc()["수정주가"].pct_change()).sub(-1)

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

    def true_range(self):

        org_dt = self.olhc()

        trm_1 = org_dt["수정주가"].sub(org_dt["수정저가"])
        trm_2 = org_dt["수정고가"].sub(org_dt["수정주가"].shift(1)).abs()
        trm_3 = org_dt["수정저가"].sub(org_dt["수정주가"].shift(1)).abs()        

        cols = org_dt["수정주가"].columns
        idx = org_dt["수정주가"].index

        ans_dt = pd.DataFrame(index = idx, columns = cols, data=np.zeros((len(idx), len(cols))))

        for col in cols:
            ans_dt[col] = pd.concat([trm_1[col], trm_2[col], trm_3[col]], axis=1).max(axis=1)

        return ans_dt

    def avg_tr_range(self, windows=14):

        return self.true_range().rolling(windows).mean()

    def avg_tr_diff(self, windows=14):

        return self.avg_tr_range(windows).pct_change()

    def relative_strength(self, comp_rt= None, windows=60):

        ## comp_rt should be (1+r) like that

        ## Relative Strength
        ## 지수 등의 Return을 불러와야 함
        ## Rolling: 60일 / 90일        

        product = lambda x: np.prod(x)

        cum_rt = (self.daily_price_rt()).rolling(windows).apply(product, raw=True)
        cum_comp_rt = comp_rt.rolling(windows).apply(product, raw=True)

        return cum_rt.div(cum_comp_rt).div(1/100)

class ChartGrid(PriceDataCleanser):

    ## GraphQL이 필요해...
    def stock_data(self, stock):

        ord_dt = self.olhc()
        cls_prc = ord_dt['수정주가'][stock]
        low_prc = ord_dt['수정저가'][stock]
        high_prc = ord_dt['수정고가'][stock]
        opn_prc = ord_dt['수정시가'][stock]

        return cls_prc, low_prc, high_prc, opn_prc
        ## 도망가자 큨큨

    




## Stock Chart

## Bar Chart
## 





    ## 차후 시스템 개발 후 덧붙일 것 
        
    ## 상승세 Using MVA

    ## 50일선 > 120일선
    ## MVA DIFF for short is bigger tha
        
        
        

        

        ## Use High / Low / Close

        ## Method One   
            ## High - Low
        ## Method Two
        ## Method Three

        ## Choose the max value of three of them


    

## 이격 공식 / 다른 클래스로 해서
## m + 2*sd or - 2*sd 공식화하긔

    ## 이격(%로 표시하기)
    ## 이격 공식: 



objOne = ChartGrid(file="price.xlsm")        
# test_one = objOne.brc_chan_breakout()
test_two = objOne.data
print(test_two)
# print(test_two.sum())





