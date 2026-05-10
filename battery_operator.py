# battery_operator.py

from contract import is_discharging
from strategy import BandStrategy
from constants import PERIOD_HOURS

## the time unit of BatteryOperator is a period of 30 minutes

class BatteryOperator:
    def __init__(self, battery, desk):
        self.battery = battery
        self.desk = desk
        self.contracts = []
        self.period = 0
        self.balance = 0
        self.completed_contracts = []
        self.trace = []
    def handle(self, tick):
        if self.period != tick.period:
            return False
        if not self.contracts:
            self.battery.idle(PERIOD_HOURS)
        else:
            r = sum([k.transaction(self.period).rate for k in self.contracts])
            if is_discharging(self.contracts):
                self.battery.discharge(PERIOD_HOURS, r)
            else:
                self.battery.charge(PERIOD_HOURS, r)
        self.update_balance(tick)
        self.completed_contracts.extend([k for k in self.contracts if k.is_complete(self.period)])
        self.contracts = [k for k in self.contracts if not k.is_complete(self.period)]
        self.period += 1
        new_contracts = self.desk.trade(self.period, tick, self.contracts, self.battery)
        self.contracts.extend(new_contracts)
        return self.balance
    def update_balance(self, tick):
        for k in self.contracts:
            if k.is_complete(self.period):
                self.balance += (PERIOD_HOURS) * sum(x.rate for x in k.transactions) * tick.price(k.market)
        self.trace.append((self.period, self.balance))
        return self.balance


### end
