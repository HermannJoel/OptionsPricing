import pandas as pd
import yfinance as yfi
from yahoofinancials import YahooFinancials
import configparser
import os
import numpy as np
#import quandl


# Read Data from the Web
def read_stocks_data(sticker, start_date, end_date, **kwargs):
    """ Reads historical data from Yahoo Finance, calculates log returns, simple returns using  
        close-close, hight-low, open-close.
    parameters
    ==========
    sticker (str) :
        target folder path
    start (str) :
        start date        
    end (str) : 
        end date   
    example
    =======
    Load(dest_dir=dest_dir, src_flow=read_data(sticker='nvda', start='2013-03-30', end='2023-03-30'), file_name='nvda-returns', file_extension='xlsx')
    >>> to load compute return of nvda as  in dest_dir as .xlsx file
    """
    try:
        yf = YahooFinancials(sticker)
        data_d = yf.get_historical_price_data(start_date, end_date, time_interval='daily')
        data_w = yf.get_historical_price_data(start_date, end_date, time_interval='weekly')
        #data_w = yfi.download(sticker, progress=True, interval='5d', **kwargs)
        data_m = yf.get_historical_price_data(start_date, end_date, time_interval='monthly')
        data_q = yfi.download(sticker, progress=True, interval='3mo', **kwargs)
        #daily data
        data_d = pd.DataFrame(data_d[sticker]['prices'])
        data_d = data_d.drop(['date', 'volume'], axis=1).set_index('formatted_date')
        #weekly data
        data_w = pd.DataFrame(data_w[sticker]['prices'])
        data_w = data_w.drop(['date', 'volume'], axis=1).set_index('formatted_date')
        #data_w = data_w.loc[:, ['Open', 'High', 'Low', 'Close', 'Adj Close']]
        #data_w.rename(columns = {'Adj Close':'adjclose'}, inplace=True)
        #data_w = data_w.dropna()
        #data_w.columns = map(str.lower, data_w.columns)
        #ts_days = pd.to_datetime(data_w.index.date)
        #bdays = pd.bdate_range(start=data_w.index[0].date(), end=data_w.index[-1].date())
        #data_w = data_w[ts_days.isin(bdays)]
        #data_w = data_w.dropna()
        #monthly data
        data_m = pd.DataFrame(data_m[sticker]['prices'])
        data_m = data_m.drop(['date', 'volume'], axis=1).set_index('formatted_date')
        #quarterly data
        data_q=data_q.loc[:, ['Open', 'High', 'Low', 'Close', 'Adj Close']]
        data_q.rename(columns={'Adj Close':'adjclose'}, inplace=True)
        data_q = data_q.dropna()
        data_q.columns = map(str.lower, data_q.columns)
        #sort index
        data_d.sort_index(axis=0, ascending=True, inplace=True)
        data_w.sort_index(axis=0, ascending=True, inplace=True)
        data_m.sort_index(axis=0, ascending=True, inplace=True)
        data_q.sort_index(axis=0, ascending=True, inplace=True)
        
        #simple daily returns
        data_d['c-c_sple_returns']=((data_d.adjclose/data_d.adjclose.shift(1))-1)*100
        data_d['h-l_sple_returns']=((data_d.high-data_d.low)/data_d.low)*100
        data_d['o-c_sple_returns']=((data_d.close/data_d.open)/data_d.open)*100
        #log daily returns
        data_d['c-c_log_returns']=(np.log(data_d.adjclose/data_d.adjclose.shift(1)))*100
        #data_d['h-l_log_rtn']=(np.log(data_d.high/data_d.low.shift(1)))*100
        #data_d['o-c_log_rtn']=(np.log(data_d.close/data_d.open.shift(1)))*100
        
        #simple weekly returns
        data_w['c-c_sple_returns']=((data_w.adjclose/data_w.adjclose.shift(1))-1)*100
        data_w['h-l_sple_returns']=((data_w.high-data_w.low)/data_w.low)*100
        #log weekly returns
        data_w['c-c_log_returns']=(np.log(data_w.adjclose/data_w.adjclose.shift(1)))*100

        #simple monthly returns 
        data_m['c-c_sple_returns']=((data_m.adjclose/data_m.adjclose.shift(1))-1)*100
        data_m['h-l_sple_returns']=((data_m.high-data_m.low)/data_m.low)*100
        #log monthly  returns
        data_m['c-c_log_returns']=(np.log(data_m.adjclose/data_m.adjclose.shift(1)))*100

        #simple quarterly returns
        data_q['c-c_sple_returns']=((data_q.adjclose/data_q.adjclose.shift(1))-1)*100
        data_q['h-l_sple_returns']=((data_q.high-data_q.low)/data_q.low)*100
        #log quarterly returns
        data_q['c-c_log_returns']=(np.log(data_q.adjclose/data_q.adjclose.shift(1)))*100

        
        return data_d, data_w, data_m, data_q
    except Exception as e:
        print("data read error!: "+str(e))

data_d, data_w, data_m, data_q = read_data(sticker='AAPL', start_date='1980-12-31', end_date='2020-11-06')


def load_as_excel_file(dest_dir, sticker, daily_data, weekly_data, monthly_data, quarterly_data, file_name, file_extension):
    """Function to load data as excle file     
    parameters
    ==========
    dest_dir (str) :
        target folder path
    src_flow (DataFrame) :
        data frame returned by transform function        
    file_name (str) : 
        destination file name
    exemple
    =======
    load_as_excel_file(dest_dir, template_asset_without_prod, 'template_asset', '.csv')
    >>> to load template_asset_without_prod in dest_dir as template_asset.csv 
    """
    try:
        if file_extension in ['.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt']:
            writer = pd.ExcelWriter(dest_dir+file_name+file_extension, engine='xlsxwriter')
            daily_data.to_excel(writer, sheet_name=f'{sticker}_dayly_dor', float_format='%.4f', index=True)
            weekly_data.to_excel(writer, sheet_name=f'{sticker}_weekly_dor', float_format='%.4f', index=True)
            monthly_data.to_excel(writer, sheet_name=f'{sticker}_monthly_dor', float_format='%.4f', index=True)
            quarterly_data.to_excel(writer, sheet_name=f'{sticker}_quarterly_dor', float_format='%.4f', index=True)
            writer.save()
            print(f"Data loaded in {dest_dir} as {file_name}.{file_extension} succesfully!")
        else: 
            raise ValueError("Invalid extension type. Choose either '.xslx' or '.xls'")
    except Exception as e:
        print('Data load error!: '+str(e))

        
data_d, data_w, data_m, data_q = read_stocks_data(sticker='AAPL', start_date='1980-12-31', end_date='2020-11-06')
load_as_excel_file(dest_dir='D:/local-repo-github/OptionsPricing/quant/storage_files/' , sticker='aapl', daily_data = data_d, weekly_data = data_w, monthly_data = data_m, quarterly_data = data_q, file_name = 'aapl-returns', file_extension='.xlsx')


