import pandas as pd
import yfinance as yfi
from yahoofinancials import YahooFinancials
import configparser
import os
import numpy as np
import quandl

sticker= 'NVDA'
yf = YahooFinancials(sticker)
data_d = yf.get_historical_price_data(start_date='2013-01-07', end_date='2023-03-30', time_interval='daily')
data_w = yfi.download(sticker, progress=True, interval='5d', start='2013-01-07', end='2023-03-30')
data_m = yf.get_historical_price_data(start_date='2013-01-07', end_date='2023-03-30', time_interval='monthly')
data_q = yfi.download(sticker, progress=True, interval='3mo', start='2013-01-07', end='2023-03-30')

data_d = pd.DataFrame(data_d[sticker]['prices'])
data_d = data_d.drop(['date', 'volume'], axis=1).set_index('formatted_date')
data_w = data_w.loc[:, ['Open', 'High', 'Low', 'Close', 'Adj Close']]
data_w.rename(columns = {'Adj Close':'adjclose'}, inplace=True)
data_w = data_w.dropna()
data_w.columns = map(str.lower, data_w.columns)
ts_days = pd.to_datetime(data_w.index.date)
bdays = pd.bdate_range(start=data_w.index[0].date(), end=data_w.index[-1].date())
data_w = data_w[ts_days.isin(bdays)]

data_m = pd.DataFrame(data_m[sticker]['prices'])
data_m = data_m.drop(['date', 'volume'], axis=1).set_index('formatted_date')
data_q=data_q.loc[:, ['Open', 'High', 'Low', 'Close', 'Adj Close']]
data_q.rename(columns={'Adj Close':'adjclose'}, inplace=True)
data_q = data_q.dropna()
data_q.columns = map(str.lower, data_q.columns)



from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
us_td = CustomBusinessDay(calendar=USFederalHolidayCalendar())