import pandas as pd 
import numpy as np
from dateutil.relativedelta import relativedelta
import pandas.tseries.offsets as off
import matplotlib as mpl 
import matplotlib.pyplot as plt
import seaborn as sns

## Universe 종목

## Dates

class FinancialBacktest:

    def __init__(self, price):

        self.price = price

    def ret(self):

        ret = self.price.div(self.price.shift(1)) 

        ret.loc[:'1998-05-23'][ret.loc[:'1998-05-23'] > 1.08] = 1.08
        ret.loc['1998-05-25':'2005-03-25'][ret.loc['1998-05-25':'2005-03-25'] > 1.12] = 1.12
        ret.loc['2005-03-28':'2015-06-14'][ret.loc['2005-03-28':'2015-06-14'] > 1.15] = 1.15
        ret.loc['2015-06-15':][ret.loc['2015-06-15':] > 1.3] = 1.3       

        return ret.dropna(axis=0, how='all')

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

        self.data = data

    def cumReturn(self):

        return self.data.cumprod()

    def totalReturn(self):

        return self.data.prod() - 1        

    def freqReturn(self, freq = 'A'):

        return ((self.data).resample(freq).prod().sub(1))

    def median_return(self, freq = 'A'):

        return self.freqReturn(freq).median()

    def mean_return(self, freq = 'A'):

        return self.freqReturn(freq).mean()

    def geo_mean_return(self, freq = 'A'):
        
        ret = self.freqReturn(freq)

        return np.power((ret.sub(-1)).prod(), 1/ret.shape[0]) - 1

    def cagr(self):

        ret = self.totalReturn() + 1

        ## Date 무시
        ## Month 갔다쓰고 
        ## Day 15 기준 if 15이하 Then 0 15 이상 1

        dayobj = relativedelta(self.data.index[-1], self.data.index[0])
        year = dayobj.years
        month = dayobj.months
        days = 1 if dayobj.days > 15 else 0

        return ret ** (1/ (year + (month+days)/12)) - 1

    def volatility(self):

        ## 252로 연율화 할것

        return (self.data.std(ddof=1)) * np.sqrt(252)

    def freqVol(self, freq = 'A'):

        vol = lambda x: np.std(x, ddof=1) * np.sqrt(265)

        return ((self.data).resample(freq).apply(vol))   

    def upordownvol(self, option=True):

        ret = self.data

        if option == True: 
            ## Upside Deviation
            return (ret[ret>1]).std() * np.sqrt(252)

        elif option == False:
            ## Downside Devitation
            return (ret[ret<1]).std() * np.sqrt(252)

    def drawDown(self, windows=252):
        
        cum_rt = self.cumReturn()
        roll_max = (cum_rt).rolling(window=windows, min_periods=1).max()
        
        return (cum_rt).div(roll_max).sub(1)

    def maxDrawDown(self, windows=252):

        return self.drawDown(windows).min()

    def rt_preety_print(self, freq='A'):

        ## 수익률 

        return pd.Series(index=['평균수익률', '기하수익률', '중간수익률'],
                         data=[self.mean_return(freq), 
                               self.geo_mean_return(freq), 
                               self.median_return(freq)]).map('{:,.2%}'.format)

    def vol_preety_print(self):

        vol = self.volatility()
        upvol = self.upordownvol(option=True)
        downvol = self.upordownvol(option=False)
        MDD = np.abs(self.maxDrawDown(windows=252)) 

        return pd.Series(index=['변동성', 'Upside Dev.', 'Downside Dev.', 'MDD'], 
                         data=[vol, upvol, downvol, MDD]).map('{:,.2%}'.format)

    ## Rolling 
    ## One Year // Three Year / Five Year

    def rolling_return(self, n=1):

        ## n: Year

        rol_rt = lambda x: np.prod(x)

        return self.data.rolling(252 * n).apply(rol_rt).sub(1)

    def rolling_max(self, n):

        return self.rolling_return(n).max().sub(1)

    def rolling_min(self, n):

        return self.rolling_return(n).min().sub(1)

    def rol_pretty_print(self):

        return pd.DataFrame(index=['1 Year', '3 Year', '5 year'],
                                 columns=['Min', 'Max'], 
                                 data=[[self.rolling_min(1),
                                        self.rolling_max(1)],
                                        [self.rolling_min(3),
                                        self.rolling_max(3)],
                                        [self.rolling_min(5),
                                        self.rolling_max(5)]]).sub(-1).applymap('{:,.2%}'.format)

class Plot:

    ## fig, ax Constructor

    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def mpl_setup(self):

        ## MPL Setup

        mpl.rcParams['axes.unicode_minus'] = False
        mpl.rcParams["font.family"] = 'NanumGothic'
        mpl.rcParams["font.size"] = 20
        mpl.rcParams["figure.figsize"] = (14,4)

    def TimeSeries(self):

        self.mpl_setup()

        self.fig.set_size_inches((20, 10))

        for spine in ['top', 'right']:
            self.ax.spines[spine].set_color('none')

        self.ax.margins(x=0)
        self.ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda y, _: '{:,.0%}'.format(y)))

        return self.fig, self.ax

    def adjFreq(self, data, xy=['year', 'return']):

        adj_data = data.reset_index()
        adj_data.columns = xy
        adj_data[xy[0]] = adj_data[xy[0]].dt.year

        return adj_data

    def FreqPlot(self, data, xy=['year', 'return']):

        self.mpl_setup()        

        fig, ax = self.TimeSeries()
        adj_data = self.adjFreq(data,xy)
        sns.barplot(x=xy[0], y=xy[1], data=adj_data, color='#727272', ax = ax)
        ax.set_ylabel('')    
        ax.set_xlabel('')

        return fig, ax


        


        

    ## Bar Graph 그릴려면
        ## sns



    


        ## 일두의 힘!

    

        


    ## Time

        ## size

    ## Bar

    

    

    ## Cum Return Plot 

    ## Freq Return Plot





    

        

        

        

    

        


    

    


    



        