import pandas as pd
import numpy as np
from new_backtest import BacktestReturn

"""
1. 팩터에 필요한 Component 를 만드는 함수입니닷 뀨
"""

## Factor Creator
class Factor:

    ## 우량성 계산
        ## 각 항목별 순위를 매긴 후
        ## 매겨진 순위를 바탕으로 각 종목별 z-score를 계산한다.
        ## 지표 내 모든 항목의 z-score를 합한 후
        ## 합한 값을 바탕으로 z-score를 산출함

    """
    거래정지 구분 데이터 사용
    주식 스크리닝 필요함.
    """

    class Size:

        def __init__(self, marketcap):

            pass

    class Value:

        def __init__(self, price, pershare):

            ## Price: 가격 데이터
            ## perShare: 주당 팩터(EPS / SPS / CPS 등)

            self.price = price
            self.pershare = pershare

        def value_fact_comp(self, st_year=2002, ed_year=2019, non_zero=True):

            dt = pd.DataFrame()

            for year in range(st_year, ed_year):

                dt = pd.concat([dt, self.price.loc[f"{year}-01-01":f"{year}-03-31"].div(self.pershare.loc[f"{year-2}-12-31"])])
                dt = pd.concat([dt, self.price.loc[f"{year}-04-01":f"{year}-12-31"].div(self.pershare.loc[f"{year-1}-12-31"])])

            if non_zero == True:

                dt[dt < 0] = np.nan

                return dt

            elif non_zero == False:

                return dt

    class Quality:

        pass

    class ReturnPrep:

        def __init__(self, price):

            self.price = price

        def ret_creator(self):

            return BacktestReturn(self.price).ret_cleaner()

        def perd_return(self, freq = 'M'):

            ## Period Return

            return self.ret_creator().resample(freq).prod()

            ## 기간수익률(월별 혹은 분기 or WhatEver)

    class LowVol(ReturnPrep):

        ## 월별 수익률 측정
        ## 5년간 표준편차 (60회) Rolling

        pass


    class Momentum:

        class Relative(Prep):

            pass

        class Dual(Prep):

            pass




        class Relative:

            def __init__(self, price):

                self.price = price

        class  DualMomentum:

            def __init__(self, price):

                self.price = price

        def ret_creator(self):

            ##

            return
