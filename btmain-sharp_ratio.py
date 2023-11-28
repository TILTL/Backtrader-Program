import datetime
import backtrader as bt
from trading_strategies import *
from risk_managment import *
from yahoo_fin.stock_info import get_data


# Instantiate Cerebro engine
cerebro = bt.Cerebro(optreturn=False)

# Arguments
Portfolios = ['tsla'] # Add more stocks in here
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
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
cerebro.optstrategy(MAcrossover, pfast=range(5, 20), pslow=range(50, 100))

# Set initial capital (Default: 10000)
cerebro.broker.setcash(10000)

# Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__':
    optimized_runs = cerebro.run()

    final_results_list = []
    for run in optimized_runs:
        for strategy in run:
            PnL = round(strategy.broker.get_value() - 10000,2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            final_results_list.append([strategy.params.pfast, 
                strategy.params.pslow, PnL, sharpe['sharperatio']])

    sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
                             reverse=True)
    for line in sort_by_sharpe[:5]:
        print(line)