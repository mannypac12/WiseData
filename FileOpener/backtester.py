import pandas as pd 
import numpy as np
import pandas.tseries.offsets as off

## Universe 종목

## Dates

class FinancialBacktest:

    def __init__(self, ret):

        self.ret = ret

    def stock_screen(self, screen):

        indices = screen.index
        stock_data = {}

        for idx in indices:
            
            stock_data[idx] = (screen.loc[idx][screen.loc[idx] == True]).index

        return stock_data
    
    def back_date(self, screen, freq = 'Q'):

        st_dt = screen.index[0]
        last_dt = self.ret.index[-1] + off.MonthEnd()
        fin_lt_dt = screen.index[-1]

        norm_list = pd.date_range(st_dt, last_dt, freq=freq)
        fin_dt = pd.date_range(st_dt, fin_lt_dt, freq=freq)
        st_list = norm_list[:-1] + off.MonthBegin()
        ed_list = norm_list[1:]

        return fin_dt, st_list, ed_list

    def backtest(self, screen, freq='Q'):

        norm_list, st_list, ed_list = self.back_date(screen, freq)
        stocks = self.stock_screen(screen)
        
        ret_data = pd.Series()

        for n_start, start, end in zip(norm_list, st_list, ed_list):

            ret_data = pd.concat([ret_data, self.ret[stocks[n_start]].loc[start:end].mean(axis=1)])
        
        return ret_data


class PfAnalysis:
    
    def __init__(self, data):

        self.data = data.sub(-1)
        # self.index = data.index

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

    def freqReturn(self, freq = 'A'):

        return (self.data.resample(freq).prod().sub(1)).apply(lambda x: '{:, .2%}'.format(x))




    

        

        

        

    

        


    

    


    



        