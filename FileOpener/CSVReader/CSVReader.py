import pandas as pd
from pandas.tseries.offsets import MonthEnd

class CSVReader:

    def __init__(self):

        pass

    def financial_reader(filename, directory):

        data = pd.read_csv(f"{directory}/{filename}", skiprows = 1)
        data['Code'] = data['Code'].astype('str')

        if (data['Code'].str.contains('AS')).sum() > 0: 
            data['Code'] = pd.to_datetime(data['Code'].str.replace('AS', '-12-31'))
        
        elif (data['Code'].str.contains('Q')).sum() > 0:
            for i in range(1,5):
                data['Code'] = data['Code'].str.replace(f"Q{i}", f"-{i*3}-01")
                data['Code'] = pd.to_datetime(data['Code']) + MonthEnd()

        else:
            data['Code'] = pd.to_datetime(data['Code'], format='%Y%m') + MonthEnd()
        
        return data.set_index('Code')

    def price_reader(filename, directory):

        return pd.read_csv(f"{directory}/{filename}", index_col = 'D A T E', parse_dates=True)

