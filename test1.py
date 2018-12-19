import pandas as pd

columns = list(pd.read_excel('Data\\test.xlsm',skiprows=8, nrows=0).columns)[1:]

dt = pd.read_excel('Data\\test.xlsm',usecols=8,skiprows=13).set_index('D A T E')
dt.columns = columns

print(dt)