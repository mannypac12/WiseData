import pandas as pd
import numpy as np
from FileOpener.analysis_prep import PriceDataCleanser 

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
