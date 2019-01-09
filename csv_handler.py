## Batch
import pandas as pd
from FileOpener.DataOpener.DataOpener import PriceDataOpener, FinancialDataOpener, StockInfoDataOpener, MarketCapOpener, TimeSeriesMapOpener, StockInfoDataOpener
from FileOpener.Fileset.fileset import TimeSeriesFileset, FinancialDataSet

## All file to csv
## Upload the file then append it to csv

class PriceCSVSaver(PriceDataOpener):

    def __init__(self, file, dir='Data'):

        super().__init__(file, dir=dir)
        self.open, self.high, self.close, self.low = super().olhc()

    def saver(self, filename, dir):

        self.open.to_csv(f"{dir}/{filename}_open.csv")
        self.high.to_csv(f"{dir}/{filename}_high.csv")
        self.close.to_csv(f"{dir}/{filename}_close.csv")
        self.low.to_csv(f"{dir}/{filename}_low.csv")
        ## 실험해보기
        (self.close.isnull()).to_csv(f"{dir}/{filename}_listed_or_not.csv")

class MarketCapSaver(MarketCapOpener):

    def __init__(self, file, dir='Data'):

        super().__init__(file, dir=dir)
        self.data = super().mkc_opener()

    def saver(self, filename, dir):

        for key in self.data.keys():
            self.data[key].to_csv(f"{dir}/{filename}_{key}.csv")

class TimeMapSaver(TimeSeriesMapOpener):

    def __init__(self, file, dir='Data', sheetnames=['KSE', 'KDQ']):

        super().__init__( file, dir=dir)
        self.sheetnames = sheetnames
        self.data = super().map_opener(self.sheetnames)

    def saver(self, filename, dir):

        for key in self.data.keys():
            self.data[key].to_csv(f"{dir}/{filename}_{key}.csv")

class StockInfoSaver(StockInfoDataOpener):

    def __init__(self, file, dir='Data', sheetnames=['KSE', 'KDQ']):

        super().__init__( file, dir=dir)
        self.sheetnames = sheetnames
        self.data = super().info_data_open(self.sheetnames)

    def saver(self, filename, dir):

        for key in self.data.keys():
            self.data[key].to_csv(f"{dir}/{filename}_{key}.csv")

class FinancialCSVSaver(FinancialDataOpener):

    def __init__(self, file, dir='Data'):

        super().__init__(file, dir=dir)
        self.data = super().fin_data_open()

    def saver(self, filename, dir):

        for key in self.data.keys():
            self.data[key].to_csv(f"{dir}/{filename}_{key}.csv")

class FinancialUploader:

    def __init__(self, file, dir='Data'):

        self.file = file
        self.dir = dir

    ## 영업이익 / 매출액의 코드
    ## 기간 코드
        ## 분기: YYYY1Q / YYYY2Q / YYYY3Q / YYYY4Q 
        ## 연간: YYYYAS

    def start_to_end(self, st_year, ed_year, option='Q'):

        pass
        ## If option is Q
        ## If option is         

def priceUploader(excel_filename, upload_filename, dir, st_date, ed_date):

    ## upload_filename = name before close
    TimeSeriesFileset(excel_filename).frequency_update(st_date, ed_date)
    price_open, price_high, price_close, price_low = PriceDataOpener(excel_filename).olhc()

    price_types = ['open', 'high', 'close', 'low']

    for price, price_type in zip([price_open, price_high, price_close, price_low], price_types):
        temp = pd.read_csv(f"{dir}/{upload_filename}_{price_type}.csv")
        temp = pd.concat([temp, price], axis = 0)
        temp.to_csv(f"{dir}/{upload_filename}_{price_type}.csv")


# FinancialCSVSaver('KOSDAQ_KOSPI_ISSUE_STOCK.xlsm').saver('ISSUE_STOCK', 'CSVFile/FinancialData/Korea')