import backtrader as bt
from trading_strategies import *
from risk_managment import *
from stock_analyzer import *
from yahoo_fin.stock_info import get_data

amazon_weekly= get_data("tsla", start_date="01/01/2022", end_date="11/01/2023", index_as_date = True, interval="1d")
amazon_weekly