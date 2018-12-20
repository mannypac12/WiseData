## Pandas
## 수익률
## 

import pandas as pd

class DataOpener:

    def __init__(self, file, dir="Data"):

        self.fullpath=f"{dir}\\{file}"
        
        
    def dataCols(self):

        return pd.read_excel(self.fullpath, skiprows=8, nrows=1).columns[1:]
    
    def dataopener(self, sheetname):
        
        dt = pd.read_excel(self.fullpath,sheet_name=sheetname,skiprows=13).set_index('D A T E')
        dt.columns = self.dataCols()

        return dt

class Anlytics(DataOpener):

    def __init__(self, file, *kwargs):
        return super().__init__(file, *kwargs)

    def rate_change(self, sheetname, num=1):

        return super().dataopener(sheetname).pct_change(num)

# test_dt = DataOpener(file='KOSPI200_opInc.xltm').dataopener("영업이익")
# print(test_dt.pct_change(4))

print(Anlytics('KOSPI200_opInc.xltm').rate_change("영업이익", 4))