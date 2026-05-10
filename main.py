# main.py

import argparse
from battery import default_battery
from strategy import BandStrategy
from battery_operator import BatteryOperator
from market import default_market_ticker


parser = argparse.ArgumentParser()
parser.add_argument("--plot", action="store_true")
parser.add_argument("--n", type=int, default=100)
args = parser.parse_args()

low = 45
high = 50
trading_desk = BandStrategy(low, high)
operator = BatteryOperator(default_battery(), trading_desk)
operator.balance = 200

market_ticker = default_market_ticker()
for tick in market_ticker:
    operator.handle(tick)

if args.plot:
    import plotly.express as px

    ts, balances = zip(*operator.trace[:args.n])
    fig = px.line(x=ts, y=balances, labels={"x": "period", "y": "balance"})
    fig.show(renderer="browser")

    bt, charges, _ = zip(*operator.battery.trace[:args.n])
    fig = px.line(x=bt, y=charges, labels={"x": "t", "y": "charge"})
    fig.show(renderer="browser")



### end
