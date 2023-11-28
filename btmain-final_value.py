import datetime
import backtrader as bt
from trading_strategies import *
from risk_managment import *
from yahoo_fin.stock_info import get_data


# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Arguments
Portfolios = ['tsla', 'msft', 'aapl'] # Add more stocks in here
start_date = "01/01/2020" # MM/DD/YYYY
end_date = "12/31/2021" # MM/DD/YYYY
interval = "1d" # 1d, 1wk, 1mo

# Set data parameters and add to Cerebro
# Loop through the stock symbols and add data to Cerebro
for stock in Portfolios:
    data = bt.feeds.PandasData(
        # Get data by using the Yahoo_fin api
        dataname = get_data(stock, 
                            start_date=start_date, 
                            end_date=end_date, 
                            index_as_date=True, 
                            interval=interval)
    )
    # Store data into cerebro
    cerebro.adddata(data, name=stock)

# Add strategy to Cerebro
cerebro.addstrategy(PrintDataNames)

# Set initial capital (Default: 10000)
cerebro.broker.setcash(10000)

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
    



