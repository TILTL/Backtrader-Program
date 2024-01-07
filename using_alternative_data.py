import backtrader as bt
from yahoo_fin.stock_info import *
from trading_strategies import *
import pandas as pd
import quantstats


# Instantiate Cerebro engine
cerebro = bt.Cerebro(stdstats=False)

cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

# Argumentspip install quantstats
start_date = "01/01/2022" # MM/DD/YYYY
end_date = "01/01/2023" # MM/DD/YYYY
interval = "1d" # 1d, 1wk, 1mo

# Set data parameters and add to Cerebro
data1 = bt.feeds.PandasData(
        # Get data by using the Yahoo_fin api
        dataname = get_data('btc',
                            start_date=start_date, 
                            end_date=end_date, 
                            index_as_date=True, 
                            interval=interval)
    )
cerebro.adddata(data1, name='BTC')

data2 = bt.feeds.GenericCSVData(
    dataname='/Users/harryg/Desktop/QUANT/backtrader/BTC_Gtrends.csv',
    fromdate=datetime.datetime(2018, 1, 1),
    todate=datetime.datetime(2020, 1, 1),
    nullvalue=0.0,
    dtformat=('%Y-%m-%d'),
    datetime=0,
    time=-1,
    high=-1,
    low=-1,
    open=-1,
    close=1,
    volume=-1,
    openinterest=-1,
    timeframe=bt.TimeFrame.Weeks)
cerebro.adddata(data2, name='BTC_Gtrends')

cerebro.addstrategy(BtcSentiment)

# Run Cerebro Engine
results = cerebro.run()
strat = results[0]

portfolio_stats = strat.analyzers.getbyname('PyFolio')
returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
returns.index = returns.index.tz_convert(None)

quantstats.reports.html(returns, output='stats.html', title='BTC Sentiment')
cerebro.addwriter(bt.WriterFile, csv=True, out='log.csv')
