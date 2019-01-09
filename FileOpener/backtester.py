import pandas as pd 
import numpy as np
from dateutil.relativedelta import relativedelta
import pandas.tseries.offsets as off

## Universe 종목

## Dates

class FinancialBacktest:

    def __init__(self, price):

        self.price = price

    def ret(self):

        return (self.price.pct_change()).dropna(axis=0, how='all')

    def listed_at_time(self, freq):

        return (~self.price.isnull()).resample(freq).sum() == 0

    def stock_screen(self, screen, freq):

        indices = screen.index
        stock_data = {}
        stock_listed = self.listed_at_time(freq)

        for idx in indices:
            
            stock_data[idx] = (screen.loc[idx][(screen.loc[idx] == True) & (stock_listed.loc[idx] == False)]).index

        return stock_data
    
    def back_date(self, screen, freq = 'Q'):

        rt = self.ret()
        st_dt = screen.index[0]
        last_dt = rt.index[-1] + off.MonthEnd()
        fin_lt_dt = screen.index[-1]

        norm_list = pd.date_range(st_dt, last_dt, freq=freq)
        fin_dt = pd.date_range(st_dt, fin_lt_dt, freq=freq)
        st_list = norm_list[:-1] + off.MonthBegin()
        ed_list = norm_list[1:]

        return fin_dt, st_list, ed_list

    def backtest(self, screen, freq_stock, freq_date='Q'):

        rt = self.ret()
        norm_list, st_list, ed_list = self.back_date(screen, freq_date)
        stocks = self.stock_screen(screen, freq_stock)
        
        ret_data = pd.Series()

        for n_start, start, end in zip(norm_list, st_list, ed_list):

            ret_data = pd.concat([ret_data, rt[stocks[n_start]].loc[start:end].mean(axis=1)])
        
        return ret_data


class PfAnalysis:
    
    def __init__(self, data):

        self.data = data.sub(-1)
        # self.index = data.index

    def totalReturn(self):

        return self.data.prod() - 1

    def cagr(self):

        ret = self.totalReturn() + 1

        dayobj = relativedelta(self.data.index[-1], self.data.index[0])
        year = dayobj.years
        month = dayobj.months
        days = 1 if dayobj.days > 15 else 0

        return ret ** (1/ (year + (month+days)/12)) - 1
        
        ## Date 무시
        ## Month 갔다쓰고 
        ## Day 15 기준 if 15이하 Then 0 15 이상 1

        pass

    def cumReturn(self):

        return self.data.cumprod()

    ## Volatility

    def rolling_vol(self, windows=252):

        return (self.data.rolling(window=windows).std(ddof=1)).div(1/np.sqrt(windows))

    ## drawDown
    def drawDown(self, windows=252):
        
        cum_rt = self.cumReturn()
        roll_max = (cum_rt).rolling(window=windows, min_periods=1).max()
        
        return (cum_rt).div(roll_max).sub(1)

    def maxDrawDown(self, windows=252):

        return self.drawDown(windows).min()

    ## Freq Return Should be fixed

    def freqReturn(self, freq = 'A'):

        return (self.data.resample(freq).prod().sub(1))




    

        

        

        

    

        


    

    


    



        