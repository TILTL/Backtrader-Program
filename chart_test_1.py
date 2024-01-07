import backtrader as bt
from yahoo_fin.stock_info import *


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

data2 = bt.feeds.PandasData(
        # Get data by using the Yahoo_fin api
        dataname = get_data('AAPL',
                            start_date=start_date,
                            end_date=end_date,
                            index_as_date=True,
                            interval=interval)
    )

data2.compensate(data1)  # let the system know ops on data1 affect data0
data2.plotinfo.plotmaster = data1
data2.plotinfo.sameaxis = True
cerebro.adddata(data2, name='AAPL')

# Run Cerebro Engine
cerebro.run()
cerebro.plot()