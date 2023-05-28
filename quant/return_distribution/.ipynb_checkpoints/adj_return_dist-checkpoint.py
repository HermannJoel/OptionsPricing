import pandas as pd
import yfinance as yf
import configparser
import os
import numpy as np
import quandl
from functions import read_data
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas_datareader as pdr
import investy


# Load Config
config_file = os.path.join(os.path.dirname("__file__"), 'Config/config.ini')
config = configparser.ConfigParser()
config.read(config_file)

nasdaq_api_key=os.path.join(os.path.dirname("__file__"), config['keys']['nasdaq_api_key'])
quandl_api_key=os.path.join(os.path.dirname("__file__"), config['keys']['quandl_api_key'])
tiingo_api_key=os.path.join(os.path.dirname("__file__"), config['keys']['tiingo_api_key'])
alpha_vantage_api_key=os.path.join(os.path.dirname("__file__"), config['keys']['alpha_vantage_api_key'])


#download data from investy
df = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')

#download data from alpha_vantage

crypto_api=CryptoCurrencies(key=ALPHA_VANTAGE_API_KEY,
output_format= "pandas")

data, meta_data = crypto_api.get_digital_currency_daily(
symbol="BTC",
market="EUR"
)

#download data from tiingo.
intrinio_sdk.ApiClient().configuration.api_key['api_key']='{tiingo_api_key}'
security_api = intrinio_sdk.SecurityApi()
eurusd = pdr.get_data_tiingo("eurusd", 
                             start=start_date, 
                             end=end_date, 
                             freq='daily',
                             api_key = auth_key)
r=security_api.get_security_stock_prices(identifier='AAPL', 
                                           start_date='2000-01-01', 
                                           end_date='2010-12-31', 
                                           frequency='daily', 
                                           page_size=10000)
df=(pd.DataFrame(r.stock_prices_dict)
      .sort_values("date")
      .set_index("date")
)

response_list=[x.to_dict() for x in r.stock_prices]
df_intrinio=pd.DataFrame(response_list).sort_values('date')
df_intrinio.set_index('date', inplace=True)

download data from yahoo.
df=yf.download("TSLA", 
                  start="2013-01-01", 
                  end="2023-01-01",
                  progress=True)

download data from nasdaq
df=nasdaqdatalink.get(dataset="WIKI/MSFT",
                       start_date="2012-01-01", 
                       end_date="2022-12-31")

stock_data=read_data(sticker='SPY', start='2012-12-31', end='2022-12-31')
stock_data.tail()

import pandas_datareader.data as getData
from matplotlib.pyplot import *
from matplotlib.finance import quotes_historical_yaho
import matplotlib.mlab as mlab

ticker='IBM'
begdate=(2015,1,1)
enddate=(2015,11,9)
p = getData(ticker, begdate, enddate, asobject=True, a
ret = (p.aclose[1:] - p.aclose[:-1])/p.aclose[:1]
[n,bins,patches] = hist(ret, 100)
mu = np.mean(ret)
sigma = np.std(ret)
x = mlab.normpdf(bins, mu, sigma)
plot(bins, x, color='red', lw=2)
title("IBM return distribution")
xlabel("Returns")
ylabel("Frequency")
show()
            

import pandas as pd
import yfinance as yf
import numpy as np
import quandl

# Read Data from the Web
def read_data(sticker, start, end):
    ''' Reads historical data from Yahoo! Finance, calculates log returns, simple returns using  
        close-close, hight-low, open-close.
    '''
    #valid periods=1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    #intervals=1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    data=yf.download(sticker, start, end, progress=True, interval='1mo')
    data=data.loc[:, ['Open', 'High', 'Low', 'Close', 'Adj Close']]
    data.rename(columns={'Adj Close':'Adj_close'}, inplace=True)
    #simple returns
    data['c-c_sple_rtn']=(data.Adj_close/data.Adj_close.shift(1))-1
    data['h-l_sple_rtn']=(data.High-data.Low)/data.Low
    data['o-c_sple_rtn']=(data.Close/data.Open)/data.Open
    #log returns
    data['c-c_log_rtn']=np.log(data.Adj_close/data.Adj_close.shift(1))
    data['h-l_log_rtn']=np.log(data.High/data.Low.shift(1))
    data['o-c_log_rtn']=np.log(data.Close/data.Open.shift(1))
    #
    df_all_dates=pd.DataFrame(index=pd.date_range(start,end))
    data=df_all_dates.join(data.loc[:,:], how='left').fillna(method='ffill').asfreq('M')
    #reads cpi data from quandl
    data_cpi=quandl.get(dataset='RATEINF/CPI_USA',
    start_date=start,
    end_date=end)
    data_cpi.rename(columns={'Value':'cpi'}, inplace=True)
    data_m=data.join(data_cpi, how='left')
    data_m['inflation_rate']=data_m.cpi.pct_change()
    #adjusted close-adjusted close simple real return
    data_m['c-c_sple_real_rtn']=(data_m['c-c_sple_rtn'] + 1) / (data_m['inflation_rate'] + 1) - 1
    #high-low simple real return
    data_m['h-l_sple_real_rtn']=(data_m['h-l_sple_rtn'] + 1) / (data_m['inflation_rate'] + 1) - 1
    #open-close simple real return
    data_m['o-c_sple_real_rtn']=(data_m['o-c_sple_rtn'] + 1) / (data_m['inflation_rate'] + 1) - 1
    data_m=data_m.dropna()
    
    return data_m