from FileOpener.Fileset import fileset as fl
from FileOpener.DataOpener.DataOpener import MarketCapOpener

Mkt_Cap = fl.Fileset('MarketCap1.xlsm',)

# Mkt_Cap.update('20171201','20180228')

## Not Pythonic! I know!!

dt_set = [['20161201','20170228'], 
          ['20151201','20160229'], 
          ['20141201','20150228'],
          ['20131201','20140228'],
          ['20121201','20130228'],
          ['20111201','20120229'],
          ['20101201','20110228'],
          ['20091201','20100228'],
          ['20081201','20090228'],
          ['20071201','20080229'],
          ['20061201','20070228'],
          ['20051201','20060228'],
          ['20041201','20050228'], 
          ['20031201','20040229'],
          ['20021201','20030228'],
          ['20011201','20020228'],
          ['20001201','20010228'],
          ['19991201','20000229']]

for dt in dt_set:

    Mkt_Cap.update(dt[0],dt[1])
    MarketCapOpener('MarketCap1.xlsm').market_cap_opener()