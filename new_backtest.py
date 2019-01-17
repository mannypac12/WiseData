import pandas as pd 
import numpy as np
from dateutil.relativedelta import relativedelta
import pandas.tseries.offsets as off
import matplotlib as mpl 
import matplotlib.pyplot as plt
import seaborn as sns

mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams["font.family"] = 'NanumGothic'
mpl.rcParams["font.size"] = 20
mpl.rcParams["figure.figsize"] = (14,4)


class BacktestReturn:

    def __init__(self, price):

        self.price = price

    def ret(self):

        return self.price.div(self.price.shift(1))

    def ret_cleaner(self):

        ret = self.ret()

        ret.loc[:'1998-05-23'][ret.loc[:'1998-05-23'] > 1.08] = 1.08
        ret.loc['1998-05-25':'2005-03-25'][ret.loc['1998-05-25':'2005-03-25'] > 1.12] = 1.12
        ret.loc['2005-03-28':'2015-06-14'][ret.loc['2005-03-28':'2015-06-14'] > 1.15] = 1.15
        ret.loc['2015-06-15':][ret.loc['2015-06-15':] > 1.3] = 1.3  

        return ret.dropna(axis=0, how='all')

class Financial(BacktestReturn): 

    def __init__(self, price, screen):
        super().__init__()
        self.screen = screen

    ## Only One 
    @staticmethod
    def screen_deficit(option=True):

        if option == True:
            return screen[screen < 0]
        elif option == False:
            return screen[screen > 0]

    ## With Tier
    @staticmethod
    def screen_rank(screen, perc=10, ascending=False):

        ## perc: Percentile

        rank = screen.rank(axis=1, pct=True, ascending=ascending)
        
        for i in range(0, perc):

            n_1 = (i+1) / perc
            n = i / perc 
            rank[(n < rank) & (rank < n_1)] = n_1 * perc 

        return rank    

    def listed_at_time(self, freq):

        return (~self.price.isnull()).resample(freq).sum() == 0

    def stock_screen(self, screen, freq):

        indices = screen.index
        stock_data = {}
        stock_listed = self.listed_at_time(freq)

        for idx in indices:
            
            stock_data[idx] = (screen.loc[idx][(screen.loc[idx] == True) & (stock_listed.loc[idx] == False)]).index

        return stock_data

    def testing_date(self, screen, freq = 'Q'):

        ## Freq 생성
        fin_st_date = screen.index[0]
        fin_lst_date = screen.index[-1]

        fin_dt = pd.date_range(fin_st_date, fin_lst_date, freq=freq)
        st_list = fin_dt[:-1] + off.MonthBegin()
        ed_list = fin_dt[1:]

        return fin_dt[:-1], st_list, ed_list

    def backtest(self, screen, freq_stock, freq_date='Q'):

        rt = self.ret_cleaner()
        norm_list, st_list, ed_list = self.testing_date(screen, freq_date)
        stocks = self.stock_screen(screen, freq_stock)
        
        ret_data = pd.Series()

        for n_start, start, end in zip(norm_list, st_list, ed_list):

            ret_data = pd.concat([ret_data, rt[stocks[n_start]].loc[start:end].mean(axis=1)])
        
        return ret_data

    def tier_backtest(self, rank, freq_stock, freq_date='Q', n=10):

        tier = {}

        for i in range(1, n+1):

            tier[f"Tier {i}"] = self.backtest(rank == i, freq_stock, freq_date)

        return pd.DataFrame(tier)


class PriceBacktester(BacktestReturn):

    def catch_signal(self, filter):

        signal = {}

        for key in filter.columns:

            temp = filter[key][filter[key]==True].index

            if len(temp) == 0: 
                pass
            else:
                signal[key] = temp
    
        return signal

    def hodling_backtest(self, filter, n=10):
        
        ## 신호 후 변경할 것
        ## n: Days of Holding

        ## Dictionary 해서 종목별로 매핑해보기

        ret_data = self.ret_cleaner()
        ret = []
        signal = self.catch_signal(filter)

        for key, value in signal.items():

            for date in value:

                from_date = date + relativedelta(days=1)
                to_date = date + relativedelta(days=n)
                ret.append((ret_data[key].loc[from_date:to_date]).prod())
        
        return np.array(ret)

class PFAnalysis:

    class Plot:

        def __init__(self):

            self.fig, self.ax = plt.subplots()

        def mpl_setup(self):

            mpl.rcParams['axes.unicode_minus'] = False
            mpl.rcParams["font.family"] = 'NanumGothic'
            mpl.rcParams["font.size"] = 20
            mpl.rcParams["figure.figsize"] = (20,10)

    class Finance:

        def __init__(self, ret, st_date=None, ed_date=None):

            ## st_date / ed_date as 'YYYY-MM-DD' or 'YYYYMMDD'
            if st_date = None:
                self.st_date = ret.index[0]
            else: 
                self.st_date = pd.to_datetime(st_date)

            if ed_date = None: 
                self.ed_date = ret.index[-1]
            else:
                self.ed_date = pd.to_datetime(ed_date)

            self.ret = ret.loc[self.st_date:self.ed_date]

        def totalReturn(self):

            return self.ret.prod() - 1        

        def freqReturn(self, freq = 'A'):

            return ((self.ret).resample(freq).prod().sub(1))

        def median_return(self, freq = 'A'):

            return self.freqReturn(freq).median()

        def mean_return(self, freq = 'A'):

            return self.freqReturn(freq).mean()

        def geo_mean_return(self, freq = 'A'):
            
            ret = self.freqReturn(freq)

            return np.power((ret.sub(-1)).prod(), 1/ret.shape[0]) - 1

        def volatility(self):

            ## 252로 연율화 할것

            return (self.ret.std(ddof=1)) * np.sqrt(252)

        def freqVol(self, freq = 'A'):

            vol = lambda x: np.std(x, ddof=1) * np.sqrt(265)

            return ((self.ret).resample(freq).apply(vol))

        def upordownvol(self, option=True):

            ret = self.ret

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

    class PfTier(Finance):

        def preety_print(self, freq):

            return pd.DataFrame([self.totalReturn().rename('총수익률'),
                                 self.mean_return(freq).rename('Arithmetic Mean Return'),
                                 self.geo_mean_return(freq).rename('Geometric Mean Return'),
                                 self.median_return(freq).rename('Median Return'),
                                 self.volatility().rename('Vol.'),
                                 self.upordownvol().rename('Upside Vol.'),
                                 self.upordownvol(option=False).rename('Downside Vol.'),                  
                                 abs(self.maxDrawDown()).rename('MDD')]).applymap('{: .2%}'.format)

    class PfOneWay(Finance):

        def preety_print(self, freq):

            return pd.Series(index = ['총수익률', 'Arithmetic Mean Return', 'Geometric Mean Return',
                                      'Median Return', 'Vol.', 'Upside Vol.', 'Downside Vol.', 'MDD'],
                             data = [self.totalReturn(), self.mean_return(freq), self.geo_mean_return(freq),
                                    self.median_return(freq), self.volatility(), self.upordownvol(),
                                    self.upordownvol(option=False), abs(self.maxDrawDown()))]).map('{: .2%}'.format)

    class FinancePlot(Finance, Plot):

        def TimeSeries(self):

            self.mpl_setup()

            for spine in ['top', 'right']:
                self.ax.spines[spine].set_color('none')

            self.ax.margins(x=0)
            self.ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda y, _: '{:,.0%}'.format(y)))

            return self.fig, self.ax

        def cumReturn(self):

            return self.ret.cumprod() - 1         

        def CumReturn_Plot(self):

            fig, ax = self.TimeSeries()
            self.cumReturn().plot(ax=ax)

            return fig, ax
 
    class Price:

        def __init__(self, ret):

            self.ret = ret

        def num_of_signal(self):

            return self.ret.shape[0]

        def win_rate(self):
            
            return (self.ret > 1).sum() / self.num_of_signal()

        def mean_rt(self):

            return (self.ret.mean()) - 1

        def min_rt(self):

            return (self.ret.min()) - 1

        def max_rt(self):

            return (self.ret.max()) - 1        

        def med_rt(self):

            return np.median(self.ret) - 1 

    class PfPrice(Price):

        def pretty_print(self):

            return pd.Series(index = ['승률', '매매신호', '중위수익률', '평균수익률', '최소수익률'],
                             data = ['{:2.2%}'.format(self.win_rate()),
                                     f"{self.num_of_signal()}회", 
                                     '{:2.2%}'.format(self.med_rt()),
                                     '{:2.2%}'.format(self.mean_rt()), 
                                     '{:2.2%}'.format(self.min_rt()), 
                                     '{:2.2%}'.format(self.max_rt())])

    class PricePlot(Price, Plot):

        def hist_plot(self):

            self.mpl_setup()
            self.ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: '{:,.0%}'.format(x)))

            for spine in ['top', 'right']:
                self.ax.spines[spine].set_color('none')

            sns.distplot(self.ret - 1, ax = self.ax, color = '#727272')

            return self.fig, self.ax                                    