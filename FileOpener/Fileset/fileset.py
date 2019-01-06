import xlwings as xl
import pandas as pd
import numpy as np

class Fileset:

    def __init__(self, file, path="Data"):

        self.path=path
        self.file=file
        self.fullpath=f"""{path}/{self.file}"""

    def file_open(self):
        
        wb=xl.Book(self.fullpath)
        return wb

class TimeSeriesFileset(Fileset):

    ## Frequency 
    ## Period
    @staticmethod
    def column_creator(x):

        ## x should be list object
        if len(x) < 1:
            raise Exception('length of list x should be more than 1')
        else: 
            return f"B8"

    def clear_sheet(self, sheets):

        for sheet in sheets:
            sheets[sheet.name].range('B8:XFD9').value = None
            sheets[sheet.name].range('A15').options(transpose=True).value = None
        
    def date_setting(self, sheets, st_date, ed_date, date_type):

        for sheet in sheets:
            sheets[sheet.name].range("B4").value = date_type
            sheets[sheet.name].range("B5").value = st_date
            sheets[sheet.name].range("B6").value = ed_date

    def column_setting(self, sheets, secs):

        ## XDF8 Hard Coding

        rng_cols = TimeSeriesFileset.column_creator(secs)

        for sheet in sheets:
            sheets[sheet.name].range("B8:XFD8").value = None
            sheets[sheet.name].range(rng_cols).value = secs

    def full_update_sheet(self, st_date, ed_date, secs, date_type = 'd'):

        ## 종목, Date 모두 업데이트

        wb = self.file_open()
        sheets = wb.sheets

        self.clear_sheet(sheets)
        self.date_setting(sheets, st_date, ed_date, date_type)
        self.column_setting(sheets, secs)

        mac = wb.macro("Refresh_Button")
        mac()
        
        wb.save(self.fullpath)

    def column_update_sheet(self, secs):

        ## 종목 업데이트만 필요할 떄

        wb = self.file_open()
        sheets = wb.sheets

        self.clear_sheet(sheets)
        self.column_setting(sheets, secs)

        mac = wb.macro("Refresh_Button")
        mac()
        
        wb.save(self.fullpath)        

    def frequency_update(self, st_date, ed_date, date_type='D'):

        ## Date Change만 필요할 때

        wb = self.file_open()
        sheets = wb.sheets

        self.clear_sheet(sheets)
        self.date_setting(sheets, st_date, ed_date, date_type)

        mac = wb.macro("Refresh_Button")
        mac()
        
        wb.save(self.fullpath)

class FinancialDataSet(Fileset):

    ## C9: XFD10 = None
    ## A14: A14

    def clear_sheet(self, sheets, options=0):

        if options == 0:

            for sheet in sheets:
                sheets[sheet.name].range('C9:XFD40000').value = None
                sheets[sheet.name].range('A14:B40000').value = None
        
        elif options == 1:

            for sheet in sheets:
                sheets[sheet.name].range('C9:XFD40000').value = None

        elif options == 2:

            for sheet in sheets:
                sheets[sheet.name].range('A14:B40000').value = None

    def column_setting(self, sheets, account, period):

        len_period = len(period)
        rp_account = account.repeat(len_period)
        
        for sheet in sheets:
            sheets[sheet.name].range("C9").value = rp_account
            sheets[sheet.name].range("C10").value = period

    def company_code(self, sheets, comp_code):

        for sheet in sheets:
            sheets[sheet.name].range(f"A14:A16").options(transpose=True).value = comp_code

    def column_update(self, account, period, options=1):

        wb = self.file_open()
        sheets = wb.sheets

        self.clear_sheet(sheets, options=options)
        self.column_setting(sheets, account, period)

        mac = wb.macro("Refresh_Button")
        mac()
        
        wb.save(self.fullpath)

    def company_update(self, account, period, options=2):

        wb = self.file_open()
        sheets = wb.sheets

        self.clear_sheet(sheets, options=options)
        self.company_code(account, period)

        mac = wb.macro("Refresh_Button")
        mac()
        
        wb.save(self.fullpath)