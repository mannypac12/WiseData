import pandas as pd
import re
from FileOpener.Fileset import fileset as fl
from FileOpener.DataOpener.DataOpener import MarketCapOpener

fl.Fileset('MarketCap1.xlsm')

MarketCapOpener('MarketCap1.xlsx').market_cap_opener()

## 상장폐지일 => 날짜 / 
