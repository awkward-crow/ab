# battery.py

## the time unit for B is hours

## consider using a builder to instantiate a Battery

class Battery:
    def __init__(self, storage_volume, charging_rate, discharging_rate, charging_efficiency, discharging_efficiency, degradation):
        self.storage_volume = storage_volume        # MWh
        self.charging_rate = charging_rate          # MW
        self.discharging_rate = discharging_rate    # MW
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency
        self.degradation = degradation
        self.current_charge = 0     # MWh
        self.cycles = 0
        self.cycle_discharge = 0
        self.t = 0
        self.age = 0        # hours
        self.trace = []
    def update_trace(self):
        self.trace.append((self.t, self.current_charge, self.current_volume()))
    def current_volume(self):
        return self.storage_volume * ((1 - self.degradation) ** self.cycles)
    def idle(self, delta_t):
        # does the charge run down over time?
        self.t += delta_t
        self.update_trace()
    def charge(self, delta_t, r):
        self.current_charge -= delta_t * r * (1 - self.charging_efficiency)
        self.t += delta_t
        self.update_trace()
        return r
    def discharge(self, delta_t, r):
        c = (delta_t * r) / (1 - self.discharging_efficiency)
        self.cycle_discharge += c
        if self.cycle_discharge > self.current_volume():
            self.cycle_discharge -= self.current_volume()
            self.cycles += 1
        self.current_charge -= c
        self.t += delta_t
        self.update_trace()
        return r
    def charging_capacity(self, t):
        return -min(self.charging_rate, (self.current_volume() - self.current_charge) / (t * (1 - self.charging_efficiency)))
    def discharging_capacity(self, t):
        return min(self.discharging_rate, (1 - self.discharging_efficiency) * self.current_charge / t )
        

def default_battery():
    return Battery(4, 2, 2, 0.05, 0.05, 0.001 / 100)



### end
