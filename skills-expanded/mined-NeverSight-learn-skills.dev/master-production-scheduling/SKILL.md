---
name: master-production-scheduling
description: When the user wants to create detailed production schedules, develop MPS, manage production planning, or translate S&OP to execution. Also use when the user mentions "MPS," "production plan," "available-to-promise," "master schedule," "rough-cut capacity planning," "time-phased planning," "planned orders," or "MRP input." For shop floor scheduling, see production-scheduling. For aggregate planning, see sales-operations-planning.
---

# Master Production Scheduling (MPS)

You are an expert in Master Production Scheduling (MPS) and production planning. Your goal is to help organizations create feasible, optimized production schedules that balance demand requirements with capacity constraints while maximizing efficiency and service levels.

## Initial Assessment

Before developing the MPS, understand:

1. **Planning Environment**
   - Manufacturing type? (make-to-stock, make-to-order, assemble-to-order, engineer-to-order)
   - Production process? (discrete, process, repetitive, batch)
   - Planning horizon? (weeks, months)
   - Planning bucket size? (daily, weekly)

2. **Product & Demand**
   - Number of end items/SKUs?
   - Product structure complexity? (single level, multi-level BOM)
   - Demand patterns? (stable, seasonal, lumpy)
   - Customer order lead times vs. manufacturing lead times?

3. **Capacity & Constraints**
   - Critical resources and bottlenecks?
   - Changeover/setup times significant?
   - Workforce availability and skills?
   - Material constraints?

4. **Current State**
   - Existing MPS process?
   - ERP/MRP system in place?
   - Schedule adherence rates?
   - Inventory levels (raw materials, WIP, finished goods)?

---

## MPS Framework

### MPS Definition

**Master Production Schedule (MPS)** is a time-phased plan that specifies how many of each end item will be produced and when. It disaggregates the aggregate production plan (from S&OP) into a specific build schedule for individual products.

**Key Characteristics:**
- **Time-phased**: Specific quantities by time period
- **Item-level**: End items or planning items
- **Feasible**: Respects capacity and material constraints
- **Firm zone**: Near-term frozen, far-term flexible
- **Drives MRP**: Input to Material Requirements Planning

### MPS vs. Related Plans

| Plan Type | Horizon | Level | Frequency | Purpose |
|-----------|---------|-------|-----------|---------|
| **S&OP** | 12-18 mo | Product family | Monthly | Align demand/supply |
| **MPS** | 3-6 mo | End item | Weekly | Detailed production plan |
| **MRP** | 3-6 mo | Component | Daily/Weekly | Material requirements |
| **Shop Floor Schedule** | Days-weeks | Operation | Daily | Detailed sequencing |

---

## MPS Planning Process

### Step 1: Review Demand Requirements

**Sources of Demand:**

1. **Forecast Demand**
   - Statistical forecast from demand planning
   - Marketing/sales input
   - Seasonality and trends

2. **Customer Orders**
   - Booked orders
   - Firm commitments
   - Contracts

3. **Safety Stock Requirements**
   - Buffer inventory targets
   - Service level policies

4. **Interplant Transfers**
   - Distribution requirements
   - Network demand

5. **Service Parts**
   - Aftermarket demand
   - Warranty requirements

**Demand Aggregation:**

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MpsDemandPlanning:
    """Aggregate demand sources for MPS"""

    def __init__(self, planning_horizon_weeks=26):
        self.horizon = planning_horizon_weeks
        self.demand_sources = []

    def add_forecast_demand(self, item, periods, quantities):
        """Add forecasted demand"""
        self.demand_sources.append({
            'source': 'forecast',
            'item': item,
            'periods': periods,
            'quantities': quantities
        })

    def add_customer_orders(self, item, periods, quantities):
        """Add firm customer orders"""
        self.demand_sources.append({
            'source': 'customer_orders',
            'item': item,
            'periods': periods,
            'quantities': quantities
        })

    def add_safety_stock(self, item, target_level):
        """Add safety stock requirement"""
        self.demand_sources.append({
            'source': 'safety_stock',
            'item': item,
            'target': target_level
        })

    def calculate_total_demand(self):
        """
        Calculate total demand by item and period

        Uses consumption logic:
        - Customer orders consume forecast in near term
        - Forecast used beyond order horizon
        """

        # Create time buckets
        start_date = datetime.now()
        periods = pd.date_range(start_date, periods=self.horizon, freq='W')

        all_items = set()
        for source in self.demand_sources:
            all_items.add(source['item'])

        demand_df = pd.DataFrame({
            'period': periods
        })

        for item in all_items:
            # Get forecast
            forecast = self._get_source_demand(item, 'forecast', periods)

            # Get customer orders
            orders = self._get_source_demand(item, 'customer_orders', periods)

            # Apply consumption logic: greater of forecast or orders
            total_demand = np.maximum(forecast, orders)

            demand_df[f'{item}_forecast'] = forecast
            demand_df[f'{item}_orders'] = orders
            demand_df[f'{item}_total'] = total_demand

        return demand_df

    def _get_source_demand(self, item, source_type, periods):
        """Extract demand for specific item and source"""

        quantities = np.zeros(len(periods))

        for source in self.demand_sources:
            if source['item'] == item and source['source'] == source_type:
                if 'periods' in source:
                    for i, period in enumerate(source['periods']):
                        if i < len(quantities):
                            quantities[i] = source['quantities'][i]

        return quantities

# Example usage
mps_demand = MpsDemandPlanning(planning_horizon_weeks=12)

# Add forecast
periods = list(range(12))
forecast_qty = [100, 110, 105, 120, 115, 125, 130, 120, 115, 110, 120, 125]
mps_demand.add_forecast_demand('Product_A', periods, forecast_qty)

# Add firm customer orders (first 4 weeks)
orders = [150, 130, 0, 0] + [0] * 8
mps_demand.add_customer_orders('Product_A', periods, orders)

# Calculate total demand
total_demand = mps_demand.calculate_total_demand()
print("MPS Demand by Week:")
print(total_demand[['period', 'Product_A_forecast', 'Product_A_orders', 'Product_A_total']])
```

### Step 2: Develop Preliminary MPS

**MPS Logic:**

```
Projected Available Balance (PAB) formula:
PAB[t] = PAB[t-1] + MPS[t] - max(Forecast[t], Orders[t])

When PAB[t] < Safety Stock:
  Schedule MPS receipt
```

**MPS Planning Table:**

| Period | Forecast | Orders | Total | Proj. Avail | MPS | ATP |
|--------|----------|--------|-------|-------------|-----|-----|
| 1 | 100 | 150 | 150 | 50 | 200 | 50 |
| 2 | 110 | 130 | 130 | 120 | 0 | 0 |
| 3 | 105 | 0 | 105 | 15 | 100 | 100 |

```python
import pandas as pd
import numpy as np

class MasterProductionSchedule:
    """Master Production Schedule generator"""

    def __init__(self, item, beginning_inventory,
                 safety_stock, lot_size, lead_time):
        """
        Parameters:
        - item: product identifier
        - beginning_inventory: starting inventory level
        - safety_stock: minimum inventory target
        - lot_size: production lot size (0 = lot-for-lot)
        - lead_time: production lead time (periods)
        """
        self.item = item
        self.beginning_inventory = beginning_inventory
        self.safety_stock = safety_stock
        self.lot_size = lot_size
        self.lead_time = lead_time

    def generate_mps(self, forecast, customer_orders, periods):
        """
        Generate MPS using standard MPS logic

        Returns DataFrame with MPS planning table
        """

        mps_table = []

        projected_available = self.beginning_inventory
        cumulative_mps = 0

        for t in range(periods):
            # Total demand (greater of forecast or orders)
            fcst = forecast[t] if t < len(forecast) else 0
            orders = customer_orders[t] if t < len(customer_orders) else 0
            total_demand = max(fcst, orders)

            # Check if MPS receipt needed
            if projected_available - total_demand < self.safety_stock:
                # Schedule MPS receipt
                shortage = self.safety_stock - (projected_available - total_demand)

                if self.lot_size > 0:
                    # Fixed lot size
                    lots_needed = int(np.ceil(shortage / self.lot_size))
                    mps_quantity = lots_needed * self.lot_size
                else:
                    # Lot-for-lot
                    mps_quantity = shortage

                # Account for lead time (schedule in future period)
                mps_receipt_period = t
            else:
                mps_quantity = 0
                mps_receipt_period = t

            # Update projected available
            projected_available = projected_available + mps_quantity - total_demand

            # Calculate Available-to-Promise (ATP)
            # ATP[t] = MPS[t] - sum(orders from t to next MPS)
            if mps_quantity > 0:
                atp = mps_quantity - orders
            else:
                atp = 0

            mps_table.append({
                'period': t + 1,
                'forecast': fcst,
                'customer_orders': orders,
                'total_demand': total_demand,
                'projected_available': max(0, projected_available),
                'mps_quantity': mps_quantity,
                'atp': max(0, atp)
            })

        return pd.DataFrame(mps_table)

    def calculate_rough_cut_capacity(self, mps_table, routing_time_per_unit):
        """
        Rough-Cut Capacity Planning (RCCP)

        Check if MPS is feasible given capacity

        Parameters:
        - mps_table: output from generate_mps
        - routing_time_per_unit: hours required per unit
        """

        mps_table['required_hours'] = (
            mps_table['mps_quantity'] * routing_time_per_unit
        )

        return mps_table[['period', 'mps_quantity', 'required_hours']]

# Example
mps = MasterProductionSchedule(
    item='Product_A',
    beginning_inventory=200,
    safety_stock=50,
    lot_size=100,  # Fixed lot size of 100
    lead_time=2
)

# Demand data
forecast = [100, 110, 105, 120, 115, 125, 130, 120, 115, 110, 120, 125]
customer_orders = [150, 130, 80, 90] + [0] * 8

# Generate MPS
mps_plan = mps.generate_mps(forecast, customer_orders, periods=12)
print("Master Production Schedule:")
print(mps_plan)

# Rough-cut capacity
rccp = mps.calculate_rough_cut_capacity(mps_plan, routing_time_per_unit=2.5)
print("\nRough-Cut Capacity Requirements:")
print(rccp)
```

### Step 3: Rough-Cut Capacity Planning (RCCP)

**Purpose:** Validate MPS is feasible given capacity constraints

**Process:**
1. Calculate resource requirements from MPS
2. Compare to available capacity
3. Identify overloads
4. Adjust MPS or capacity

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class RoughCutCapacityPlanning:
    """RCCP - Validate MPS feasibility"""

    def __init__(self, work_centers):
        """
        Parameters:
        - work_centers: dict {name: {'capacity_hours': x, 'efficiency': y}}
        """
        self.work_centers = work_centers

    def validate_mps(self, mps_schedule, routings):
        """
        Check if MPS is feasible

        Parameters:
        - mps_schedule: DataFrame with 'item', 'period', 'mps_quantity'
        - routings: dict {item: [(work_center, hours_per_unit)]}

        Returns capacity analysis
        """

        requirements = []

        for idx, row in mps_schedule.iterrows():
            item = row['item']
            period = row['period']
            quantity = row['mps_quantity']

            if quantity == 0:
                continue

            # Get routing for item
            routing = routings.get(item, [])

            for work_center, hours_per_unit in routing:
                # Calculate required hours
                efficiency = self.work_centers[work_center]['efficiency']
                required_hours = (quantity * hours_per_unit) / efficiency

                requirements.append({
                    'period': period,
                    'work_center': work_center,
                    'item': item,
                    'quantity': quantity,
                    'required_hours': required_hours
                })

        req_df = pd.DataFrame(requirements)

        # Aggregate by work center and period
        capacity_analysis = req_df.groupby(
            ['period', 'work_center']
        )['required_hours'].sum().reset_index()

        # Add available capacity
        capacity_analysis['available_capacity'] = capacity_analysis['work_center'].map(
            lambda wc: self.work_centers[wc]['capacity_hours']
        )

        # Calculate load %
        capacity_analysis['load_pct'] = (
            capacity_analysis['required_hours'] /
            capacity_analysis['available_capacity'] * 100
        )

        capacity_analysis['status'] = capacity_analysis['load_pct'].apply(
            lambda x: 'Overload' if x > 100 else
                     'High' if x > 90 else
                     'OK'
        )

        return capacity_analysis

    def identify_overloads(self, capacity_analysis):
        """Get periods and resources with overload"""
        return capacity_analysis[capacity_analysis['status'] == 'Overload']

    def plot_capacity_profile(self, capacity_analysis):
        """Visualize capacity load"""

        work_centers = capacity_analysis['work_center'].unique()

        fig, axes = plt.subplots(len(work_centers), 1,
                                figsize=(12, 4 * len(work_centers)),
                                squeeze=False)

        for i, wc in enumerate(work_centers):
            wc_data = capacity_analysis[
                capacity_analysis['work_center'] == wc
            ].sort_values('period')

            ax = axes[i, 0]

            # Plot capacity line
            ax.axhline(y=wc_data['available_capacity'].iloc[0],
                      color='green', linestyle='--',
                      linewidth=2, label='Available Capacity')

            # Plot requirements
            bars = ax.bar(wc_data['period'], wc_data['required_hours'],
                         alpha=0.7)

            # Color overloads red
            for j, (idx, row) in enumerate(wc_data.iterrows()):
                if row['status'] == 'Overload':
                    bars[j].set_color('red')

            ax.set_title(f'{wc} - Capacity Load')
            ax.set_xlabel('Period')
            ax.set_ylabel('Hours')
            ax.legend()
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example
work_centers = {
    'Assembly': {'capacity_hours': 160, 'efficiency': 0.90},
    'Testing': {'capacity_hours': 120, 'efficiency': 0.95},
    'Packaging': {'capacity_hours': 140, 'efficiency': 0.92}
}

rccp = RoughCutCapacityPlanning(work_centers)

# MPS schedule (from previous example)
mps_schedule = pd.DataFrame({
    'item': ['Product_A'] * 12,
    'period': range(1, 13),
    'mps_quantity': [200, 0, 100, 200, 0, 100, 200, 0, 100, 200, 0, 100]
})

# Routings
routings = {
    'Product_A': [
        ('Assembly', 1.5),
        ('Testing', 0.8),
        ('Packaging', 0.5)
    ]
}

# Validate MPS
capacity_check = rccp.validate_mps(mps_schedule, routings)
print("Capacity Analysis:")
print(capacity_check)

# Identify overloads
overloads = rccp.identify_overloads(capacity_check)
if not overloads.empty:
    print("\nOverloaded Resources:")
    print(overloads)
else:
    print("\nNo capacity overloads - MPS is feasible")

# Plot
rccp.plot_capacity_profile(capacity_check)
```

### Step 4: Available-to-Promise (ATP)

**ATP Definition:** Uncommitted portion of inventory and planned production

**ATP Rules:**
- First period: On-hand + MPS - Customer orders
- Subsequent periods: MPS - Customer orders (until next MPS)

**ATP Calculation:**

```python
class AvailableToPromise:
    """Calculate ATP for order promising"""

    def __init__(self, mps_table, on_hand_inventory):
        self.mps = mps_table
        self.on_hand = on_hand_inventory

    def calculate_atp(self):
        """
        Calculate Available-to-Promise

        ATP provides visibility for order promising
        """

        atp_table = self.mps.copy()
        atp_table['atp'] = 0

        for i in range(len(atp_table)):
            if i == 0:
                # First period: On-hand + MPS - Orders
                atp_table.loc[i, 'atp'] = (
                    self.on_hand +
                    atp_table.loc[i, 'mps_quantity'] -
                    atp_table.loc[i, 'customer_orders']
                )
            else:
                # Check if MPS in this period
                if atp_table.loc[i, 'mps_quantity'] > 0:
                    # ATP = MPS - orders from this period until next MPS
                    orders_to_next_mps = 0

                    # Look ahead for orders until next MPS
                    for j in range(i, len(atp_table)):
                        orders_to_next_mps += atp_table.loc[j, 'customer_orders']

                        # Stop at next MPS
                        if j > i and atp_table.loc[j, 'mps_quantity'] > 0:
                            break

                    atp_table.loc[i, 'atp'] = (
                        atp_table.loc[i, 'mps_quantity'] - orders_to_next_mps
                    )

        return atp_table

    def check_order_promise(self, order_quantity, requested_period):
        """
        Check if order can be promised

        Returns: (can_promise, available_period)
        """

        atp_table = self.calculate_atp()

        # Check requested period first
        if requested_period <= len(atp_table):
            cumulative_atp = atp_table.loc[:requested_period-1, 'atp'].sum()

            if cumulative_atp >= order_quantity:
                return True, requested_period

        # Find earliest period with enough ATP
        cumulative = 0
        for i in range(len(atp_table)):
            cumulative += atp_table.loc[i, 'atp']

            if cumulative >= order_quantity:
                return True, i + 1

        # Cannot promise
        return False, None

# Example
mps_table = pd.DataFrame({
    'period': [1, 2, 3, 4, 5, 6],
    'forecast': [100, 110, 105, 120, 115, 125],
    'customer_orders': [80, 70, 50, 30, 0, 0],
    'mps_quantity': [200, 0, 150, 0, 0, 200],
    'projected_available': [120, 50, 195, 75, 75, 150]
})

atp = AvailableToPromise(mps_table, on_hand_inventory=100)

# Calculate ATP
atp_results = atp.calculate_atp()
print("Available-to-Promise:")
print(atp_results[['period', 'mps_quantity', 'customer_orders', 'atp']])

# Check if can promise order
can_promise, period = atp.check_order_promise(order_quantity=150, requested_period=2)
if can_promise:
    print(f"\n✓ Can promise 150 units by period {period}")
else:
    print("\n✗ Cannot promise order")
```

### Step 5: Freeze and Release MPS

**Time Fences:**

```
|<-- Frozen Zone -->|<-- Slushy Zone -->|<-- Liquid Zone -->|
       2-4 weeks          4-8 weeks           8+ weeks

Frozen: No changes without executive approval
Slushy: Changes with planner approval
Liquid: Flexible, planning purposes only
```

**Freeze Policy:**

```python
from datetime import datetime, timedelta

class MpsTimeFences:
    """Manage MPS time fences and change control"""

    def __init__(self, frozen_weeks, slushy_weeks):
        self.frozen_weeks = frozen_weeks
        self.slushy_weeks = slushy_weeks

    def get_zone(self, period_date):
        """Determine time fence zone for a period"""

        now = datetime.now()
        frozen_end = now + timedelta(weeks=self.frozen_weeks)
        slushy_end = now + timedelta(weeks=self.frozen_weeks + self.slushy_weeks)

        if period_date <= frozen_end:
            return 'Frozen'
        elif period_date <= slushy_end:
            return 'Slushy'
        else:
            return 'Liquid'

    def approve_change(self, period_date, change_type, authority_level):
        """
        Check if change is allowed

        Parameters:
        - change_type: 'quantity', 'timing', 'cancellation'
        - authority_level: 'planner', 'manager', 'executive'

        Returns: (approved, reason)
        """

        zone = self.get_zone(period_date)

        if zone == 'Frozen':
            if authority_level == 'executive':
                return True, 'Executive approval in frozen zone'
            else:
                return False, 'Changes require executive approval in frozen zone'

        elif zone == 'Slushy':
            if authority_level in ['manager', 'executive']:
                return True, 'Manager approval in slushy zone'
            else:
                return False, 'Changes require manager approval in slushy zone'

        else:  # Liquid
            return True, 'Free to change in liquid zone'

    def mps_release(self, mps_table):
        """
        Release MPS with time fence zones marked

        Returns MPS with zones and change authority
        """

        mps_released = mps_table.copy()

        # Assume period is datetime
        mps_released['zone'] = mps_released['period'].apply(self.get_zone)

        mps_released['change_authority'] = mps_released['zone'].map({
            'Frozen': 'Executive',
            'Slushy': 'Manager',
            'Liquid': 'Planner'
        })

        return mps_released

# Example
fences = MpsTimeFences(frozen_weeks=4, slushy_weeks=4)

# Check change approval
period = datetime.now() + timedelta(weeks=2)
approved, reason = fences.approve_change(period, 'quantity', authority_level='planner')
print(f"Change approval: {approved}")
print(f"Reason: {reason}")
```

---

## MPS Strategies by Manufacturing Environment

### Make-to-Stock (MTS)

**Characteristics:**
- Produce to forecast
- Maintain finished goods inventory
- Fast customer delivery

**MPS Approach:**
- Schedule based on forecast + safety stock
- Level loading preferred
- Replenishment triggers (min/max, EOQ)

```python
def mts_mps_logic(forecast, current_inventory, safety_stock,
                  target_inventory, lot_size):
    """
    Make-to-Stock MPS logic

    Schedule production to maintain target inventory
    """

    mps_schedule = []

    inventory = current_inventory

    for period, demand in enumerate(forecast):
        # Check if replenishment needed
        projected_inventory = inventory - demand

        if projected_inventory < safety_stock:
            # Order up to target
            order_quantity = target_inventory - projected_inventory

            # Round to lot size
            if lot_size > 0:
                lots = int(np.ceil(order_quantity / lot_size))
                order_quantity = lots * lot_size

            inventory = projected_inventory + order_quantity
        else:
            order_quantity = 0
            inventory = projected_inventory

        mps_schedule.append({
            'period': period + 1,
            'demand': demand,
            'mps_quantity': order_quantity,
            'ending_inventory': inventory
        })

    return pd.DataFrame(mps_schedule)

# Example
forecast = [100, 110, 105, 120, 115, 125, 130, 120]
mts_plan = mts_mps_logic(
    forecast=forecast,
    current_inventory=200,
    safety_stock=50,
    target_inventory=250,
    lot_size=100
)
print("Make-to-Stock MPS:")
print(mts_plan)
```

### Make-to-Order (MTO)

**Characteristics:**
- Produce only for specific customer orders
- No finished goods inventory
- Longer customer lead times

**MPS Approach:**
- Schedule based on customer orders
- Backward scheduling from due date
- Order promising via ATP

```python
def mto_mps_logic(customer_orders, production_lead_time):
    """
    Make-to-Order MPS logic

    Schedule production to meet order due dates
    """

    mps_schedule = []

    for order in customer_orders:
        order_id = order['order_id']
        quantity = order['quantity']
        due_date = order['due_date']

        # Backward schedule: start = due date - lead time
        start_period = due_date - production_lead_time

        mps_schedule.append({
            'order_id': order_id,
            'start_period': max(1, start_period),
            'due_period': due_date,
            'quantity': quantity,
            'order_type': 'customer_order'
        })

    return pd.DataFrame(mps_schedule)

# Example
orders = [
    {'order_id': 'ORD-001', 'quantity': 50, 'due_date': 5},
    {'order_id': 'ORD-002', 'quantity': 75, 'due_date': 7},
    {'order_id': 'ORD-003', 'quantity': 60, 'due_date': 10}
]

mto_plan = mto_mps_logic(orders, production_lead_time=3)
print("Make-to-Order MPS:")
print(mto_plan)
```

### Assemble-to-Order (ATO)

**Characteristics:**
- Stock components, final assembly on order
- High product variety from common components
- Moderate lead times

**MPS Approach:**
- Two-level MPS:
  1. Component/module level (forecast-driven)
  2. Final assembly (order-driven)
- Planning bill of materials
- Final assembly schedule (FAS)

```python
class AssembleToOrderMPS:
    """ATO with planning bills and final assembly schedule"""

    def __init__(self, planning_bill):
        """
        planning_bill: dict {option: {component: percentage}}

        Example:
        {
            'Base_Model': {'Frame': 1.0, 'Engine_A': 0.6, 'Engine_B': 0.4},
            ...
        }
        """
        self.planning_bill = planning_bill

    def generate_component_mps(self, demand_forecast, planning_item):
        """
        Generate MPS for components based on option percentages

        Parameters:
        - demand_forecast: forecast for planning item
        - planning_item: aggregate product family
        """

        component_forecast = {}

        for component, percentage in self.planning_bill[planning_item].items():
            component_forecast[component] = [
                qty * percentage for qty in demand_forecast
            ]

        return component_forecast

    def create_final_assembly_schedule(self, customer_orders,
                                      assembly_lead_time):
        """
        Create FAS from customer orders

        FAS specifies exact configuration to build
        """

        fas = []

        for order in customer_orders:
            config = order['configuration']
            quantity = order['quantity']
            due_date = order['due_date']

            start_date = max(1, due_date - assembly_lead_time)

            fas.append({
                'order_id': order['order_id'],
                'configuration': config,
                'quantity': quantity,
                'start_period': start_date,
                'due_period': due_date
            })

        return pd.DataFrame(fas)

# Example
planning_bill = {
    'Laptop': {
        'Base_Unit': 1.0,
        'CPU_i5': 0.6,
        'CPU_i7': 0.4,
        'RAM_8GB': 0.5,
        'RAM_16GB': 0.5,
        'SSD_256GB': 0.7,
        'SSD_512GB': 0.3
    }
}

ato = AssembleToOrderMPS(planning_bill)

# Forecast for planning item
laptop_forecast = [100, 110, 105, 120, 115, 125]

# Generate component MPS
component_mps = ato.generate_component_mps(laptop_forecast, 'Laptop')
print("Component MPS (Forecast-Driven):")
for component, forecast in component_mps.items():
    print(f"  {component}: {forecast[:4]}")

# Customer orders with specific configurations
orders = [
    {
        'order_id': 'ORD-001',
        'configuration': 'i7/16GB/512GB',
        'quantity': 50,
        'due_date': 3
    },
    {
        'order_id': 'ORD-002',
        'configuration': 'i5/8GB/256GB',
        'quantity': 75,
        'due_date': 5
    }
]

# Final assembly schedule
fas = ato.create_final_assembly_schedule(orders, assembly_lead_time=1)
print("\nFinal Assembly Schedule (Order-Driven):")
print(fas)
```

---

## MPS Optimization Techniques

### Level Loading

**Objective:** Smooth production to minimize variability

**Approach:**
- Calculate average demand
- Produce at constant rate
- Use inventory as buffer

```python
def level_loading_mps(total_demand, periods, lot_size=0):
    """
    Level loading - produce at constant rate

    Parameters:
    - total_demand: total demand over horizon
    - periods: number of periods
    - lot_size: production lot size (0 = continuous)
    """

    # Calculate average per period
    avg_demand = total_demand / periods

    # Round to lot size if applicable
    if lot_size > 0:
        level_quantity = int(np.ceil(avg_demand / lot_size)) * lot_size
    else:
        level_quantity = avg_demand

    # Create level schedule
    mps = [level_quantity] * periods

    return mps

# Example
total_demand = 1200
periods = 10

level_mps = level_loading_mps(total_demand, periods, lot_size=50)
print(f"Level Loading MPS: {level_mps}")
print(f"Average production per period: {sum(level_mps)/len(level_mps):.0f}")
```

### Chase Strategy

**Objective:** Match production to demand exactly

**Approach:**
- Vary production rate with demand
- Minimize inventory
- Higher costs (hiring/firing, setup)

```python
def chase_strategy_mps(demand_forecast, lot_size=0):
    """
    Chase strategy - match production to demand

    Parameters:
    - demand_forecast: demand by period
    - lot_size: minimum production quantity
    """

    mps = []

    for demand in demand_forecast:
        if lot_size > 0:
            # Round up to lot size
            quantity = int(np.ceil(demand / lot_size)) * lot_size
        else:
            quantity = demand

        mps.append(quantity)

    return mps

# Example
demand = [100, 120, 90, 150, 110, 130, 95, 140]
chase_mps = chase_strategy_mps(demand, lot_size=50)
print(f"Chase Strategy MPS: {chase_mps}")
```

### Mixed Strategy (Hybrid)

**Objective:** Balance inventory costs and production variability

**Approach:**
- Level production for base demand
- Use overtime, subcontracting, or inventory for peaks

```python
from pulp import *

def mixed_strategy_mps(demand, costs, capacity_normal, capacity_overtime):
    """
    Mixed strategy optimization

    Minimize total cost of production + inventory + backorders

    Parameters:
    - demand: list of demand by period
    - costs: dict {'regular': x, 'overtime': y, 'inventory': z, 'backorder': w}
    - capacity_normal: regular capacity per period
    - capacity_overtime: max overtime capacity per period
    """

    periods = len(demand)

    # Create problem
    prob = LpProblem("Mixed_Strategy_MPS", LpMinimize)

    # Variables
    P = LpVariable.dicts("Regular", range(periods), lowBound=0)
    O = LpVariable.dicts("Overtime", range(periods), lowBound=0)
    I = LpVariable.dicts("Inventory", range(periods), lowBound=0)
    B = LpVariable.dicts("Backorder", range(periods), lowBound=0)

    # Objective
    prob += lpSum([
        costs['regular'] * P[t] +
        costs['overtime'] * O[t] +
        costs['inventory'] * I[t] +
        costs['backorder'] * B[t]
        for t in range(periods)
    ])

    # Constraints
    for t in range(periods):
        # Capacity
        prob += P[t] <= capacity_normal
        prob += O[t] <= capacity_overtime

        # Inventory balance
        if t == 0:
            prob += I[t] == P[t] + O[t] - demand[t] + B[t]
        else:
            prob += I[t] == I[t-1] + P[t] + O[t] - demand[t] + B[t] - B[t-1]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    solution = {
        'regular': [P[t].varValue for t in range(periods)],
        'overtime': [O[t].varValue for t in range(periods)],
        'inventory': [I[t].varValue for t in range(periods)],
        'backorder': [B[t].varValue for t in range(periods)],
        'total_cost': value(prob.objective)
    }

    return solution

# Example
demand = [100, 120, 150, 180, 160, 140, 120, 110]

costs = {
    'regular': 50,
    'overtime': 75,
    'inventory': 5,
    'backorder': 100
}

mixed_mps = mixed_strategy_mps(
    demand=demand,
    costs=costs,
    capacity_normal=120,
    capacity_overtime=40
)

print("Mixed Strategy MPS:")
print(f"Total Cost: ${mixed_mps['total_cost']:,.0f}")
print(f"Regular Production: {[int(x) for x in mixed_mps['regular']]}")
print(f"Overtime Production: {[int(x) for x in mixed_mps['overtime']]}")
print(f"Ending Inventory: {[int(x) for x in mixed_mps['inventory']]}")
```

---

## MPS Performance Metrics

### Schedule Adherence

**MPS Attainment:**
```
Actual Production / Planned Production × 100%
```

Target: >95%

### Inventory Metrics

**Inventory Turnover:**
```
COGS / Average Inventory
```

**Days of Inventory:**
```
(Average Inventory / Daily Demand) × Days
```

### Customer Service

**On-Time Delivery:**
```
Orders Delivered On-Time / Total Orders × 100%
```

Target: >95%

**Order Fill Rate:**
```
Orders Filled Complete / Total Orders × 100%
```

### Planning Metrics

**Planning Nervousness:**
- Measures schedule instability
- Count of changes to frozen MPS

**ATP Accuracy:**
- Promised vs. actual delivery performance

```python
class MPSMetrics:
    """Track MPS performance metrics"""

    def __init__(self):
        self.periods = []

    def add_period(self, planned, actual, inventory, orders_on_time, total_orders):
        """Record period performance"""

        self.periods.append({
            'planned_production': planned,
            'actual_production': actual,
            'ending_inventory': inventory,
            'orders_on_time': orders_on_time,
            'total_orders': total_orders
        })

    def calculate_metrics(self):
        """Calculate summary metrics"""

        df = pd.DataFrame(self.periods)

        metrics = {
            'mps_attainment': (df['actual_production'].sum() /
                              df['planned_production'].sum() * 100),
            'avg_inventory': df['ending_inventory'].mean(),
            'on_time_delivery': (df['orders_on_time'].sum() /
                                df['total_orders'].sum() * 100)
        }

        return metrics

# Example
metrics = MPSMetrics()

# Add several periods
for i in range(6):
    metrics.add_period(
        planned=200,
        actual=np.random.randint(185, 205),
        inventory=np.random.randint(80, 120),
        orders_on_time=np.random.randint(18, 20),
        total_orders=20
    )

summary = metrics.calculate_metrics()
print("MPS Performance Metrics:")
for metric, value in summary.items():
    print(f"  {metric}: {value:.1f}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`: Linear programming for MPS optimization
- `pyomo`: Advanced optimization
- `scipy.optimize`: Optimization algorithms

**Data Management:**
- `pandas`: Time series and data manipulation
- `numpy`: Numerical computations

**Visualization:**
- `matplotlib`, `seaborn`: Gantt charts, capacity profiles
- `plotly`: Interactive schedules

### Commercial MPS Software

**ERP Systems with MPS:**
- **SAP**: MRP/MPS modules
- **Oracle**: Advanced Supply Chain Planning
- **Microsoft Dynamics**: Master Planning
- **Infor**: Production Planning

**Specialized Planning:**
- **Kinaxis RapidResponse**: Real-time planning
- **Blue Yonder**: Demand-driven MPS
- **o9 Solutions**: AI-powered planning
- **Anaplan**: Cloud-based planning

**Shop Floor Integration:**
- **Plex**: Manufacturing MPS
- **IQMS**: MRP/MPS for manufacturing
- **Epicor**: Production management

---

## Common Challenges & Solutions

### Challenge: Frozen Zone Too Short

**Problem:**
- Constant schedule changes
- Production disruption
- Low attainment

**Solutions:**
- Extend frozen zone (4-6 weeks typical)
- Reduce lead times to shorten freeze needed
- Improve forecast accuracy
- Enforce change control policies
- Buffer with safety stock

### Challenge: Overloaded Capacity

**Problem:**
- RCCP shows capacity shortfall
- Cannot meet MPS

**Solutions:**
- Add shifts or overtime
- Outsource/subcontract
- Reduce demand (allocation)
- Increase lead times
- Capital investment (long-term)

### Challenge: Poor Schedule Adherence

**Problem:**
- Actual production doesn't match MPS
- Firefighting and expediting

**Solutions:**
- Improve shop floor execution
- Better material availability (MRP)
- Reduce variability (quality, uptime)
- Realistic MPS (don't overplan)
- Root cause analysis on misses

### Challenge: Lumpy MPS (Lot Sizing)

**Problem:**
- Large lot sizes create peaks/valleys
- Capacity swings
- Inventory buildup

**Solutions:**
- Reduce setup times (SMED)
- Smaller lot sizes
- Level loading approach
- Mixed-model scheduling
- Lean manufacturing principles

### Challenge: Nervousness (Too Many Changes)

**Problem:**
- MPS changes frequently
- Planner credibility issues
- Shop floor confusion

**Solutions:**
- Stricter time fences
- Improve forecast accuracy
- Demand filtering/dampening
- Manage customer expectations
- Better S&OP process

---

## Output Format

### MPS Report Structure

**MPS Planning Table:**

| Week | Forecast | Customer Orders | Total Demand | Proj. Available | MPS | ATP | Zone |
|------|----------|----------------|--------------|----------------|-----|-----|------|
| 1 | 100 | 150 | 150 | 50 | 200 | 50 | Frozen |
| 2 | 110 | 130 | 130 | 120 | 0 | 0 | Frozen |
| 3 | 105 | 80 | 105 | 15 | 100 | 20 | Frozen |
| 4 | 120 | 60 | 120 | -5 | 200 | 140 | Slushy |
| 5 | 115 | 0 | 115 | 80 | 0 | 0 | Slushy |
| 6 | 125 | 0 | 125 | -45 | 200 | 200 | Liquid |

**Capacity Load Summary:**

| Work Center | Week 1 | Week 2 | Week 3 | Week 4 | Available | Status |
|-------------|--------|--------|--------|--------|-----------|---------|
| Assembly | 145 | 120 | 130 | 160 | 160 | OK |
| Testing | 95 | 85 | 90 | 110 | 120 | OK |
| Packaging | 70 | 60 | 65 | 80 | 80 | OK |

**MPS Changes from Last Week:**

| Item | Week | Old Quantity | New Quantity | Change | Zone | Reason |
|------|------|-------------|-------------|--------|------|--------|
| Product_A | 4 | 150 | 200 | +50 | Slushy | New order |
| Product_B | 6 | 100 | 0 | -100 | Liquid | Forecast reduced |

**ATP Summary:**

| Item | Week 1 | Week 2 | Week 3 | Week 4 | Total ATP |
|------|--------|--------|--------|--------|-----------|
| Product_A | 50 | 0 | 20 | 140 | 210 |
| Product_B | 30 | 0 | 0 | 100 | 130 |

**Exception Reports:**

- **Overdue Orders**: List of orders past due date
- **Capacity Overloads**: Resources exceeding 100%
- **Material Shortages**: Components not available
- **Schedule Changes**: Changes in frozen zone

---

## Questions to Ask

If you need more context:
1. What manufacturing environment? (MTS, MTO, ATO, ETO)
2. What's the production process? (discrete, process, batch)
3. Planning horizon and bucket size? (weeks, months)
4. Number of end items to schedule?
5. Current MPS process and tools?
6. Critical capacity constraints?
7. Time fence policies?
8. Schedule adherence rates?

---

## Related Skills

- **sales-operations-planning**: For aggregate production plan input
- **capacity-planning**: For capacity analysis and RCCP
- **demand-forecasting**: For demand input to MPS
- **production-scheduling**: For detailed shop floor scheduling
- **inventory-optimization**: For safety stock and lot sizing
- **lot-sizing-problems**: For MPS quantity decisions
- **supply-chain-analytics**: For MPS performance tracking
- **lean-manufacturing**: For setup reduction and level loading
