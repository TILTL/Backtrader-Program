import backtrader as bt
from yahoo_fin.stock_info import *
from trading_strategies import *


#simple moving average
class SimpleMA(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data, period=20, 
                plotname="20 SMA")

#Instantiate Cerebro engine
cerebro = bt.Cerebro(stdstats=False)

# Arguments
start_date = "01/01/2022" # MM/DD/YYYY
end_date = "01/01/2023" # MM/DD/YYYY
interval = "1d" # 1d, 1wk, 1mo

#Set data parameters and add to Cerebro
data1 = bt.feeds.PandasData(
        # Get data by using the Yahoo_fin api
        dataname = get_data('TSLA',
                            start_date=start_date, 
                            end_date=end_date, 
                            index_as_date=True, 
                            interval=interval)
    )
cerebro.adddata(data1, name='TSLA')

cerebro.addstrategy(BtcSentiment)
#Run Cerebro Engine
cerebro.run()
cerebro.plot()