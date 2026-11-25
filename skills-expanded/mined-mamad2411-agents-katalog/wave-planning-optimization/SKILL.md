---
name: wave-planning-optimization
description: When the user wants to optimize pick wave planning, schedule warehouse operations, or improve order fulfillment efficiency. Also use when the user mentions "wave management," "batch picking," "pick wave scheduling," "order release optimization," "wave design," or "pick wave strategy." For order batching, see order-batching-optimization. For workforce scheduling, see workforce-scheduling.
---

# Wave Planning Optimization

You are an expert in warehouse wave planning and order release optimization. Your goal is to help design and optimize pick waves to maximize picker productivity, balance workload, meet cutoff times, and improve overall fulfillment efficiency.

## Initial Assessment

Before optimizing wave planning, understand:

1. **Operational Characteristics**
   - Daily order volume (lines and units)?
   - Order types (each-pick, case-pick, full-pallet)?
   - Warehouse zones and pick methods?
   - Shift structure and available labor?
   - Current wave frequency and size?

2. **Business Requirements**
   - Shipping cutoff times?
   - Priority order types (same-day, next-day)?
   - Customer SLAs and promises?
   - Carrier pickup schedules?
   - Order profile (single-line vs. multi-line)?

3. **Constraints**
   - Equipment capacity (conveyors, sorters)?
   - Packing station capacity?
   - Shipping dock doors available?
   - Labor availability by shift?
   - WMS capabilities and limitations?

4. **Performance Metrics**
   - Current picks per hour?
   - Order cycle time (order → ship)?
   - Labor utilization?
   - On-time shipping performance?
   - Wave completion rates?

---

## Wave Planning Framework

### Wave Design Principles

**1. Wave Sizing**
- **Small Waves (50-200 orders)**
  - Pros: Flexible, quick completion, easy re-wave
  - Cons: More frequent releases, higher admin overhead
  - Use: High variability, frequent cutoffs

- **Medium Waves (200-500 orders)**
  - Pros: Balanced workload, good equipment utilization
  - Cons: Some idle time between waves
  - Use: Standard operations, moderate volume

- **Large Waves (500-1000+ orders)**
  - Pros: Maximum efficiency, fewer releases
  - Cons: Inflexible, longer cycle time
  - Use: High volume, stable demand

**2. Wave Frequency**
- **Continuous Waves**: Release new wave when previous completes
- **Fixed Schedule**: Every 2-4 hours (e.g., 8am, 12pm, 4pm)
- **Dynamic**: Based on order accumulation threshold
- **Just-in-Time**: Aligned with carrier pickups

**3. Wave Composition**
- **Zone-Based**: All orders for a warehouse zone
- **Order-Type Based**: Priority, standard, bulk separately
- **Customer-Based**: Group by customer or ship-to region
- **Carrier-Based**: Group by shipping carrier
- **Hybrid**: Combination of above

### Wave Optimization Objectives

```
Primary Goals:
1. Maximize picker productivity (picks/hour)
2. Balance workload across zones/pickers
3. Meet shipping cutoff times
4. Minimize labor cost
5. Maximize equipment utilization

Trade-offs:
- Large waves → Higher efficiency BUT Longer cycle time
- Small waves → Faster cycle time BUT Lower efficiency
- Balanced waves → Even workload BUT May miss optimal picking
```

---

## Mathematical Formulation

### Wave Planning Optimization Model

**Decision Variables:**
- x[o,w] = 1 if order o assigned to wave w, 0 otherwise
- y[w] = 1 if wave w is used, 0 otherwise
- t[w] = start time of wave w
- z[w,z] = workload (lines) in wave w for zone z

**Parameters:**
- L[o] = number of pick lines in order o
- Z[o,z] = number of lines in order o for zone z
- D[o] = deadline for order o
- P = picker productivity (lines/hour)
- W_min, W_max = min/max lines per wave
- N_pickers[z] = number of pickers in zone z

**Objective Function:**

```
Minimize:
  α × (Number of waves)              # Minimize wave releases
  + β × (Total completion time)      # Minimize cycle time
  + γ × (Workload imbalance)         # Balance zones
  + δ × (Late orders penalty)        # Meet deadlines

Formally:
  α × Σ y[w]
  + β × Σ (t[w] + duration[w])
  + γ × Σ (max_workload[w] - min_workload[w])
  + δ × Σ max(0, completion[o] - D[o])
```

**Constraints:**

```python
# 1. Each order in exactly one wave
for o in orders:
    Σ x[o,w] = 1  for all w

# 2. Wave size limits
for w in waves:
    W_min × y[w] ≤ Σ (L[o] × x[o,w]) ≤ W_max × y[w]  for all o

# 3. Meet deadlines
for o in orders:
    for w in waves:
        if x[o,w] = 1:
            t[w] + processing_time[w] ≤ D[o]

# 4. Zone workload calculation
for w in waves:
    for z in zones:
        z[w,z] = Σ (Z[o,z] × x[o,w])  for all o

# 5. Workload feasibility (can complete in shift)
for w in waves:
    for z in zones:
        z[w,z] / (N_pickers[z] × P) ≤ shift_duration

# 6. Wave sequencing
for w in 1..W-1:
    t[w] + duration[w] ≤ t[w+1]
```

---

## Wave Planning Algorithms

### Greedy Wave Building

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def greedy_wave_planning(orders, max_wave_size=500, max_waves=10):
    """
    Build waves using greedy heuristic

    Sort orders by priority/deadline, then fill waves

    Parameters:
    -----------
    orders : DataFrame
        Columns: order_id, lines, deadline, priority, zone
    max_wave_size : int
        Maximum lines per wave
    max_waves : int
        Maximum number of waves

    Returns:
    --------
    Wave assignments
    """

    # Sort orders: priority first, then deadline
    orders_sorted = orders.sort_values(
        ['priority', 'deadline', 'lines'],
        ascending=[False, True, False]
    )

    waves = []
    current_wave = {
        'wave_id': 1,
        'orders': [],
        'total_lines': 0,
        'zones': {}
    }

    for idx, order in orders_sorted.iterrows():
        order_lines = order['lines']
        order_zone = order.get('zone', 'default')

        # Check if adding order exceeds wave size
        if current_wave['total_lines'] + order_lines <= max_wave_size:
            # Add to current wave
            current_wave['orders'].append(order['order_id'])
            current_wave['total_lines'] += order_lines

            # Track zone distribution
            if order_zone not in current_wave['zones']:
                current_wave['zones'][order_zone] = 0
            current_wave['zones'][order_zone] += order_lines

        else:
            # Start new wave
            waves.append(current_wave)

            if len(waves) >= max_waves:
                break

            current_wave = {
                'wave_id': len(waves) + 1,
                'orders': [order['order_id']],
                'total_lines': order_lines,
                'zones': {order_zone: order_lines}
            }

    # Add final wave
    if current_wave['orders'] and len(waves) < max_waves:
        waves.append(current_wave)

    return pd.DataFrame(waves)


# Example usage
orders = pd.DataFrame({
    'order_id': [f'ORD{i:04d}' for i in range(1, 101)],
    'lines': np.random.randint(1, 50, 100),
    'deadline': pd.date_range('2024-01-01 16:00', periods=100, freq='H'),
    'priority': np.random.choice([1, 2, 3], 100),
    'zone': np.random.choice(['A', 'B', 'C'], 100)
})

waves = greedy_wave_planning(orders, max_wave_size=400, max_waves=8)

print("Wave Planning Results:")
print(f"Total Waves: {len(waves)}")
print("\nWave Summary:")
for _, wave in waves.iterrows():
    print(f"Wave {wave['wave_id']}: {len(wave['orders'])} orders, "
          f"{wave['total_lines']} lines, Zones: {wave['zones']}")
```

### Balanced Wave Planning

```python
def balanced_wave_planning(orders, num_waves, zones):
    """
    Create balanced waves across zones to even workload

    Parameters:
    -----------
    orders : DataFrame
        Order data with zone distribution
    num_waves : int
        Number of waves to create
    zones : list
        Zone identifiers

    Returns:
    --------
    Balanced wave assignments
    """

    # Calculate zone distribution for each order
    order_zone_lines = {}
    for idx, order in orders.iterrows():
        order_id = order['order_id']
        # Assume we have zone breakdown (simplified: random here)
        zone_dist = {z: np.random.randint(0, order['lines'] // len(zones) + 1)
                    for z in zones}
        order_zone_lines[order_id] = zone_dist

    # Initialize waves
    waves = [{
        'wave_id': w + 1,
        'orders': [],
        'zone_lines': {z: 0 for z in zones},
        'total_lines': 0
    } for w in range(num_waves)]

    # Sort orders by total lines (largest first for better packing)
    orders_sorted = orders.sort_values('lines', ascending=False)

    # Assign each order to wave with minimum workload imbalance
    for idx, order in orders_sorted.iterrows():
        order_id = order['order_id']
        zone_dist = order_zone_lines[order_id]

        # Find wave that minimizes maximum zone workload
        best_wave_idx = None
        best_balance_score = float('inf')

        for w_idx, wave in enumerate(waves):
            # Calculate new zone workloads if order added
            new_zone_loads = {}
            for z in zones:
                new_zone_loads[z] = wave['zone_lines'][z] + zone_dist[z]

            # Balance score: range of zone workloads
            max_load = max(new_zone_loads.values())
            min_load = min(new_zone_loads.values())
            balance_score = max_load - min_load

            if balance_score < best_balance_score:
                best_balance_score = balance_score
                best_wave_idx = w_idx

        # Assign order to best wave
        waves[best_wave_idx]['orders'].append(order_id)
        waves[best_wave_idx]['total_lines'] += order['lines']
        for z in zones:
            waves[best_wave_idx]['zone_lines'][z] += zone_dist[order_id][z]

    return pd.DataFrame(waves)


# Example
zones = ['Zone_A', 'Zone_B', 'Zone_C']
balanced_waves = balanced_wave_planning(orders, num_waves=5, zones=zones)

print("\nBalanced Wave Planning:")
for _, wave in balanced_waves.iterrows():
    print(f"Wave {wave['wave_id']}: {len(wave['orders'])} orders")
    print(f"  Zone distribution: {wave['zone_lines']}")
    max_zone = max(wave['zone_lines'].values())
    min_zone = min(wave['zone_lines'].values())
    print(f"  Balance: {max_zone - min_zone} lines difference\n")
```

### MIP-Based Wave Optimization

```python
from pulp import *

def optimize_wave_planning(orders_df, num_waves, zone_productivity,
                           shift_hours=8, min_wave_size=100):
    """
    Optimize wave planning using Mixed-Integer Programming

    Parameters:
    -----------
    orders_df : DataFrame
        Order data: order_id, lines, deadline, zone_breakdown
    num_waves : int
        Number of waves to plan
    zone_productivity : dict
        {zone: lines_per_hour_per_picker}
    shift_hours : float
        Hours available per shift
    min_wave_size : int
        Minimum lines per wave

    Returns:
    --------
    Optimal wave assignments
    """

    orders = orders_df['order_id'].tolist()
    waves = list(range(num_waves))
    zones = list(zone_productivity.keys())

    # Create problem
    prob = LpProblem("Wave_Planning", LpMinimize)

    # Decision variables
    # x[o,w] = 1 if order o in wave w
    x = LpVariable.dicts("assign",
                        [(o, w) for o in orders for w in waves],
                        cat='Binary')

    # y[w] = 1 if wave w is used
    y = LpVariable.dicts("use_wave",
                        waves,
                        cat='Binary')

    # Workload variables
    workload = LpVariable.dicts("workload",
                               [(w, z) for w in waves for z in zones],
                               lowBound=0,
                               cat='Continuous')

    # Max workload per wave (for balancing)
    max_workload = LpVariable.dicts("max_load",
                                   waves,
                                   lowBound=0,
                                   cat='Continuous')

    # Objective: Minimize number of waves + balance workload
    prob += (
        100 * lpSum([y[w] for w in waves]) +  # Minimize waves
        lpSum([max_workload[w] for w in waves])  # Balance workload
    ), "Objective"

    # Constraints

    # 1. Each order in exactly one wave
    for o in orders:
        prob += lpSum([x[o, w] for w in waves]) == 1, f"Order_{o}"

    # 2. Calculate workload per wave per zone
    for w in waves:
        for z in zones:
            # Simplified: assume equal zone distribution
            # In practice, would have actual zone breakdown per order
            prob += workload[w, z] == lpSum([
                orders_df.loc[orders_df['order_id'] == o, 'lines'].values[0] / len(zones) * x[o, w]
                for o in orders
            ]), f"Workload_{w}_{z}"

    # 3. Track maximum workload per wave
    for w in waves:
        for z in zones:
            prob += max_workload[w] >= workload[w, z], f"MaxLoad_{w}_{z}"

    # 4. Wave size constraints
    for w in waves:
        total_lines = lpSum([
            orders_df.loc[orders_df['order_id'] == o, 'lines'].values[0] * x[o, w]
            for o in orders
        ])

        # Minimum wave size
        prob += total_lines >= min_wave_size * y[w], f"MinSize_{w}"

        # Maximum wave size (implicit from shift capacity)
        # Total lines must be completable in shift
        prob += total_lines <= shift_hours * sum(zone_productivity.values()) * y[w], \
                f"MaxSize_{w}"

    # 5. Link order assignment to wave usage
    for w in waves:
        for o in orders:
            prob += x[o, w] <= y[w], f"Link_{o}_{w}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    wave_assignments = []
    for w in waves:
        if y[w].varValue > 0.5:
            wave_orders = [o for o in orders if x[o, w].varValue > 0.5]
            total_lines = sum(
                orders_df.loc[orders_df['order_id'] == o, 'lines'].values[0]
                for o in wave_orders
            )

            wave_workloads = {
                z: workload[w, z].varValue for z in zones
            }

            wave_assignments.append({
                'wave_id': w + 1,
                'orders': wave_orders,
                'num_orders': len(wave_orders),
                'total_lines': total_lines,
                'zone_workloads': wave_workloads,
                'max_zone_workload': max_workload[w].varValue
            })

    return {
        'status': LpStatus[prob.status],
        'objective': value(prob.objective),
        'waves': pd.DataFrame(wave_assignments)
    }


# Example
zone_productivity = {'Zone_A': 100, 'Zone_B': 120, 'Zone_C': 110}  # lines/hour

result = optimize_wave_planning(
    orders.head(50),  # Use subset for faster solving
    num_waves=6,
    zone_productivity=zone_productivity,
    shift_hours=8,
    min_wave_size=80
)

print(f"\nOptimization Status: {result['status']}")
print(f"Objective Value: {result['objective']:.2f}")
print("\nOptimal Waves:")
print(result['waves'][['wave_id', 'num_orders', 'total_lines', 'max_zone_workload']])
```

---

## Advanced Wave Planning Techniques

### Dynamic Wave Release Strategy

```python
class DynamicWaveManager:
    """
    Manage dynamic wave releases based on order accumulation
    """

    def __init__(self, target_wave_size=400, min_wave_size=200,
                 release_threshold=0.9):
        self.target_wave_size = target_wave_size
        self.min_wave_size = min_wave_size
        self.release_threshold = release_threshold
        self.pending_orders = []
        self.released_waves = []

    def add_order(self, order):
        """Add new order to pending queue"""
        self.pending_orders.append(order)

    def should_release_wave(self):
        """
        Determine if wave should be released

        Release criteria:
        1. Accumulated lines >= target size
        2. Oldest order waiting > max_wait_time
        3. Cutoff time approaching
        """

        total_lines = sum(o['lines'] for o in self.pending_orders)

        # Criterion 1: Size threshold
        if total_lines >= self.target_wave_size * self.release_threshold:
            return True, "Size threshold reached"

        # Criterion 2: Max wait time (simplified)
        if len(self.pending_orders) > 0:
            oldest_order_time = min(o['received_time'] for o in self.pending_orders)
            wait_minutes = (datetime.now() - oldest_order_time).total_seconds() / 60

            if wait_minutes > 120:  # 2 hours max wait
                return True, "Max wait time exceeded"

        # Criterion 3: Minimum size and approaching cutoff
        if total_lines >= self.min_wave_size:
            # Check if cutoff approaching (simplified)
            return True, "Minimum size reached, release to avoid rush"

        return False, "Not ready"

    def release_wave(self):
        """Release wave from pending orders"""

        if len(self.pending_orders) == 0:
            return None

        # Take up to target_wave_size
        wave_orders = []
        total_lines = 0

        # Sort by priority and deadline
        sorted_orders = sorted(
            self.pending_orders,
            key=lambda x: (x.get('priority', 0), x.get('deadline', datetime.max)),
            reverse=True
        )

        for order in sorted_orders:
            if total_lines + order['lines'] <= self.target_wave_size:
                wave_orders.append(order)
                total_lines += order['lines']

        # Remove released orders from pending
        for order in wave_orders:
            self.pending_orders.remove(order)

        wave = {
            'wave_id': len(self.released_waves) + 1,
            'orders': wave_orders,
            'total_lines': total_lines,
            'release_time': datetime.now()
        }

        self.released_waves.append(wave)

        return wave

    def get_pending_summary(self):
        """Get summary of pending orders"""
        return {
            'num_orders': len(self.pending_orders),
            'total_lines': sum(o['lines'] for o in self.pending_orders),
            'oldest_order': min((o['received_time'] for o in self.pending_orders),
                              default=None)
        }


# Example usage
manager = DynamicWaveManager(target_wave_size=500, min_wave_size=200)

# Simulate order arrivals
for i in range(30):
    order = {
        'order_id': f'ORD{i:04d}',
        'lines': np.random.randint(10, 50),
        'priority': np.random.choice([1, 2, 3]),
        'deadline': datetime.now() + timedelta(hours=4),
        'received_time': datetime.now() - timedelta(minutes=np.random.randint(0, 180))
    }
    manager.add_order(order)

# Check if should release
should_release, reason = manager.should_release_wave()
print(f"Should release wave: {should_release} ({reason})")

if should_release:
    wave = manager.release_wave()
    print(f"\nReleased Wave {wave['wave_id']}:")
    print(f"  Orders: {len(wave['orders'])}")
    print(f"  Lines: {wave['total_lines']}")

pending = manager.get_pending_summary()
print(f"\nPending Orders: {pending['num_orders']} orders, {pending['total_lines']} lines")
```

### Multi-Shift Wave Planning

```python
def plan_multi_shift_waves(orders, shifts, pickers_per_shift,
                           productivity=100):
    """
    Plan waves across multiple shifts

    Parameters:
    -----------
    orders : DataFrame
        All orders to fulfill
    shifts : list of dict
        [{shift_id, start_time, end_time, hours}, ...]
    pickers_per_shift : dict
        {shift_id: num_pickers}
    productivity : float
        Lines per hour per picker

    Returns:
    --------
    Wave plan with shift assignments
    """

    # Calculate capacity per shift
    shift_capacity = {}
    for shift in shifts:
        shift_id = shift['shift_id']
        capacity = (pickers_per_shift[shift_id] *
                   shift['hours'] *
                   productivity)
        shift_capacity[shift_id] = capacity

    # Sort orders by deadline
    orders_sorted = orders.sort_values('deadline')

    shift_assignments = {shift['shift_id']: [] for shift in shifts}
    shift_loads = {shift['shift_id']: 0 for shift in shifts}

    # Assign orders to shifts
    for idx, order in orders_sorted.iterrows():
        order_lines = order['lines']
        deadline = order['deadline']

        # Find earliest shift that can handle this order and meet deadline
        assigned = False
        for shift in shifts:
            shift_id = shift['shift_id']

            # Check if shift can complete before deadline
            if shift['end_time'] <= deadline:
                # Check if capacity available
                if shift_loads[shift_id] + order_lines <= shift_capacity[shift_id]:
                    shift_assignments[shift_id].append(order['order_id'])
                    shift_loads[shift_id] += order_lines
                    assigned = True
                    break

        if not assigned:
            print(f"Warning: Could not assign order {order['order_id']}")

    # Create waves within each shift
    all_waves = []
    wave_counter = 1

    for shift in shifts:
        shift_id = shift['shift_id']
        shift_orders = shift_assignments[shift_id]

        if not shift_orders:
            continue

        # Split shift into waves (e.g., 2 waves per 8-hour shift)
        num_waves_per_shift = max(1, int(shift['hours'] / 4))
        orders_per_wave = len(shift_orders) // num_waves_per_shift

        for w in range(num_waves_per_shift):
            start_idx = w * orders_per_wave
            end_idx = start_idx + orders_per_wave if w < num_waves_per_shift - 1 else len(shift_orders)

            wave_orders = shift_orders[start_idx:end_idx]
            wave_lines = sum(
                orders.loc[orders['order_id'] == o, 'lines'].values[0]
                for o in wave_orders
            )

            all_waves.append({
                'wave_id': wave_counter,
                'shift_id': shift_id,
                'wave_in_shift': w + 1,
                'orders': wave_orders,
                'num_orders': len(wave_orders),
                'total_lines': wave_lines
            })
            wave_counter += 1

    return pd.DataFrame(all_waves)


# Example
shifts = [
    {'shift_id': 'Day', 'start_time': datetime(2024,1,1,6,0),
     'end_time': datetime(2024,1,1,14,0), 'hours': 8},
    {'shift_id': 'Evening', 'start_time': datetime(2024,1,1,14,0),
     'end_time': datetime(2024,1,1,22,0), 'hours': 8},
    {'shift_id': 'Night', 'start_time': datetime(2024,1,1,22,0),
     'end_time': datetime(2024,1,2,6,0), 'hours': 8}
]

pickers = {'Day': 12, 'Evening': 8, 'Night': 4}

multi_shift_waves = plan_multi_shift_waves(orders.head(100), shifts, pickers)

print("\nMulti-Shift Wave Plan:")
print(multi_shift_waves.groupby('shift_id')[['num_orders', 'total_lines']].sum())
```

---

## Tools & Libraries

### Wave Management Software

**Warehouse Management Systems:**
- **Manhattan WMS**: Advanced wave planning and optimization
- **Blue Yonder (JDA) WMS**: AI-driven wave management
- **SAP EWM**: Wave templates and dynamic release
- **HighJump WMS**: Configurable wave strategies
- **Körber WMS**: Multi-wave parallel processing

**Order Management Systems:**
- **IBM Sterling OMS**: Wave release and order orchestration
- **Fluent Commerce**: Real-time order promising and waving
- **Radial OMS**: Distributed order management with waving

### Python Libraries

```python
# Optimization
from pulp import *
from ortools.sat.python import cp_model

# Scheduling
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Analysis
from sklearn.cluster import KMeans  # Order clustering
import matplotlib.pyplot as plt
```

---

## Common Challenges & Solutions

### Challenge: Cutoff Time Pressure

**Problem:**
- Orders arrive late, need same-day ship
- Wave released too early misses late orders
- Wave released too late misses carrier pickup

**Solutions:**
- Multiple cutoff waves (e.g., 12pm, 2pm, 4pm)
- Express wave for urgent orders (small, frequent)
- Dynamic wave release triggered at 80% threshold
- Pre-stage high-probability orders
- Negotiate later carrier pickups
- Use last-mile carriers with flexible schedules

### Challenge: Workload Imbalance

**Problem:**
- Some zones finish early, others late
- Pickers idle while others overwhelmed
- Bottlenecks at packing stations

**Solutions:**
- Balance waves across zones mathematically
- Cross-train pickers to work multiple zones
- Dynamic picker redeployment mid-wave
- Adjust wave size by zone capacity
- Use pick-to-light or goods-to-person (balanced automatically)
- Monitor real-time progress, rebalance next wave

### Challenge: Order Profile Variability

**Problem:**
- Mix of single-line and 50-line orders
- Some days 500 orders, some days 2000
- Seasonal peaks disrupt standard waves

**Solutions:**
- Separate waves by order complexity (each vs. case)
- Variable wave size (200-600 lines, not fixed)
- Reserve capacity for large orders
- Pre-pick high-velocity items during off-peak
- Hire temp labor for peaks
- Adjust wave frequency dynamically (not fixed schedule)

### Challenge: Equipment Constraints

**Problem:**
- Conveyor at capacity (max 500 units/hour)
- Sorter can't handle wave volume
- Packing stations become bottleneck

**Solutions:**
- Wave size limited by downstream capacity
- Stagger wave releases (15-min offset between zones)
- Use wave pools (release to picking, but meter to packing)
- Add surge capacity (temporary packing stations)
- Batch packing for same customer/carrier
- Upgrade equipment or add parallel lines

### Challenge: WMS Limitations

**Problem:**
- WMS only supports fixed wave sizes
- Can't auto-release based on thresholds
- Limited wave templates
- No cross-zone wave support

**Solutions:**
- Use middleware for advanced wave logic
- Manual monitoring with alert thresholds
- Pre-build wave templates for common scenarios
- Upgrade WMS or add bolt-on optimization
- Work with WMS vendor on custom logic
- Implement external optimization, feed results to WMS

---

## Output Format

### Wave Planning Report

**Daily Wave Schedule - January 15, 2024**

| Wave | Start Time | Lines | Orders | Zones | Est. Duration | Cutoff Met | Status |
|------|------------|-------|--------|-------|---------------|----------|--------|
| W01 | 06:00 | 420 | 87 | A,B,C | 3.2 hrs | 12pm | Complete |
| W02 | 09:00 | 385 | 96 | A,B,C | 2.9 hrs | 12pm | In Progress |
| W03 | 12:00 | 510 | 102 | A,B,C | 3.8 hrs | 4pm | Scheduled |
| W04 | 16:00 | 295 | 74 | A,B,C | 2.2 hrs | 6pm | Scheduled |

**Wave W02 Details:**

```
Orders: 96
Total Lines: 385
Average Lines/Order: 4.0

Zone Distribution:
  Zone A: 145 lines (38%)
  Zone B: 132 lines (34%)
  Zone C: 108 lines (28%)

Pickers Assigned:
  Zone A: 4 pickers → ~36 lines/picker
  Zone B: 3 pickers → ~44 lines/picker
  Zone C: 3 pickers → ~36 lines/picker

Expected Completion: 11:54 AM
Cutoff: 12:00 PM (6 min buffer)

Priority Orders: 12 (flagged for early pick)
```

**Performance Summary:**

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Waves per Day | 8-10 | 9 | ✓ On Target |
| Avg Wave Size | 350-450 | 403 | ✓ On Target |
| Balance (max-min zone) | <50 lines | 37 lines | ✓ On Target |
| Cutoff Adherence | >95% | 98% | ✓ On Target |
| Picker Utilization | 80-90% | 86% | ✓ On Target |

**Recommendations:**
- Wave 3 is largest - consider split if issues arise
- Zone B slightly higher workload in W02 - add 1 picker if available
- Suggest moving cutoff to 12:30pm for 30min buffer

---

## Questions to Ask

If you need more context:
1. What's your daily order volume (orders and lines)?
2. How many pick waves do you currently run per day?
3. What are your shipping cutoff times?
4. How many warehouse zones and pickers per zone?
5. What WMS do you use? Wave planning capabilities?
6. What's your average picks per hour per picker?
7. Any equipment bottlenecks (conveyor, sorter, packing)?
8. Do you have priority or express orders?

---

## Related Skills

- **order-batching-optimization**: For grouping orders within waves
- **picker-routing-optimization**: For optimizing pick paths within waves
- **workforce-scheduling**: For shift and labor planning
- **task-assignment-problem**: For assigning pickers to zones/waves
- **warehouse-slotting-optimization**: For SKU placement affecting pick efficiency
- **order-fulfillment**: For overall fulfillment process design
- **capacity-planning**: For long-term wave capacity planning
