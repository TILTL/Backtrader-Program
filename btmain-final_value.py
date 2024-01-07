import backtrader as bt
from trading_strategies import *
from risk_managment import *
from stock_analyzer import *
from yahoo_fin.stock_info import *


# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Arguments
Portfolios = ['tsla', 'msft', 'aapl'] # Add more stocks in here
start_date = "12/23/2022" # MM/DD/YYYY
end_date = "12/23/2023" # MM/DD/YYYY
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
cerebro.addstrategy(MAcrossover)

# Set initial capital (Default: 10000)
cerebro.broker.setcash(10000)

# Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__':
    start_portfolio_value = cerebro.broker.getvalue()
    
     # Run Cerebro Engine
    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')
    
    # cerebro.plot()
    



