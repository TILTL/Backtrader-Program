import backtrader as bt

# class MyStrategy(bt.Strategy):
#     def next(self):
#         pass #Do something
        
class CPPI(bt.Strategy):
    params = (
        ('floor', 0.8),  # 80% of initial portfolio value
        ('multiplier', 3),  # CPPI multiplier
    )

    def __init__(self):
        self.initial_portfolio_value = self.broker.getvalue()
        self.floor_value = self.initial_portfolio_value * self.params.floor

    def next(self):
        total_value = self.broker.getvalue()
        cushion = max(total_value - self.floor_value, 0)
        risky_asset_allocation = self.params.multiplier * cushion
        risk_free_allocation = total_value - risky_asset_allocation

        # Assuming only one asset in the strategy for simplicity
        risky_asset = self.datas[0]
        current_position = self.getposition(risky_asset).size
        current_value = current_position * risky_asset.close[0]

        # Calculate the desired position size
        target_position_size = risky_asset_allocation / risky_asset.close[0]

        # Adjust the position
        self.order_target_size(data=risky_asset, target=target_position_size)
