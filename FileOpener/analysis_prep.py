import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FileOpener.DataOpener.DataOpener import PriceDataOpener, StockInfoDataOpener, FinancialDataOpener

## DataOpener(Stuff): olhc Opener

## Data Opener General

class PriceDataCleanser(PriceDataOpener):

    def __init__(self, file, dir='Data'):
        
        super().__init__(file, dir=dir)
        self.open, self.high, self.close, self.low = super().olhc()

    def daily_price_rt(self):

        return ((self.close).pct_change()).sub(-1)

    def candle(self):

        nan_dt = pd.isnull(self.close)
        candle_dt = self.close >= self.open 
        candle_dt[nan_dt] = np.nan
        
        def convertToBool(x):

            if x == 0: 
                return False
            elif x == 1:
                return True
            else:
                return np.nan

        return candle_dt.applymap(convertToBool)

    def candle_size(self):

        ## If 양봉 / 수정주가.div(수정시가)
        ## elif 음봉 / 수정시가.div(수정주가)                

        candle = self.candle()
        
        ans_dt = (self.close).div(self.open)
        ans_dt[candle == False] = (self.open).div(self.close)

        return ans_dt

    def uptail_size(self):

        ## Uptail 의 크기
        ## If 양봉 / 수정고가.div(수정주가)
        ## else 음봉 / 수정고가.div(수정시가)        
        candle = self.candle()

        ans_dt = (self.high).div(self.close)
        ans_dt[candle == False] = (self.high).div(self.open)

        return ans_dt

    def downtail_size(self):

        ## Downtail 의 크기

        ## Uptail 의 크기
        ## If 양봉 / 수정시가.div(수정저가)
        ## else 음봉 / 수정주가.div(수정시가)        

        ans_dt = (self.open).div(self.low)
        ans_dt[self.candle() == False] = (self.close).div(self.open)

    def SMPmovAvg(self, windows=5):

        ## 모든 이동평균선 분석은 Simple Moving Average 로 대신함

        return self.close.rolling(windows).mean()

    def EXPmovAvg(self, span=5):

        return (self.close).ewm(span).mean()        

    def mva_inline(self, shorter, longer, amount=5): 

    ## 정배열 
    ## 5일 이상 shorter window > Longer Window        
        
        shortmva = self.SMPmovAvg(shorter)
        longmva = self.SMPmovAvg(longer)

        return ((shortmva > longmva).rolling(amount).sum()) == amount
        
    def chan_break_out(self, windows):
        
        return self.close == (self.close).rolling(windows).max()

    def adj_price(self):

        ## if candle is red then 종가
        ## if candle is blue then 시가

        candle  = self.candle()
        cls_org_dt = self.close
        cls_org_dt[candle == False] = self.open

        return cls_org_dt
        
    def brc_chan_breakout(self, windows=20):

        ## 음봉은 시가가 우선
        
        # cls_price = self.data['수정주가']
        # brk_price = self.adj_price().rolling(windows).max()
        #          'brk_price_signal': cls_price == brk_price }

        return {
                    'brk_price': (self.adj_price()).rolling(windows).max(), 
                    'brk_price_signal': self.adj_price() == (self.adj_price()).rolling(windows).max()
               }
    
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


        trm_1 = (self.close).sub(self.low)
        trm_2 = (self.high).sub(self.close.shift(1)).abs()
        trm_3 = (self.low).sub(self.close.shift(1)).abs()        

        cols = self.close.columns
        idx = self.close.index

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
    
    def pocketPivot(self, shorter=10, longer=50, filter=200, mt_cls=10, shift_amt=2):

        cond_1 = self.mva_inline(shorter, longer).shift(shift_amt)
        cond_2 = (self.candle() == True)
        cond_3 = self.close > self.SMPmovAvg(mt_cls)
        cond_3 = self.SMPmovAvg(mt_cls) > self.SMPmovAvg(filter)

        return cond_1 & cond_2 & cond_3

"""
    Class DualMomentum

        ## Inherit From PriceDataAnalysis
        ## Common Dual Momentum
            ## Default Ten Choose
            ## But if lower than Ten stuff's return are lower than zero then only then the number choose
        ## Basic Dual Momentum
            ## 30 day return / 90 day holding: Can be changed Anytime soon
        ## Elegance Dual Momentum
            ## Add Some technical Indicator / 
                ## Holding Period can vary according to the indicators
"""
    
class BasicDualMomentum(PriceDataCleanser):

    def __init__(self, file, dir='Data'):
        super().__init__(file, dir=dir)
        self.ret = self.daily_price_rt()

    def rolling_return(self, windows=30):

        return (self.ret.rolling(windows).apply(lambda x: np.prod(x), raw=True)).dropna(how='all')

    def morethanzero(self, windows=30):

        ## 절대 수익률: More than 0
        return (self.rolling_return(windows)).applymap(lambda x: True if x > 1 else False)

    def rank(self, windows=30):

        return (self.rolling_return(windows)).rank(axis = 1, ascending=False)

    def DualSecurity(self, windows=30):

        tr = self.morethanzero(windows)
        
        return self.rank(windows)[tr]

    def SelectableSecurity(self, windows=30):

        ## Selectable Security
        
        dt = self.DualSecurity(windows=30)
        idx = dt.index
        invest = {}

        for date in idx: 
            temp = dt.loc[date].dropna().reset_index()
            temp.columns = ['sec_name', 'rank']
            
            ## 
            invest[date] = list(temp.sort_values(by='rank', ascending=True)['sec_name'])
            # invest[date] = list((dt.loc[date].dropna().sort_values(ascending=True)).index)

        return invest

    def compositReturn(self, windows=30, holding_date=60, start=0, sec=10):

        select_sec = self.SelectableSecurity(windows)
        
        ## date keys

        select_sec_date = list(select_sec.keys())
        chs_date = []
        ansDt = pd.Series()

        for i in range(start, len(select_sec_date), holding_date):

            chs_date.append(select_sec_date[i])

        for date in chs_date:

            columns = select_sec[date][:sec]
            
            ## The stuff is Equal Weight The code should be modified if other allocation method required            
            num_cols = len(columns)
            dt = ((self.ret.loc[date:, columns].iloc[:holding_date]).div(num_cols)).sum(axis=1)
            ansDt = pd.concat([ansDt, dt])
            
        return ansDt

"""
백테스트 전용 클래스 만들어보기
"""    

class PfAnalysis:
    
    def __init__(self, data):

        self.data = data
        # self.index = data.index

    def cumReturn(self):

        return self.data.cumprod()

    ## Volatility

    def rolling_vol(self, windows=252):

        return (self.data.rolling(window=windows).std(ddof=1)).div(1/np.sqrt(windows))

    ## drawDown
    def drawDown(self, windows=252):

        roll_max = self.data.rolling(window=windows, min_periods=1).max()
        
        return (self.data).div(roll_max).sub(1)

    def maxDrawDown(self, windows=252):

        return self.drawDown(windows).min()

class Delisted:

    def __init__(self, data):

        self.data=data
    
    




## 
## 레알 상폐: Return should be 0
## 합병주식: Return should be 1


    ## Composit Return 
    ## Maximum DrawDown
    ##



## 이격 공식 / 다른 클래스로 해서
## m + 2*sd or - 2*sd 공식화하긔

    ## 이격(%로 표시하기)
    ## 이격 공식: 


# objOne = PriceDataCleanser(file="price.xlsm")   
# print(objOne.pocketPivot(10, 50,200,10,2).sum())

