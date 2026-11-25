---
name: energy-storage-optimization
description: When the user wants to optimize battery storage systems, manage energy storage operations, or plan storage deployment. Also use when the user mentions "battery optimization," "BESS," "energy storage management," "battery dispatch," "storage arbitrage," "grid-scale storage," "battery sizing," or "storage scheduling." For renewable integration, see renewable-energy-planning. For grid operations, see power-grid-optimization.
---

# Energy Storage Optimization

You are an expert in energy storage optimization and battery management. Your goal is to help optimize the deployment, sizing, operation, and economics of energy storage systems (batteries, pumped hydro, compressed air, etc.) for grid services, renewable integration, and cost reduction.

## Initial Assessment

Before optimizing energy storage, understand:

1. **Storage Application**
   - Primary use case? (arbitrage, peak shaving, renewables, backup)
   - Grid services? (frequency regulation, voltage support, black start)
   - Customer type? (utility, commercial, industrial, residential)
   - Location and grid connection?

2. **Storage Technology**
   - Technology type? (Li-ion, flow battery, pumped hydro, CAES)
   - Power capacity (MW or kW)?
   - Energy capacity (MWh or kWh)?
   - Round-trip efficiency?
   - Cycle life and degradation?

3. **System Parameters**
   - Load profile and patterns?
   - Renewable generation (if applicable)?
   - Electricity pricing structure? (TOU, real-time, demand charges)
   - Grid constraints or requirements?

4. **Objectives & Constraints**
   - Primary goal? (cost savings, reliability, renewable integration)
   - Budget and economics? (capex, payback period)
   - Physical constraints? (space, temperature, safety)
   - Regulatory requirements or incentives?

---

## Energy Storage Framework

### Storage Technologies

**Electrochemical (Batteries):**
- Lithium-ion: High efficiency (90-95%), fast response, declining costs
- Flow batteries: Long duration, independent power/energy scaling
- Lead-acid: Mature, low cost, limited cycle life
- Sodium-sulfur: High energy density, high temperature operation

**Mechanical:**
- Pumped hydro: Largest capacity, 70-85% efficiency, site-specific
- Compressed air (CAES): Large scale, geological storage required
- Flywheels: High power, short duration, long cycle life

**Thermal:**
- Molten salt: CSP integration, 6-15 hours duration
- Ice storage: Cooling applications, load shifting

**Hydrogen:**
- Power-to-gas: Seasonal storage, 30-40% round-trip efficiency
- Fuel cells: Backup power, longer duration

---

## Storage Sizing Optimization

### Optimal Battery Sizing

```python
import numpy as np
import pandas as pd
from pulp import *

def optimize_battery_sizing(load_profile, solar_generation, electricity_prices,
                           max_power_mw=10, max_energy_mwh=40):
    """
    Determine optimal battery size for load shifting and solar firming

    Parameters:
    - load_profile: array of load (MW) by hour
    - solar_generation: array of solar output (MW) by hour
    - electricity_prices: array of prices ($/MWh) by hour
    - max_power_mw: maximum power capacity to consider
    - max_energy_mwh: maximum energy capacity to consider
    """

    # Evaluate different battery sizes
    power_sizes = np.linspace(1, max_power_mw, 10)
    energy_sizes = np.linspace(2, max_energy_mwh, 10)

    results = []

    for power_mw in power_sizes:
        for energy_mwh in energy_sizes:
            # Energy/Power ratio (hours)
            duration = energy_mwh / power_mw

            if duration < 0.5 or duration > 10:
                continue  # Skip infeasible ratios

            # Calculate annual value
            annual_value = optimize_battery_dispatch(
                load_profile,
                solar_generation,
                electricity_prices,
                power_mw,
                energy_mwh
            )['annual_value']

            # Calculate cost
            power_cost = power_mw * 150000  # $/MW
            energy_cost = energy_mwh * 300000  # $/MWh
            total_capex = power_cost + energy_cost

            # Calculate NPV over 15 years
            discount_rate = 0.08
            years = 15
            npv = -total_capex + sum([annual_value / (1 + discount_rate)**y
                                     for y in range(1, years + 1)])

            results.append({
                'power_mw': power_mw,
                'energy_mwh': energy_mwh,
                'duration_hours': duration,
                'capex': total_capex,
                'annual_value': annual_value,
                'npv': npv,
                'payback_years': total_capex / annual_value if annual_value > 0 else 999
            })

    # Find optimal size
    results_df = pd.DataFrame(results)
    optimal = results_df.loc[results_df['npv'].idxmax()]

    return {
        'optimal_size': {
            'power_mw': optimal['power_mw'],
            'energy_mwh': optimal['energy_mwh'],
            'duration_hours': optimal['duration_hours']
        },
        'economics': {
            'capex': optimal['capex'],
            'annual_value': optimal['annual_value'],
            'npv': optimal['npv'],
            'payback_years': optimal['payback_years']
        },
        'all_results': results_df
    }

def optimize_battery_dispatch(load, solar, prices, power_mw, energy_mwh,
                              efficiency=0.92):
    """
    Optimize battery dispatch for given size
    """
    T = len(load)
    prob = LpProblem("Battery_Dispatch", LpMaximize)

    # Variables
    charge = [LpVariable(f"Charge_{t}", lowBound=0, upBound=power_mw)
             for t in range(T)]
    discharge = [LpVariable(f"Discharge_{t}", lowBound=0, upBound=power_mw)
                for t in range(T)]
    soc = [LpVariable(f"SOC_{t}", lowBound=0, upBound=energy_mwh)
          for t in range(T)]

    # Objective: maximize arbitrage value
    prob += lpSum([(discharge[t] * prices[t] - charge[t] * prices[t])
                  for t in range(T)])

    # Constraints
    for t in range(T):
        # SOC dynamics
        if t == 0:
            prob += soc[t] == energy_mwh * 0.5 + \
                    charge[t] * efficiency - discharge[t] / efficiency
        else:
            prob += soc[t] == soc[t-1] + \
                    charge[t] * efficiency - discharge[t] / efficiency

    # Cyclic constraint (end at same SOC as start)
    prob += soc[T-1] == energy_mwh * 0.5

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Calculate annual value
    daily_value = value(prob.objective)
    annual_value = daily_value * 365

    return {
        'daily_value': daily_value,
        'annual_value': annual_value,
        'charge_schedule': [charge[t].varValue for t in range(T)],
        'discharge_schedule': [discharge[t].varValue for t in range(T)],
        'soc_profile': [soc[t].varValue for t in range(T)]
    }

# Example usage
# Generate sample data
hours = 24
load = [100, 95, 90, 85, 80, 85, 100, 120, 140, 150, 155, 160,
       158, 155, 150, 145, 150, 160, 155, 145, 130, 120, 110, 105]

solar = [0, 0, 0, 0, 0, 5, 30, 60, 90, 110, 120, 125,
        120, 110, 95, 70, 40, 15, 0, 0, 0, 0, 0, 0]

prices = [40, 38, 35, 32, 30, 35, 50, 80, 120, 140, 150, 145,
         140, 135, 130, 140, 160, 180, 170, 150, 120, 90, 60, 50]

result = optimize_battery_sizing(load, solar, prices,
                                max_power_mw=10, max_energy_mwh=40)

print(f"Optimal size: {result['optimal_size']['power_mw']:.1f} MW / "
     f"{result['optimal_size']['energy_mwh']:.1f} MWh")
print(f"NPV: ${result['economics']['npv']:,.0f}")
print(f"Payback: {result['economics']['payback_years']:.1f} years")
```

---

## Energy Arbitrage Optimization

### Price-Based Arbitrage

```python
def optimize_energy_arbitrage(prices, power_capacity, energy_capacity,
                              efficiency=0.9, cycles_per_day=1):
    """
    Optimize battery operation for energy arbitrage

    Buy low, sell high based on electricity prices
    """
    from pulp import *

    T = len(prices)
    prob = LpProblem("Arbitrage", LpMaximize)

    # Variables
    charge = [LpVariable(f"Charge_{t}", lowBound=0, upBound=power_capacity)
             for t in range(T)]
    discharge = [LpVariable(f"Discharge_{t}", lowBound=0, upBound=power_capacity)
                for t in range(T)]
    soc = [LpVariable(f"SOC_{t}", lowBound=0, upBound=energy_capacity)
          for t in range(T)]

    # Binary variables for charge/discharge (prevent simultaneous)
    u_charge = [LpVariable(f"U_charge_{t}", cat='Binary') for t in range(T)]
    u_discharge = [LpVariable(f"U_discharge_{t}", cat='Binary') for t in range(T)]

    # Objective: maximize profit
    revenue = lpSum([discharge[t] * prices[t] for t in range(T)])
    cost = lpSum([charge[t] * prices[t] for t in range(T)])
    prob += revenue - cost

    # Constraints
    for t in range(T):
        # SOC dynamics
        if t == 0:
            initial_soc = energy_capacity * 0.5
            prob += soc[t] == initial_soc + \
                    charge[t] * efficiency - discharge[t] / efficiency
        else:
            prob += soc[t] == soc[t-1] + \
                    charge[t] * efficiency - discharge[t] / efficiency

        # Cannot charge and discharge simultaneously
        prob += u_charge[t] + u_discharge[t] <= 1

        # Link binary variables to continuous
        prob += charge[t] <= power_capacity * u_charge[t]
        prob += discharge[t] <= power_capacity * u_discharge[t]

    # Cycle limit (battery degradation)
    max_throughput = energy_capacity * cycles_per_day
    prob += lpSum([discharge[t] for t in range(T)]) <= max_throughput

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'profit': value(prob.objective),
        'revenue': sum([discharge[t].varValue * prices[t] for t in range(T)]),
        'cost': sum([charge[t].varValue * prices[t] for t in range(T)]),
        'charge_schedule': [charge[t].varValue for t in range(T)],
        'discharge_schedule': [discharge[t].varValue for t in range(T)],
        'soc_profile': [soc[t].varValue for t in range(T)],
        'cycles_used': sum([discharge[t].varValue for t in range(T)]) / energy_capacity
    }
```

---

## Peak Shaving & Demand Charge Reduction

### Commercial/Industrial Peak Shaving

```python
def optimize_peak_shaving(load_forecast, demand_charge_rate,
                         energy_rate, power_capacity, energy_capacity):
    """
    Optimize battery to reduce demand charges

    Demand charges based on monthly peak demand
    """
    from pulp import *

    T = len(load_forecast)
    prob = LpProblem("Peak_Shaving", LpMinimize)

    # Variables
    charge = [LpVariable(f"Charge_{t}", lowBound=0, upBound=power_capacity)
             for t in range(T)]
    discharge = [LpVariable(f"Discharge_{t}", lowBound=0, upBound=power_capacity)
                for t in range(T)]
    soc = [LpVariable(f"SOC_{t}", lowBound=0, upBound=energy_capacity)
          for t in range(T)]

    # Net load from grid
    net_load = [LpVariable(f"NetLoad_{t}", lowBound=0) for t in range(T)]

    # Peak demand (maximum of net load)
    peak_demand = LpVariable("PeakDemand", lowBound=0)

    # Objective: minimize total cost
    demand_cost = demand_charge_rate * peak_demand
    energy_cost = lpSum([net_load[t] * energy_rate[t] for t in range(T)])

    prob += demand_cost + energy_cost

    # Constraints
    for t in range(T):
        # Net load = original load - discharge + charge
        prob += net_load[t] == load_forecast[t] - discharge[t] + charge[t]

        # Peak constraint
        prob += peak_demand >= net_load[t]

        # SOC dynamics
        if t == 0:
            prob += soc[t] == energy_capacity * 0.5 + \
                    charge[t] * 0.92 - discharge[t] / 0.92
        else:
            prob += soc[t] == soc[t-1] + \
                    charge[t] * 0.92 - discharge[t] / 0.92

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    original_peak = max(load_forecast)
    new_peak = peak_demand.varValue

    return {
        'total_cost': value(prob.objective),
        'peak_demand_kw': new_peak,
        'original_peak_kw': original_peak,
        'peak_reduction_kw': original_peak - new_peak,
        'peak_reduction_pct': (original_peak - new_peak) / original_peak * 100,
        'monthly_savings': demand_charge_rate * (original_peak - new_peak),
        'charge_schedule': [charge[t].varValue for t in range(T)],
        'discharge_schedule': [discharge[t].varValue for t in range(T)],
        'net_load_profile': [net_load[t].varValue for t in range(T)]
    }

# Example
load_forecast = [800, 750, 700, 680, 700, 750, 850, 920, 980, 1020, 1050, 1080,
                1100, 1090, 1070, 1050, 1080, 1100, 1050, 980, 920, 880, 850, 820]

demand_charge = 15  # $/kW
energy_rate = [0.08] * 24  # $/kWh

result = optimize_peak_shaving(load_forecast, demand_charge, energy_rate,
                               power_capacity=200, energy_capacity=400)

print(f"Peak reduction: {result['peak_reduction_kw']:.0f} kW "
     f"({result['peak_reduction_pct']:.1f}%)")
print(f"Monthly savings: ${result['monthly_savings']:,.0f}")
```

---

## Renewable Energy Firming

### Solar + Storage Optimization

```python
def optimize_solar_plus_storage(solar_generation, load, power_capacity,
                                energy_capacity, tariff_structure):
    """
    Optimize storage with solar to maximize self-consumption
    and minimize grid imports
    """
    from pulp import *

    T = len(solar_generation)
    prob = LpProblem("Solar_Storage", LpMinimize)

    # Variables
    charge = [LpVariable(f"Charge_{t}", lowBound=0, upBound=power_capacity)
             for t in range(T)]
    discharge = [LpVariable(f"Discharge_{t}", lowBound=0, upBound=power_capacity)
                for t in range(T)]
    soc = [LpVariable(f"SOC_{t}", lowBound=0, upBound=energy_capacity)
          for t in range(T)]

    grid_import = [LpVariable(f"Import_{t}", lowBound=0) for t in range(T)]
    grid_export = [LpVariable(f"Export_{t}", lowBound=0) for t in range(T)]

    # Objective: minimize electricity cost
    import_cost = lpSum([grid_import[t] * tariff_structure['import_rate'][t]
                        for t in range(T)])
    export_revenue = lpSum([grid_export[t] * tariff_structure['export_rate'][t]
                           for t in range(T)])

    prob += import_cost - export_revenue

    # Constraints
    for t in range(T):
        # Energy balance
        # Load = Solar + Discharge - Charge + Import - Export
        prob += load[t] == solar_generation[t] + discharge[t] - charge[t] + \
                grid_import[t] - grid_export[t]

        # Battery can only charge from solar
        prob += charge[t] <= solar_generation[t]

        # SOC dynamics
        if t == 0:
            prob += soc[t] == energy_capacity * 0.2 + \
                    charge[t] * 0.92 - discharge[t] / 0.92
        else:
            prob += soc[t] == soc[t-1] + \
                    charge[t] * 0.92 - discharge[t] / 0.92

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Calculate metrics
    total_import = sum([grid_import[t].varValue for t in range(T)])
    total_export = sum([grid_export[t].varValue for t in range(T)])
    total_load = sum(load)
    total_solar = sum(solar_generation)

    self_consumption = total_solar - total_export
    self_consumption_rate = self_consumption / total_solar * 100

    return {
        'total_cost': value(prob.objective),
        'grid_import_kwh': total_import,
        'grid_export_kwh': total_export,
        'self_consumption_kwh': self_consumption,
        'self_consumption_rate_pct': self_consumption_rate,
        'charge_schedule': [charge[t].varValue for t in range(T)],
        'discharge_schedule': [discharge[t].varValue for t in range(T)],
        'soc_profile': [soc[t].varValue for t in range(T)]
    }
```

---

## Grid Services & Frequency Regulation

### Frequency Regulation Bidding

```python
def optimize_frequency_regulation(regulation_prices, energy_prices,
                                 power_capacity, energy_capacity,
                                 performance_score=0.95):
    """
    Optimize battery participation in frequency regulation market

    Parameters:
    - regulation_prices: dict with 'reg_up' and 'reg_down' prices ($/MW)
    - energy_prices: real-time energy prices ($/MWh)
    - power_capacity: battery power rating (MW)
    - energy_capacity: battery energy capacity (MWh)
    - performance_score: historical performance (affects payment)
    """
    from pulp import *

    T = len(regulation_prices['reg_up'])
    prob = LpProblem("Frequency_Regulation", LpMaximize)

    # Variables
    reg_up_capacity = [LpVariable(f"RegUp_{t}", lowBound=0, upBound=power_capacity)
                      for t in range(T)]
    reg_down_capacity = [LpVariable(f"RegDown_{t}", lowBound=0, upBound=power_capacity)
                        for t in range(T)]

    energy_position = [LpVariable(f"Energy_{t}") for t in range(T)]

    # Objective: maximize regulation revenue
    reg_up_revenue = lpSum([reg_up_capacity[t] * regulation_prices['reg_up'][t] *
                           performance_score for t in range(T)])
    reg_down_revenue = lpSum([reg_down_capacity[t] * regulation_prices['reg_down'][t] *
                             performance_score for t in range(T)])

    prob += reg_up_revenue + reg_down_revenue

    # Constraints
    for t in range(T):
        # Power capacity constraint
        prob += reg_up_capacity[t] + reg_down_capacity[t] <= power_capacity

        # Energy capacity constraint (must be able to sustain regulation)
        # Assume 50% deployment over hour
        prob += energy_position[t] + 0.5 * reg_up_capacity[t] <= energy_capacity
        prob += energy_position[t] - 0.5 * reg_down_capacity[t] >= 0

        # Energy neutrality (return to same SOC)
        if t > 0:
            prob += energy_position[t] == energy_position[t-1]

    prob += energy_position[0] == energy_capacity * 0.5

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'total_revenue': value(prob.objective),
        'reg_up_capacity': [reg_up_capacity[t].varValue for t in range(T)],
        'reg_down_capacity': [reg_down_capacity[t].varValue for t in range(T)],
        'avg_capacity_offered': np.mean([reg_up_capacity[t].varValue + reg_down_capacity[t].varValue
                                        for t in range(T)])
    }
```

---

## Battery Degradation & Lifetime Management

### Degradation Modeling

```python
class BatteryDegradationModel:
    """
    Model battery degradation from cycling and calendar aging
    """

    def __init__(self, initial_capacity_mwh, chemistry='li-ion'):
        self.initial_capacity = initial_capacity_mwh
        self.current_capacity = initial_capacity_mwh
        self.chemistry = chemistry
        self.total_cycles = 0
        self.total_throughput = 0

    def calculate_cycle_aging(self, depth_of_discharge, num_cycles):
        """
        Calculate capacity loss from cycling

        Cycle life depends on DOD:
        - 10% DOD: ~100,000 cycles
        - 50% DOD: ~10,000 cycles
        - 80% DOD: ~5,000 cycles
        - 100% DOD: ~3,000 cycles
        """
        if self.chemistry == 'li-ion':
            # Empirical cycle life model
            cycle_life_100 = 3000  # cycles at 100% DOD

            # Cycle life increases with lower DOD (roughly exponential)
            cycle_life = cycle_life_100 * (1 / depth_of_discharge) ** 0.5

            # Capacity loss per cycle
            loss_per_cycle = 0.2 / cycle_life  # 20% loss at EOL

            capacity_loss = loss_per_cycle * num_cycles

        elif self.chemistry == 'flow-battery':
            # Flow batteries have minimal cycle degradation
            capacity_loss = 0.0001 * num_cycles

        else:
            capacity_loss = 0

        self.current_capacity -= capacity_loss
        self.total_cycles += num_cycles

        return capacity_loss

    def calculate_calendar_aging(self, days, avg_soc=0.5, avg_temp_c=25):
        """
        Calculate capacity loss from calendar aging

        Higher SOC and temperature accelerate aging
        """
        if self.chemistry == 'li-ion':
            # Base calendar aging: 2-3% per year at 25°C, 50% SOC
            base_rate = 0.025 / 365  # per day

            # Temperature factor (Arrhenius-like)
            temp_factor = np.exp((avg_temp_c - 25) * 0.05)

            # SOC stress factor
            soc_factor = 1 + (avg_soc - 0.5)

            daily_loss_rate = base_rate * temp_factor * soc_factor
            capacity_loss = daily_loss_rate * days * self.initial_capacity

        else:
            capacity_loss = 0

        self.current_capacity -= capacity_loss

        return capacity_loss

    def calculate_state_of_health(self):
        """Return current state of health (%)"""
        return (self.current_capacity / self.initial_capacity) * 100

    def estimate_remaining_life(self, daily_cycles, avg_dod):
        """
        Estimate remaining useful life

        Returns days until 80% capacity threshold
        """
        target_capacity = self.initial_capacity * 0.8
        remaining_capacity_to_lose = self.current_capacity - target_capacity

        if remaining_capacity_to_lose <= 0:
            return 0  # Already below threshold

        # Daily degradation from cycling
        cycle_loss_per_day = self.calculate_cycle_aging(avg_dod, daily_cycles)

        # Daily calendar aging
        calendar_loss_per_day = self.calculate_calendar_aging(1)

        total_daily_loss = cycle_loss_per_day + calendar_loss_per_day

        if total_daily_loss <= 0:
            return float('inf')

        remaining_days = remaining_capacity_to_lose / total_daily_loss

        return remaining_days

# Example usage
battery = BatteryDegradationModel(initial_capacity_mwh=10, chemistry='li-ion')

# Simulate 1 year of operation
for day in range(365):
    # 1 cycle per day at 80% DOD
    battery.calculate_cycle_aging(depth_of_discharge=0.8, num_cycles=1)
    # Calendar aging
    battery.calculate_calendar_aging(days=1, avg_soc=0.6, avg_temp_c=25)

print(f"State of Health after 1 year: {battery.calculate_state_of_health():.1f}%")
print(f"Estimated remaining life: {battery.estimate_remaining_life(1, 0.8)/365:.1f} years")
```

---

## Multi-Use Case Value Stacking

### Stacked Revenue Optimization

```python
def optimize_multi_use_storage(use_cases, power_capacity, energy_capacity,
                               time_horizon=24):
    """
    Optimize battery across multiple revenue streams (value stacking)

    Use cases can include:
    - Energy arbitrage
    - Demand charge reduction
    - Frequency regulation
    - Capacity market
    - Renewable firming
    """
    from pulp import *

    prob = LpProblem("Value_Stacking", LpMaximize)

    T = time_horizon

    # Variables: power allocation to each use case
    allocation = {}
    for use_case in use_cases:
        for t in range(T):
            allocation[use_case['name'], t] = LpVariable(
                f"{use_case['name']}_{t}",
                lowBound=0,
                upBound=power_capacity
            )

    # Objective: maximize total revenue
    total_revenue = []

    for use_case in use_cases:
        for t in range(T):
            value_rate = use_case['value_per_mw_hour'][t]
            total_revenue.append(allocation[use_case['name'], t] * value_rate)

    prob += lpSum(total_revenue)

    # Constraints

    # Total power allocation cannot exceed capacity
    for t in range(T):
        prob += lpSum([allocation[uc['name'], t] for uc in use_cases]) <= power_capacity

    # Use case specific constraints
    for use_case in use_cases:
        if 'min_commitment' in use_case:
            # Some services require minimum commitment
            for t in range(T):
                prob += allocation[use_case['name'], t] >= \
                        use_case['min_commitment'] * power_capacity

        if 'max_hours' in use_case:
            # Some services limited to certain hours per day
            prob += lpSum([allocation[use_case['name'], t]
                          for t in range(T)]) <= use_case['max_hours'] * power_capacity

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Calculate revenue by use case
    revenue_breakdown = {}
    for use_case in use_cases:
        revenue = sum([allocation[use_case['name'], t].varValue *
                      use_case['value_per_mw_hour'][t]
                      for t in range(T)])
        revenue_breakdown[use_case['name']] = revenue

    return {
        'total_revenue': value(prob.objective),
        'revenue_breakdown': revenue_breakdown,
        'allocation_schedule': {
            use_case['name']: [allocation[use_case['name'], t].varValue
                              for t in range(T)]
            for use_case in use_cases
        }
    }

# Example
use_cases = [
    {
        'name': 'Energy_Arbitrage',
        'value_per_mw_hour': [5, 4, 3, 2, 2, 3, 8, 15, 20, 22, 24, 23,
                             22, 21, 20, 22, 25, 28, 26, 22, 18, 12, 8, 6]
    },
    {
        'name': 'Frequency_Regulation',
        'value_per_mw_hour': [12] * 24,
        'min_commitment': 0.5,  # Must commit at least 50% if participating
    },
    {
        'name': 'Demand_Response',
        'value_per_mw_hour': [0]*14 + [50, 50, 50, 50] + [0]*6,
        'max_hours': 4  # Only 4 hours per day
    }
]

result = optimize_multi_use_storage(use_cases, power_capacity=10,
                                   energy_capacity=40, time_horizon=24)

print(f"Total daily revenue: ${result['total_revenue']:,.0f}")
for uc, rev in result['revenue_breakdown'].items():
    print(f"  {uc}: ${rev:,.0f} ({rev/result['total_revenue']*100:.1f}%)")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `Pyomo`: Advanced optimization modeling
- `cvxpy`: Convex optimization
- `gurobipy`: Gurobi optimizer

**Battery Modeling:**
- `PyBaMM`: Physics-based battery modeling
- `scikit-learn`: Machine learning for degradation

**Energy Analysis:**
- `pvlib`: Solar PV modeling
- `pandapower`: Power system analysis
- `SAM` (NREL): System Advisor Model

**Data & Visualization:**
- `pandas`, `numpy`: Data manipulation
- `matplotlib`, `plotly`: Visualization

### Commercial Software

**Energy Storage:**
- **Energy Toolbase**: Battery storage analysis and proposals
- **Homer Energy**: Hybrid renewable energy system design
- **CAISO BESS**: Battery energy storage system tools
- **Stem Athena**: AI-powered storage optimization

**Grid Integration:**
- **AutoGrid Flex**: Distributed energy resource optimization
- **Greensmith GEMS**: Grid energy management system
- **Fluence Mosaic**: Battery energy storage platform
- **Tesla Autobidder**: Automated energy trading

**Financial Analysis:**
- **Aurora**: Energy market modeling
- **Ascend Analytics**: Storage valuation
- **NREL REopt**: Renewable energy integration

---

## Common Challenges & Solutions

### Challenge: Revenue Uncertainty

**Problem:**
- Volatile electricity prices
- Changing market rules
- Technology cost trends

**Solutions:**
- Conservative financial projections
- Diversified revenue streams (value stacking)
- Flexible contracts and PPAs
- Real options analysis
- Scenario-based planning

### Challenge: Degradation Management

**Problem:**
- Battery capacity fade over time
- Warranty compliance
- Optimal replacement timing

**Solutions:**
- Degradation-aware dispatch algorithms
- State-of-health monitoring
- Conservative DOD and cycle limits
- Predictive maintenance
- Augmentation strategies

### Challenge: Grid Integration

**Problem:**
- Interconnection delays and costs
- Grid service requirements
- Utility coordination

**Solutions:**
- Early interconnection applications
- Pre-approved equipment lists
- Clear operating procedures
- Regular communication with utility
- Compliance testing and certification

### Challenge: Optimal Sizing

**Problem:**
- Uncertain future load/generation
- Technology cost evolution
- Competing use cases

**Solutions:**
- Sensitivity analysis on key parameters
- Modular/scalable designs
- Option value of waiting
- Pilot programs before full deployment
- Multi-year optimization

---

## Output Format

### Energy Storage Optimization Report

**Executive Summary:**
- Recommended storage system configuration
- Economic analysis and payback
- Primary value drivers
- Implementation roadmap

**System Specifications:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Technology | Li-ion NMC | High energy density |
| Power Capacity | 5 MW | AC rating |
| Energy Capacity | 20 MWh | Usable capacity |
| Duration | 4 hours | At rated power |
| Round-trip Efficiency | 88% | AC-AC |
| Warranty | 10 years / 5,000 cycles | 80% EOL capacity |

**Economic Analysis:**

| Metric | Value |
|--------|-------|
| Capital Cost | $7.5M |
| Installation & EPC | $1.5M |
| **Total Project Cost** | **$9.0M** |
| Annual Revenue | $1.2M |
| Annual O&M | $75K |
| Net Annual Benefit | $1.125M |
| Simple Payback | 8.0 years |
| NPV (15 years, 8%) | $3.2M |
| IRR | 12.5% |

**Revenue Streams:**

| Revenue Source | Annual Value | % of Total |
|----------------|--------------|------------|
| Energy Arbitrage | $450K | 37% |
| Demand Charge Reduction | $380K | 32% |
| Frequency Regulation | $270K | 22% |
| Capacity Market | $100K | 8% |
| **Total** | **$1,200K** | **100%** |

**Operational Strategy:**

| Time Period | Primary Use | Secondary Use | Avg. SOC Target |
|-------------|-------------|---------------|-----------------|
| 00:00-06:00 | Charge (arbitrage) | - | 80% |
| 06:00-10:00 | Frequency regulation | - | 50% |
| 10:00-14:00 | Solar firming | Regulation | 40% |
| 14:00-20:00 | Peak shaving | Arbitrage | 20% |
| 20:00-24:00 | Discharge (arbitrage) | - | 40% |

**Performance Metrics:**

| Metric | Target | Monitoring |
|--------|--------|------------|
| Daily Cycles | 1.2 | SCADA logging |
| Avg. DOD | 70% | BMS data |
| Availability | > 95% | Uptime tracking |
| Response Time | < 1 sec | Market compliance |
| SOH Degradation | < 2.5%/year | Quarterly testing |

---

## Questions to Ask

If you need more context:
1. What's the primary application? (arbitrage, peak shaving, renewables, grid services)
2. What's the scale? (residential, commercial, utility)
3. What's the grid tariff structure? (TOU, demand charges, real-time pricing)
4. What renewable generation exists or is planned?
5. What's the available budget or target payback period?
6. Are there space, temperature, or safety constraints?
7. What's the expected project lifetime?

---

## Related Skills

- **power-grid-optimization**: For grid integration and dispatch
- **renewable-energy-planning**: For solar and wind pairing
- **energy-logistics**: For energy supply chain management
- **demand-forecasting**: For load and generation forecasting
- **optimization-modeling**: For advanced optimization techniques
- **capacity-planning**: For long-term capacity planning
- **risk-mitigation**: For financial and operational risk management
