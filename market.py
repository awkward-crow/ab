# market.py

from enum import Enum


class Market(Enum):
    Market_1 = 1
    Market_2 = 2


class MarketData:
    def __init__(self, period, prices):
        self.period = period
        self.prices = prices
    def __repr__(self):
        return f"MarketData({self.period}, {self.prices})"
    def price(self, market):
        if market == Market.Market_1:
            return self.prices[0]
        else:
            return self.prices[1]


def create_market_ticker(prices_1, prices_2):
    i1 = iter(prices_1)
    i2 = iter(prices_2)
    p = 0
    while True:
        try:
            yield MarketData(p, [next(i1), None])
            p += 1
            yield MarketData(p, [next(i1), next(i2)])
            p += 1
        except StopIteration:
            return

def read_prices(filename):
    with open(filename) as f:
        v = [float(line.strip()) for line in f if line.strip()]
    return v


def default_market_ticker():
    hourly = read_prices("data/hourly.txt")
    half_hourly = read_prices("data/half_hourly.txt")
    return create_market_ticker(half_hourly, hourly)



### end
