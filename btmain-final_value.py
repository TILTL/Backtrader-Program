import datetime
import backtrader as bt
from strategies import *
from risk_management import *
from yahoo_fin.stock_info import get_data

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Set data parameters and add to Cerebro
data = bt.feeds.PandasData(
    # Call Yahoo_fin and get corresponding data
    dataname = get_data('tsla', 
                        start_date = "01/01/2020", 
                        end_date = "12/31/2021", 
                        index_as_date = True, 
                        interval = "1d")
    )

cerebro.adddata(data)

# Add strategy to Cerebro
cerebro.addstrategy(MAcrossover)

# Set initial capital
cerebro.broker.setcash(1)

# Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__':
    # Run Cerebro Engine
    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')
    



