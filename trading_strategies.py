import backtrader as bt

# class MyStrategy(bt.Strategy):
#     def next(self):
#         pass #Do something


class PrintClose(bt.Strategy):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} {txt}")  # Print date and close

    def next(self):
        self.log(f"Close: {self.dataclose[0]}")


class PrintDataNames(bt.Strategy):
    def start(self):
        # Print the names of all data feeds
        data_names = self.getdatanames()
        for name in data_names:
            print(f"Stock Name: {name}")


class MAcrossover(bt.Strategy):
    # Moving average parameters
    params = (
        ("pfast", 20),
        ("pslow", 50),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} {txt}")  # Comment this line when running optimization

    def __init__(self):
        self.dataclose = self.datas[0].close

        # Order variable will contain ongoing order details/status
        self.order = None

        # Instantiate MA
        self.slow_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.pslow
        )
        self.fast_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.pfast
        )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price:.2f}")
            elif order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price:.2f}")
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # Reset orders
        self.order = None

    def next(self):
        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades

            # If the 20 SMA is above the 50 SMA
            if (
                self.fast_sma[0] > self.slow_sma[0]
                and self.fast_sma[-1] < self.slow_sma[-1]
            ):
                self.log(f"BUY CREATE {self.dataclose[0]:2f}")
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            # Otherwise if the 20 SMA is below the 50 SMA
            elif (
                self.fast_sma[0] < self.slow_sma[0]
                and self.fast_sma[-1] > self.slow_sma[-1]
            ):
                self.log(f"SELL CREATE {self.dataclose[0]:2f}")
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f"CLOSE CREATE {self.dataclose[0]:2f}")
                self.order = self.close()


class AverageTrueRange(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} {txt}")  # Print date and close

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

    def next(self):
        range_total = 0
        for i in range(-13, 1):
            true_range = self.datahigh[i] - self.datalow[i]
            range_total += true_range
        ATR = range_total / 14

        self.log(f"Close: {self.dataclose[0]:.2f}, ATR: {ATR:.4f}")


class BtcSentiment(bt.Strategy):
    params = (('period', 10), ('devfactor', 1),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.btc_price = self.datas[0].close
        self.google_sentiment = self.datas[1].close
        self.bbands = bt.indicators.BollingerBands(self.google_sentiment,
                period=self.params.period, devfactor=self.params.devfactor)

        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Existing order - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
                elif order.issell():
                    self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
                self.bar_executed = len(self)

            elif order.status in [order.Canceled, order.Margin, 
                                order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def next(self):
        # Check for open orders
        if self.order:
            return

        #Long signal 
        if self.google_sentiment > self.bbands.lines.top[0]:
            # Check if we are in the market
            if not self.position:
                self.log(f'Google Sentiment Value: {self.google_sentiment[0]:.2f}')
                self.log(f'Top band: {self.bbands.lines.top[0]:.2f}')
                # We are not in the market, we will open a trade
                self.log(f'***BUY CREATE {self.btc_price[0]:.2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()       

        #Short signal
        elif self.google_sentiment < self.bbands.lines.bot[0]:
            # Check if we are in the market
            if not self.position:
                self.log(f'Google Sentiment Value: {self.google_sentiment[0]:.2f}')
                self.log(f'Bottom band: {self.bbands.lines.bot[0]:.2f}')
                # We are not in the market, we will open a trade
                self.log(f'***SELL CREATE {self.btc_price[0]:.2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        
        #Neutral signal - close any open trades     
        else:
            if self.position:
                # We are in the market, we will close the existing trade
                self.log(f'Google Sentiment Value: {self.google_sentiment[0]:.2f}')
                self.log(f'Bottom band: {self.bbands.lines.bot[0]:.2f}')
                self.log(f'Top band: {self.bbands.lines.top[0]:.2f}')
                self.log(f'CLOSE CREATE {self.btc_price[0]:.2f}')
                self.order = self.close()


class MyStrategy(bt.Strategy):
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price:.2f}")
            elif order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price:.2f}")
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # Reset orders
        self.order = None
        
    def next(self):
        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades

            # If the 20 SMA is above the 50 SMA
            if (
                self.fast_sma[0] > self.slow_sma[0]
                and self.fast_sma[-1] < self.slow_sma[-1]
            ):
                self.log(f"BUY CREATE {self.dataclose[0]:2f}")
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            # Otherwise if the 20 SMA is below the 50 SMA
            elif (
                self.fast_sma[0] < self.slow_sma[0]
                and self.fast_sma[-1] > self.slow_sma[-1]
            ):
                self.log(f"SELL CREATE {self.dataclose[0]:2f}")
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f"CLOSE CREATE {self.dataclose[0]:2f}")
                self.order = self.close()
