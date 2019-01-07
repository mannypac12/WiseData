import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

        return self.data.resample(freq).prod()