import backtrader as bt
from trading_strategies import *
from risk_managment import *
from stock_analyzer import *
from yahoo_fin.stock_info import *

#Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Arguments
start_date = "01/01/2016" # MM/DD/YYYY
end_date = "10/30/2017" # MM/DD/YYYY
interval = "1d" # 1d, 1wk, 1mo

#Add data to Cerebro
instruments = ['TSLA', 'AAPL', 'GE', 'GRPN']
for ticker in instruments:
    data = bt.feeds.PandasData(
        dataname = get_data(ticker, 
                            start_date=start_date, 
                            end_date=end_date, 
                            index_as_date=True, 
                            interval=interval))
    cerebro.adddata(data, name=ticker) 

#Add analyzer for screener
cerebro.addanalyzer(Screener_SMA)

if __name__ == '__main__':
    #Run Cerebro Engine
    cerebro.run(runonce=False, stdstats=False, writer=True)