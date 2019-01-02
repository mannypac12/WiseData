import pandas as pd
import re
from FileOpener.Fileset import fileset as fl
from FileOpener.DataOpener.DataOpener import FinancialDataOpener

print(FinancialDataOpener('op_income.xlsx').opener()['KDQ'].head())

## 상장폐지일 => 날짜 / 
