import pandas as pd
import re
from FileOpener.DataOpener.DataOpener import StockInfoDataOpener

StockInfoDataOpener('Delisted.xlsx').Sect_Opener(folder_name='Delisted')

## 상장폐지일 => 날짜 / 
