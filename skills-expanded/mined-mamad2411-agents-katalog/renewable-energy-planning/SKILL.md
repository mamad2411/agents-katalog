---
name: renewable-energy-planning
description: When the user wants to plan renewable energy supply chains, optimize wind or solar logistics, or manage clean energy operations. Also use when the user mentions "solar logistics," "wind farm operations," "renewable energy supply chain," "green energy planning," "battery storage," "solar panel distribution," "wind turbine logistics," or "clean energy optimization." For power grids, see power-grid-optimization. For energy storage, see energy-storage-optimization.
---

# Renewable Energy Planning

You are an expert in renewable energy supply chain planning and optimization. Your goal is to help design and optimize the logistics, operations, and supply chains for wind, solar, and other renewable energy systems, balancing cost, reliability, sustainability, and grid integration.

## Initial Assessment

Before planning renewable energy operations, understand:

1. **Energy Source & Technology**
   - What renewable type? (solar PV, wind, hydro, biomass, geothermal)
   - Installation scale? (residential, commercial, utility-scale)
   - Technology specifications? (panel types, turbine models)
   - Geographic locations and sites?

2. **Project Phase**
   - Development stage? (planning, construction, operation)
   - Timeline and milestones?
   - Existing infrastructure or greenfield?
   - Grid connection status?

3. **Supply Chain Scope**
   - Manufacturing and sourcing?
   - Transportation and logistics?
   - Installation and commissioning?
   - Operations and maintenance (O&M)?

4. **Objectives & Constraints**
   - Primary goals? (cost, speed, sustainability)
   - Budget and financing structure?
   - Regulatory requirements and incentives?
   - Environmental or community constraints?

---

## Renewable Energy Supply Chain Framework

### End-to-End Supply Chain

**Upstream (Manufacturing):**
- Raw material sourcing (silicon, rare earths, steel)
- Component manufacturing (panels, turbines, batteries)
- Quality control and testing
- Supplier management

**Midstream (Logistics):**
- International shipping (containers, heavy-lift)
- Domestic transportation (truck, rail, specialized)
- Warehousing and staging
- Customs and compliance

**Downstream (Installation & Operation):**
- Site preparation and construction
- Installation and commissioning
- Grid connection and testing
- Ongoing operations and maintenance

---

## Solar Energy Logistics

### Solar Panel Supply Chain

**Component Structure:**
- Photovoltaic modules (panels)
- Inverters
- Racking and mounting systems
- Electrical components (cables, connectors)
- Monitoring systems

**Planning Model:**
```python
import numpy as np
import pandas as pd
from pulp import *

def optimize_solar_supply_chain(projects, suppliers, warehouses, costs):
    """
    Optimize solar component supply chain from suppliers to project sites

    Parameters:
    - projects: list of {id, location, demand_mw, installation_date}
    - suppliers: list of {id, location, capacity_mw, lead_time}
    - warehouses: list of {id, location, capacity, cost_per_mw}
    - costs: dict with transportation and inventory costs
    """

    prob = LpProblem("Solar_Supply_Chain", LpMinimize)

    # Decision variables
    # x[s,w]: flow from supplier s to warehouse w
    x_sw = {}
    for s in range(len(suppliers)):
        for w in range(len(warehouses)):
            x_sw[s, w] = LpVariable(f"Supplier_{s}_Warehouse_{w}",
                                   lowBound=0)

    # y[w,p]: flow from warehouse w to project p
    y_wp = {}
    for w in range(len(warehouses)):
        for p in range(len(projects)):
            y_wp[w, p] = LpVariable(f"Warehouse_{w}_Project_{p}",
                                   lowBound=0)

    # Objective function: minimize total cost
    total_cost = []

    # Supplier to warehouse transportation
    for (s, w), var in x_sw.items():
        distance = calculate_distance(
            suppliers[s]['location'],
            warehouses[w]['location']
        )
        total_cost.append(costs['transport_supplier_warehouse'] * distance * var)

    # Warehouse holding costs
    for w in range(len(warehouses)):
        warehouse_volume = lpSum([x_sw[s, w] for s in range(len(suppliers))])
        total_cost.append(warehouses[w]['cost_per_mw'] * warehouse_volume)

    # Warehouse to project transportation
    for (w, p), var in y_wp.items():
        distance = calculate_distance(
            warehouses[w]['location'],
            projects[p]['location']
        )
        total_cost.append(costs['transport_warehouse_project'] * distance * var)

    prob += lpSum(total_cost)

    # Constraints

    # Supplier capacity
    for s in range(len(suppliers)):
        prob += lpSum([x_sw[s, w] for w in range(len(warehouses))]) <= \
                suppliers[s]['capacity_mw']

    # Warehouse capacity
    for w in range(len(warehouses)):
        prob += lpSum([x_sw[s, w] for s in range(len(suppliers))]) <= \
                warehouses[w]['capacity']

    # Warehouse balance (in = out)
    for w in range(len(warehouses)):
        inflow = lpSum([x_sw[s, w] for s in range(len(suppliers))])
        outflow = lpSum([y_wp[w, p] for p in range(len(projects))])
        prob += inflow == outflow

    # Project demand satisfaction
    for p in range(len(projects)):
        prob += lpSum([y_wp[w, p] for w in range(len(warehouses))]) >= \
                projects[p]['demand_mw']

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'supplier_flows': {(s, w): x_sw[s, w].varValue
                          for (s, w) in x_sw if x_sw[s, w].varValue > 0.01},
        'project_flows': {(w, p): y_wp[w, p].varValue
                         for (w, p) in y_wp if y_wp[w, p].varValue > 0.01}
    }

def calculate_distance(loc1, loc2):
    """Calculate distance between two locations"""
    return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2) * 69  # miles

# Example usage
projects = [
    {'id': 'Solar_Farm_A', 'location': (35.0, -120.0),
     'demand_mw': 50, 'installation_date': '2026-06'},
    {'id': 'Solar_Farm_B', 'location': (33.0, -117.0),
     'demand_mw': 100, 'installation_date': '2026-09'},
]

suppliers = [
    {'id': 'Supplier_Asia', 'location': (22.0, 114.0),
     'capacity_mw': 500, 'lead_time': 60},
    {'id': 'Supplier_US', 'location': (40.0, -105.0),
     'capacity_mw': 200, 'lead_time': 30},
]

warehouses = [
    {'id': 'Warehouse_West', 'location': (34.0, -118.0),
     'capacity': 300, 'cost_per_mw': 1000},
    {'id': 'Warehouse_Central', 'location': (39.0, -105.0),
     'capacity': 400, 'cost_per_mw': 800},
]

costs = {
    'transport_supplier_warehouse': 0.50,  # $/MW/mile
    'transport_warehouse_project': 2.00,
}

result = optimize_solar_supply_chain(projects, suppliers, warehouses, costs)
```

### Installation Scheduling

```python
def schedule_solar_installation(projects, crews, equipment):
    """
    Schedule solar installation activities

    Parameters:
    - projects: list of {id, size_mw, location, earliest_start, deadline}
    - crews: list of {id, capacity_mw_per_day, availability}
    - equipment: list of {type, quantity, required_per_mw}
    """
    from pulp import *
    import datetime

    prob = LpProblem("Installation_Schedule", LpMinimize)

    # Time periods (days)
    horizon = 180
    periods = range(horizon)

    # Variables: assign crew to project in period
    x = {}
    for p, project in enumerate(projects):
        for c, crew in enumerate(crews):
            for t in periods:
                x[p, c, t] = LpVariable(f"Project_{p}_Crew_{c}_Day_{t}",
                                       cat='Binary')

    # Project completion time
    completion = {}
    for p in range(len(projects)):
        completion[p] = LpVariable(f"Completion_{p}", lowBound=0)

    # Objective: minimize total project completion time (makespan)
    prob += lpSum([completion[p] for p in range(len(projects))])

    # Constraints

    # Crew can work on one project per day
    for c in range(len(crews)):
        for t in periods:
            prob += lpSum([x[p, c, t] for p in range(len(projects))]) <= 1

    # Project must be completed
    for p, project in enumerate(projects):
        days_needed = project['size_mw'] / sum(
            crews[c]['capacity_mw_per_day'] for c in range(len(crews))
        )

        prob += lpSum([x[p, c, t]
                      for c in range(len(crews))
                      for t in periods]) >= days_needed

    # Completion time definition
    for p in range(len(projects)):
        for t in periods:
            prob += completion[p] >= t * lpSum([x[p, c, t]
                                               for c in range(len(crews))])

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    schedule = {}
    for p in range(len(projects)):
        assigned_days = [(c, t) for (p_, c, t) in x
                        if p_ == p and x[p_, c, t].varValue > 0.5]
        schedule[projects[p]['id']] = {
            'assigned_crews': assigned_days,
            'completion_day': completion[p].varValue
        }

    return schedule
```

---

## Wind Energy Logistics

### Wind Turbine Components

**Major Components:**
- Tower sections (3-4 pieces, 80-120m total height)
- Nacelle (generator housing, 50-100 tons)
- Blades (3 per turbine, 50-80m length each)
- Hub and rotor
- Foundation components

### Heavy-Haul Transportation

```python
class WindTurbineLogistics:
    """
    Manage logistics for wind turbine transportation and installation
    """

    def __init__(self, wind_farm_location, turbine_specs):
        self.wind_farm = wind_farm_location
        self.turbine_specs = turbine_specs

    def plan_heavy_haul_route(self, origin, destination, component_type):
        """
        Plan heavy-haul route considering constraints

        Returns feasible route and cost estimate
        """

        constraints = {
            'blade': {
                'max_length': 80,  # meters
                'max_weight': 25,  # tons
                'requires_special_trailer': True,
                'clearance_needed': True,
                'road_width_min': 5  # meters
            },
            'nacelle': {
                'max_weight': 100,  # tons
                'requires_crane': True,
                'road_grade_max': 8,  # percent
                'bridge_capacity_needed': 150  # tons
            },
            'tower': {
                'max_length': 40,  # meters
                'max_weight': 80,  # tons
                'road_width_min': 4.5  # meters
            }
        }

        component_constraints = constraints.get(component_type, {})

        # Route analysis
        route = {
            'distance': self.calculate_route_distance(origin, destination),
            'estimated_time': None,
            'permits_required': [],
            'infrastructure_upgrades': [],
            'cost_estimate': 0
        }

        # Calculate transport time (slow speed for oversized loads)
        avg_speed = 20  # mph for heavy haul
        route['estimated_time'] = route['distance'] / avg_speed

        # Identify permit requirements
        if component_constraints.get('requires_special_trailer'):
            route['permits_required'].append('Oversized Load Permit')
            route['cost_estimate'] += 5000

        if component_constraints.get('clearance_needed'):
            route['permits_required'].append('Utility Clearance')
            route['cost_estimate'] += 2000

        # Base transportation cost
        route['cost_estimate'] += route['distance'] * 15  # $/mile

        return route

    def calculate_route_distance(self, origin, dest):
        """Calculate route distance"""
        import numpy as np
        return np.sqrt((dest[0] - origin[0])**2 + (dest[1] - origin[1])**2) * 69

    def optimize_turbine_delivery_sequence(self, turbines, delivery_schedule):
        """
        Optimize the sequence of turbine deliveries to minimize total time

        Just-in-time delivery to avoid on-site storage
        """

        # Calculate installation duration per turbine
        install_time_days = 3  # typical time per turbine

        sequence = []
        current_day = 0

        for turbine in turbines:
            # Deliver components just before installation
            delivery_dates = {
                'foundation': current_day - 10,  # arrives early
                'tower': current_day - 2,
                'nacelle': current_day - 1,
                'blades': current_day
            }

            sequence.append({
                'turbine_id': turbine['id'],
                'installation_start': current_day,
                'installation_end': current_day + install_time_days,
                'component_deliveries': delivery_dates
            })

            current_day += install_time_days

        return sequence

# Example usage
logistics = WindTurbineLogistics(
    wind_farm_location=(42.0, -95.0),
    turbine_specs={'height': 100, 'capacity_mw': 3.0}
)

route = logistics.plan_heavy_haul_route(
    origin=(41.5, -93.0),  # Manufacturing plant
    destination=(42.0, -95.0),  # Wind farm
    component_type='blade'
)

print(f"Route distance: {route['distance']:.1f} miles")
print(f"Estimated cost: ${route['cost_estimate']:,.0f}")
print(f"Permits required: {route['permits_required']}")
```

### Crane and Equipment Scheduling

```python
def schedule_crane_operations(turbines, cranes, weather_windows):
    """
    Schedule crane operations for turbine installation

    Must consider weather constraints (wind speed limits)
    """
    from pulp import *

    prob = LpProblem("Crane_Scheduling", LpMinimize)

    days = len(weather_windows)

    # Variables: crane c installs turbine t on day d
    x = {}
    for t, turbine in enumerate(turbines):
        for c, crane in enumerate(cranes):
            for d in range(days):
                if weather_windows[d]['suitable_for_crane']:
                    x[t, c, d] = LpVariable(f"Turbine_{t}_Crane_{c}_Day_{d}",
                                           cat='Binary')

    # Completion time for each turbine
    completion = {}
    for t in range(len(turbines)):
        completion[t] = LpVariable(f"Done_{t}", lowBound=0)

    # Objective: minimize makespan
    max_completion = LpVariable("Makespan", lowBound=0)
    prob += max_completion

    for t in range(len(turbines)):
        prob += max_completion >= completion[t]

    # Constraints

    # Each turbine installed exactly once
    for t in range(len(turbines)):
        prob += lpSum([x[t, c, d] for (t_, c, d) in x if t_ == t]) == 1

    # Crane used once per day
    for c in range(len(cranes)):
        for d in range(days):
            turbines_on_day = [x[t, c, d] for (t, c_, d_) in x
                             if c_ == c and d_ == d]
            if turbines_on_day:
                prob += lpSum(turbines_on_day) <= 1

    # Define completion times
    for t in range(len(turbines)):
        for (t_, c, d) in x:
            if t_ == t:
                prob += completion[t] >= d * x[t, c, d]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    schedule = []
    for (t, c, d) in x:
        if x[t, c, d].varValue > 0.5:
            schedule.append({
                'turbine': turbines[t]['id'],
                'crane': cranes[c]['id'],
                'day': d,
                'weather': weather_windows[d]
            })

    return {
        'schedule': schedule,
        'makespan': max_completion.varValue
    }
```

---

## Operations & Maintenance (O&M)

### Preventive Maintenance Scheduling

```python
import pandas as pd
import numpy as np

class RenewableEnergyOM:
    """
    Operations and maintenance optimization for renewable energy assets
    """

    def __init__(self, assets, maintenance_plans):
        self.assets = assets
        self.maintenance_plans = maintenance_plans

    def schedule_preventive_maintenance(self, horizon_days=365):
        """
        Schedule preventive maintenance to minimize downtime and cost
        """
        from pulp import *

        prob = LpProblem("PM_Scheduling", LpMinimize)

        # Variables: perform maintenance m on asset a in period t
        x = {}
        for a, asset in enumerate(self.assets):
            for m, plan in enumerate(self.maintenance_plans):
                for t in range(horizon_days):
                    x[a, m, t] = LpVariable(f"Asset_{a}_Maint_{m}_Day_{t}",
                                           cat='Binary')

        # Objective: minimize cost + downtime cost
        total_cost = []

        for (a, m, t), var in x.items():
            plan = self.maintenance_plans[m]
            asset = self.assets[a]

            # Direct maintenance cost
            maint_cost = plan['cost']

            # Downtime cost (lost production)
            downtime_hours = plan['duration_hours']
            lost_production = asset['capacity_mw'] * downtime_hours
            production_value = lost_production * asset['price_per_mwh']

            total_cost.append((maint_cost + production_value) * var)

        prob += lpSum(total_cost)

        # Constraints

        # Maintenance frequency requirements
        for a, asset in enumerate(self.assets):
            for m, plan in enumerate(self.maintenance_plans):
                if plan['type'] in asset['required_maintenance']:
                    frequency = plan['frequency_days']
                    num_required = horizon_days // frequency

                    prob += lpSum([x[a, m, t] for t in range(horizon_days)]) >= num_required

        # Resource constraints (crews available)
        max_crew_per_day = 3
        for t in range(horizon_days):
            prob += lpSum([x[a, m, t] for (a, m, t_) in x if t_ == t]) <= max_crew_per_day

        # No overlapping maintenance on same asset
        for a in range(len(self.assets)):
            for t in range(horizon_days):
                prob += lpSum([x[a, m, t] for m in range(len(self.maintenance_plans))]) <= 1

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract schedule
        schedule = []
        for (a, m, t) in x:
            if x[a, m, t].varValue > 0.5:
                schedule.append({
                    'asset': self.assets[a]['id'],
                    'maintenance_type': self.maintenance_plans[m]['type'],
                    'day': t,
                    'duration_hours': self.maintenance_plans[m]['duration_hours'],
                    'cost': self.maintenance_plans[m]['cost']
                })

        return schedule

    def predict_component_failure(self, sensor_data, historical_failures):
        """
        Predict component failures using machine learning

        Enables predictive maintenance
        """
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler

        # Prepare features
        X = sensor_data[['vibration', 'temperature', 'power_output',
                        'age_days', 'operating_hours']]

        # Target: failure within next 30 days
        y = historical_failures['failed_within_30_days']

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)

        # Predict for current assets
        current_data = sensor_data[sensor_data['date'] == sensor_data['date'].max()]
        X_current = current_data[['vibration', 'temperature', 'power_output',
                                  'age_days', 'operating_hours']]
        X_current_scaled = scaler.transform(X_current)

        predictions = model.predict_proba(X_current_scaled)[:, 1]

        # Flag high-risk assets
        risk_threshold = 0.7
        high_risk = current_data[predictions > risk_threshold].copy()
        high_risk['failure_probability'] = predictions[predictions > risk_threshold]

        return {
            'model_accuracy': model.score(X_scaled, y),
            'feature_importance': dict(zip(X.columns, model.feature_importances_)),
            'high_risk_assets': high_risk[['asset_id', 'failure_probability']].to_dict('records')
        }
```

---

## Energy Production Forecasting

### Solar Generation Forecast

```python
def forecast_solar_generation(historical_generation, weather_forecast):
    """
    Forecast solar energy generation using weather data

    Parameters:
    - historical_generation: DataFrame with datetime, actual_mwh
    - weather_forecast: DataFrame with datetime, irradiance, cloud_cover, temperature
    """
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    import pandas as pd

    # Merge historical data with weather
    data = historical_generation.merge(weather_forecast, on='datetime')

    # Feature engineering
    data['hour'] = data['datetime'].dt.hour
    data['month'] = data['datetime'].dt.month
    data['day_of_year'] = data['datetime'].dt.dayofyear

    # Calculate theoretical max (seasonal variation)
    data['theoretical_max'] = 1 + 0.3 * np.sin(2 * np.pi * data['day_of_year'] / 365)

    # Features
    features = ['irradiance', 'cloud_cover', 'temperature',
               'hour', 'month', 'theoretical_max']

    X = data[features]
    y = data['actual_mwh']

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)

    # Forecast
    forecast = model.predict(weather_forecast[features])

    return {
        'forecast_mwh': forecast,
        'model_r2': model.score(X_test, y_test),
        'feature_importance': dict(zip(features, model.feature_importances_))
    }
```

### Wind Generation Forecast

```python
def forecast_wind_generation(wind_speed_forecast, turbine_specs):
    """
    Forecast wind energy generation from wind speed forecasts

    Uses power curve of wind turbine
    """

    def power_curve(wind_speed, rated_power, cut_in, rated_speed, cut_out):
        """
        Wind turbine power curve

        Parameters:
        - wind_speed: m/s
        - rated_power: MW
        - cut_in: minimum wind speed (m/s)
        - rated_speed: wind speed at rated power (m/s)
        - cut_out: maximum wind speed (m/s)
        """
        if wind_speed < cut_in or wind_speed > cut_out:
            return 0
        elif wind_speed >= rated_speed:
            return rated_power
        else:
            # Cubic relationship in operating range
            return rated_power * ((wind_speed - cut_in) / (rated_speed - cut_in)) ** 3

    # Apply power curve to wind speed forecast
    generation_forecast = []

    for ws in wind_speed_forecast:
        power = power_curve(
            wind_speed=ws,
            rated_power=turbine_specs['rated_power_mw'],
            cut_in=turbine_specs['cut_in_speed'],
            rated_speed=turbine_specs['rated_wind_speed'],
            cut_out=turbine_specs['cut_out_speed']
        )
        generation_forecast.append(power * turbine_specs['num_turbines'])

    return {
        'forecast_mwh': generation_forecast,
        'capacity_factor': np.mean(generation_forecast) /
                          (turbine_specs['rated_power_mw'] * turbine_specs['num_turbines'])
    }

# Example
turbine_specs = {
    'rated_power_mw': 3.0,
    'cut_in_speed': 3.0,  # m/s
    'rated_wind_speed': 12.0,  # m/s
    'cut_out_speed': 25.0,  # m/s
    'num_turbines': 50
}

wind_forecast = [5, 7, 9, 11, 13, 15, 10, 8, 6]  # m/s

result = forecast_wind_generation(wind_forecast, turbine_specs)
print(f"Forecasted capacity factor: {result['capacity_factor']:.1%}")
```

---

## Grid Integration & Energy Storage

### Grid Connection Planning

```python
def plan_grid_connection(renewable_site, substations, grid_capacity):
    """
    Optimize grid connection point for renewable energy project

    Parameters:
    - renewable_site: {location, capacity_mw}
    - substations: list of {id, location, available_capacity_mw, connection_cost}
    - grid_capacity: capacity constraints
    """
    from pulp import *

    prob = LpProblem("Grid_Connection", LpMinimize)

    # Variables: connect to substation s
    x = {}
    for s, substation in enumerate(substations):
        if substation['available_capacity_mw'] >= renewable_site['capacity_mw']:
            x[s] = LpVariable(f"Connect_to_{s}", cat='Binary')

    # Objective: minimize connection cost + transmission line cost
    total_cost = []

    for s, var in x.items():
        substation = substations[s]

        # Distance-based transmission line cost
        distance = calculate_distance(
            renewable_site['location'],
            substation['location']
        )

        line_cost = distance * 1000000  # $1M per mile for transmission line
        connection_cost = substation['connection_cost']

        total_cost.append((line_cost + connection_cost) * var)

    prob += lpSum(total_cost)

    # Constraints

    # Connect to exactly one substation
    prob += lpSum([x[s] for s in x]) == 1

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    selected = [s for s in x if x[s].varValue > 0.5][0]

    return {
        'selected_substation': substations[selected]['id'],
        'connection_cost': value(prob.objective),
        'distance_miles': calculate_distance(
            renewable_site['location'],
            substations[selected]['location']
        )
    }

def calculate_distance(loc1, loc2):
    """Calculate distance between locations"""
    import numpy as np
    return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2) * 69
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `pyomo`: Optimization modeling
- `cvxpy`: Convex optimization

**Weather & Solar:**
- `pvlib`: Photovoltaic modeling
- `windpowerlib`: Wind turbine modeling
- `solarpy`: Solar position calculations

**Forecasting:**
- `scikit-learn`: Machine learning
- `xgboost`, `lightgbm`: Gradient boosting
- `prophet`: Time series forecasting
- `statsmodels`: Statistical models

**Geospatial:**
- `geopandas`: Geographic data
- `rasterio`: Raster data processing
- `pyproj`: Coordinate systems

### Commercial Software

**Project Management:**
- **PVsyst**: Solar PV system design
- **WindPRO**: Wind farm design and optimization
- **RETScreen**: Renewable energy project analysis
- **HOMER**: Hybrid renewable energy system design

**Asset Management:**
- **Greenbyte**: Wind and solar asset management
- **3TIER**: Renewable energy forecasting
- **SCADA systems**: Supervisory control and data acquisition

**Supply Chain:**
- **SAP S/4HANA**: ERP with renewable energy modules
- **Oracle Primavera**: Project scheduling
- **Microsoft Project**: Project management

---

## Common Challenges & Solutions

### Challenge: Supply Chain Disruptions

**Problem:**
- Component shortages (chips, rare materials)
- Shipping delays (port congestion)
- Trade restrictions and tariffs

**Solutions:**
- Dual sourcing strategies
- Safety stock for critical components
- Local manufacturing development
- Long-term supplier contracts
- Supply chain visibility tools

### Challenge: Transportation Logistics

**Problem:**
- Oversized component transportation
- Infrastructure limitations (roads, bridges)
- Permitting complexities
- High transportation costs

**Solutions:**
- Route surveys and planning
- Infrastructure upgrades (cost-benefit)
- Modular designs (smaller components)
- Regional manufacturing/assembly
- Just-in-sequence delivery

### Challenge: Weather-Dependent Installation

**Problem:**
- Crane operations limited by wind
- Seasonal weather patterns
- Schedule delays and cost overruns

**Solutions:**
- Weather window analysis
- Flexible scheduling with buffers
- Weather forecasting and monitoring
- Alternative installation methods
- Weather-based risk modeling

### Challenge: Grid Integration Delays

**Problem:**
- Limited grid capacity
- Interconnection queue backlogs
- Curtailment of renewable generation

**Solutions:**
- Early grid studies and applications
- Energy storage pairing
- Power purchase agreements (PPAs)
- Transmission planning coordination
- Grid upgrade cost-sharing

### Challenge: Maintenance Access

**Problem:**
- Remote site locations
- Limited service infrastructure
- Parts availability
- Technician training

**Solutions:**
- Predictive maintenance (reduce trips)
- Mobile service units
- Spare parts inventory optimization
- Remote monitoring and diagnostics
- Local training programs

---

## Output Format

### Renewable Energy Project Plan

**Executive Summary:**
- Project overview (type, capacity, location)
- Total project cost and timeline
- Key supply chain strategies
- Risk mitigation approach

**Supply Chain Plan:**

| Component | Supplier | Lead Time | Cost | Delivery Date |
|-----------|----------|-----------|------|---------------|
| Solar Panels (250 MW) | Supplier_A | 90 days | $35M | 2026-08-15 |
| Inverters | Supplier_B | 60 days | $8M | 2026-09-01 |
| Racking | Supplier_C | 75 days | $12M | 2026-08-20 |

**Logistics Plan:**

| Component | Origin | Mode | Route | Duration | Cost |
|-----------|--------|------|-------|----------|------|
| Panels | Shanghai | Ocean+Truck | Port of LA | 45 days | $2.5M |
| Inverters | Phoenix | Truck | Direct | 2 days | $150K |

**Installation Schedule:**

| Phase | Duration | Start Date | End Date | Key Activities |
|-------|----------|------------|----------|----------------|
| Site Prep | 30 days | 2026-07-01 | 2026-07-30 | Grading, foundations |
| Module Install | 60 days | 2026-08-15 | 2026-10-15 | Panel installation |
| Electrical | 30 days | 2026-10-01 | 2026-10-30 | Wiring, inverters |
| Commissioning | 15 days | 2026-11-01 | 2026-11-15 | Testing, grid connection |

**Risk Assessment:**

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Component delay | High | Medium | Safety stock, alternative suppliers |
| Weather delays | Medium | Medium | Schedule buffer, weather tracking |
| Grid interconnection | High | Low | Early application, coordination |

---

## Questions to Ask

If you need more context:
1. What type of renewable energy? (solar, wind, hydro, other)
2. What's the project scale and capacity?
3. What stage are you in? (planning, construction, operation)
4. What's the geographic location?
5. What are the key constraints? (budget, timeline, regulatory)
6. What supply chain elements need optimization?
7. What are the primary risks and concerns?

---

## Related Skills

- **energy-logistics**: For overall energy supply chain management
- **power-grid-optimization**: For grid integration and transmission
- **energy-storage-optimization**: For battery and storage systems
- **network-design**: For facility location and network optimization
- **project-scheduling**: For construction and installation scheduling
- **demand-forecasting**: For energy generation forecasting
- **risk-mitigation**: For supply chain risk management
- **sustainable-sourcing**: For responsible material sourcing
