<<<<<<< HEAD
=======
import pandas as pd
import re
from FileOpener.Fileset import fileset as fl
from FileOpener.DataOpener.DataOpener import FinancialDataOpener

print(FinancialDataOpener('op_income.xlsx').opener()['KDQ'].head())

## 상장폐지일 => 날짜 / 
>>>>>>> 221ad3897250990e1c598aebdedef444a2755a59
