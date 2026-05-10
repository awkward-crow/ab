# example.py

from battery import default_battery
from strategy import BandStrategy
from battery_operator import BatteryOperator
from market import default_market_ticker

low = 45
high = 50
trading_desk = BandStrategy(low, high)
operator = BatteryOperator(default_battery(), trading_desk)
operator.balance = 200

market_ticker = default_market_ticker()
for tick in market_ticker:
    operator.handle(tick)
    if operator.period >= 10:
        break

print(f"{'period':>8}  {'balance':>10}  {'charge':>10}")
for (period, balance), (_, charge, _) in zip(operator.trace, operator.battery.trace):
    print(f"{period:>8}  {balance:>10.2f}  {charge:>10.2f}")


### end
