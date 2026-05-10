# contract.py

class Transaction:
    def __init__(self, period, rate):
        self.period = period
        self.rate = rate
    def __repr__(self):
        return f"Transaction({self.period}, {self.rate})"
    def is_charging(self):
        return self.rate < 0
    def is_discharging(self):
        return self.rate > 0


class Contract:
    def __init__(self, start, transactions, market):
        self.period0 = start
        self.transactions = transactions
        self.market = market
    def __repr__(self):
        return f"Contract({self.period0}, {self.transactions}, {self.market})"
    def is_charging(self):
        return self.transactions and self.transactions[0].is_charging()
    def is_discharging(self):
        return self.transactions and self.transactions[0].is_discharging()
    def transaction(self, p):
        return self.transactions[p - self.period0]
    def is_complete(self, p):
        return p == self.period0 + len(self.transactions) - 1


def is_charging(contracts):
    return bool(contracts and contracts[0].is_charging())

def is_discharging(contracts):
    return bool(contracts and contracts[0].is_discharging())


def total_committed(p, contracts):
    return sum(k.transaction(p).rate for k in contracts)


### end
