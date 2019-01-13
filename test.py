import pandas as pd
import numpy as np
import swifter
from FileOpener.CSVReader.CSVReader import CSVReader as csv
from multiprocessing import cpu_count, Pool
 

directory = 'CSVFile/Price/Korea/Stocks'
kse_file = 'KOSPI_FROM_1998_close.csv'
kdq_file = 'KOSDAQ_FROM_1998_close.csv'

<<<<<<< HEAD
kse_price = csv.price_reader(kse_file, directory)
kdq_price = csv.price_reader(kdq_file, directory)

kse_rt = kse_price.div(kse_price.shift(1))
kdq_rt = kdq_price.div(kdq_price.shift(1))


roll_prod = lambda x: np.prod(x)

def rolling_return(data):

    return data.swifter.rolling(30).apply(roll_prod, raw=False)

print(rolling_return(kse_rt))




#     with mp.Pool(processes=4) as pool:

#         pool.apply_async(rolling_return, args=(kse_rt, 30))
#         pool.close()
#         pool.join()        
        
=======


# test = pd.read_csv(f"{directory}/{filename}", skiprows = 1)
>>>>>>> 952f0fb223632885a9d1572cb61184dbac5502e5

