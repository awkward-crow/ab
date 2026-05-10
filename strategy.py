# strategy.py

from market import Market
from contract import Contract, Transaction, is_charging, is_discharging, total_committed
from constants import PERIOD_HOURS

class BandStrategy:
    def __init__(self, low, high):
        self.low = low
        self.high = high
    def trade(self, p, tick, current_contracts, battery):
        price_2 = tick.price(Market.Market_2)
        price_1 = tick.price(Market.Market_1)
        if not is_charging(current_contracts):
            if price_2 and price_2 > self.high:
                capacity = battery.discharging_capacity(2 * PERIOD_HOURS)
                committed_p = total_committed(p, current_contracts)
                committed_p1 = total_committed(p + 1, current_contracts)
                if capacity - committed_p > 0 and capacity - committed_p1 > 0:
                    return [Contract(p, [Transaction(p, capacity - committed_p), Transaction(p + 1, capacity - committed_p1)], Market.Market_2)]
            elif price_1 and price_1 > self.high:
                capacity = battery.discharging_capacity(PERIOD_HOURS)
                committed = total_committed(p, current_contracts)
                if capacity - committed > 0:
                    return [Contract(p, [Transaction(p, capacity - committed)], Market.Market_1)]
        if not is_discharging(current_contracts):
            if price_2 and price_2 < self.low:
                capacity = battery.charging_capacity(2 * PERIOD_HOURS)
                committed_p = total_committed(p, current_contracts)
                committed_p1 = total_committed(p + 1, current_contracts)
                if capacity - committed_p < 0 and capacity - committed_p1 < 0:
                    return [Contract(p, [Transaction(p, capacity - committed_p), Transaction(p + 1, capacity - committed_p1)], Market.Market_2)]
            elif price_1 and price_1 < self.low:
                capacity = battery.charging_capacity(PERIOD_HOURS)
                committed = total_committed(p, current_contracts)
                if capacity - committed < 0:
                    return [Contract(p, [Transaction(p, capacity - committed)], Market.Market_1)]
        return []

### end
