import pandas as pd
from pandas.tseries.offsets import MonthEnd

class CSVReader:

    def __init__(self):

        pass

    def financial_reader(filename, directory):
        
        a = pd.read_csv(f"{directory}/{filename}", skiprows = 1)

        if (a['Code'].str.contains('AS')).sum() > 0: 
            a['Code'] = a['Code'].str.replace('AS', '-12-31')
            a['Code'] = pd.to_datetime(a['Code'])

        elif (a['Code'].str.contains('Q')).sum() > 0:

            for i in range(1,5):
                a['Code'] = a['Code'].str.replace(f"Q{i}", f"-{i*3}-29")

            a['Code'] = pd.to_datetime(a['Code']) + MonthEnd()
        
        else:
            a['Code'] = pd.to_datetime(a['Code'].astype('str'), format='%Y%m') + MonthEnd()

        return a.set_index('Code')

    def price_reader(filename, directory):

        return pd.read_csv(f"{directory}/{filename}", index_col = 'D A T E', parse_dates=True)

