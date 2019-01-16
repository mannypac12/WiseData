import pandas as pd 
# import numpy as np
# from dateutil.relativedelta import relativedelta
# import pandas.tseries.offsets as off
# import matplotlib as mpl 
# import matplotlib.pyplot as plt
# import seaborn as sns

# mpl.rcParams['axes.unicode_minus'] = False
# mpl.rcParams["font.family"] = 'NanumGothic'
# mpl.rcParams["font.size"] = 20
# mpl.rcParams["figure.figsize"] = (14,4)




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

    class Finance:

        def __init__(self, ret):

            self.ret = ret

        @property
        def st_end_date(self):

            return (self.ret.index[0], self.ret.index[-1])

        def stuff(self):
            print(self.st_end_date)

        def cumReturn(self):

            return self.ret.cumprod() - 1 

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
        

    class Price:    

        def __init__(self, ret):

            self.ret = ret        





        ## if rt_index[-1] > ~+Q

            ## then 
            ## else
                ## ed_date = screen[-1]

        ## Quarter





    # def back_date(self, screen, freq = 'Q'):

    #     ## Date를 집어 넣을 때 반영
        
    #     rt = self.ret_cleaner().index
    #     st_dt = screen.index[0]
    #     last_dt = rt.index[-1] + off.MonthEnd()
    #     fin_lt_dt = screen.index[-1]

    #     norm_list = pd.date_range(st_dt, last_dt, freq=freq)
    #     fin_dt = pd.date_range(st_dt, fin_lt_dt, freq=freq)
    #     st_list = norm_list[:-1] + off.MonthBegin()
    #     ed_list = norm_list[1:]

    #     return fin_dt, st_list, ed_list

    
    

    ## Tier Analysis
        
# class Price(BacktestReturn):

#     pass

# class PerformanceAnalytics:

#     pass

#     class Financial:

#         class Indicators:
#             pass
#         class Plot:
#             pass

#     class Price:
#             pass
#         class Indicators:        
#             pass
#         class Plot:        
#             pass            

print(PFAnalysis.Finance(pd.DataFrame(index=pd.date_range('2017-01-01', '2017-01-10'))).st_end_date)