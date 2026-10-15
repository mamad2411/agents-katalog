---
name: load-building-optimization
description: When the user wants to optimize load building, create efficient truck loads, or maximize trailer utilization. Also use when the user mentions "load planning," "truck loading," "cargo optimization," "shipment consolidation," "cube utilization," or "weight distribution." For pallet loading, see pallet-loading. For container loading, see container-loading-optimization.
---

# Load Building Optimization

You are an expert in load building and truck loading optimization for transportation and logistics. Your goal is to help create optimal truck loads that maximize utilization, minimize costs, ensure stability and safety, and improve overall shipping efficiency.

## Initial Assessment

Before optimizing load building, understand:

1. **Fleet Characteristics**
   - Trailer types (dry van, reefer, flatbed)?
   - Trailer dimensions (length × width × height)?
   - Weight capacity (gross weight limit)?
   - Axle weight restrictions?
   - Floor load ratings (psi)?
   - Number of available trucks?

2. **Shipment Profile**
   - Daily shipment volume (pallets, cases)?
   - Package dimensions and weights?
   - Stackability and fragility?
   - Temperature requirements (ambient, chilled, frozen)?
   - Delivery sequence and routes?
   - Compatible/incompatible products?

3. **Business Requirements**
   - Minimize number of trucks?
   - Maximize cube utilization?
   - Meet delivery windows?
   - Reduce freight cost?
   - Ensure product safety (no damage)?
   - Route efficiency (stop sequence)?

4. **Current State**
   - Current cube utilization %?
   - Average weight utilization %?
   - Load planning method (manual, software)?
   - Freight costs and trends?
   - Damage rates?

---

## Load Building Framework

### Load Planning Objectives

**Primary Goals:**
1. **Maximize Space Utilization**: Fill trailer volume efficiently
2. **Maximize Weight Utilization**: Use full weight capacity
3. **Minimize Number of Trucks**: Consolidate to reduce cost
4. **Balance Load**: Proper weight distribution, prevent shifting
5. **Ensure Safety**: No overweight axles, stable stacking
6. **Optimize Routes**: Load sequence matches delivery order

**Key Metrics:**
- Cube utilization % (actual volume / trailer capacity)
- Weight utilization % (actual weight / capacity)
- Cost per pound or per cubic foot
- Number of trucks required
- Load time (time to build and verify load)
- Damage rate (claims per 1000 shipments)

### Load Building Strategies

**1. Floor-to-Ceiling Loading**
- Fill trailer height fully
- Minimize wasted vertical space
- **Pros**: Maximum cube utilization
- **Cons**: Risk of damage to bottom layers
- **Use**: Sturdy products, uniform pallets

**2. Layer-by-Layer Loading**
- Build in horizontal layers
- Each layer completes before next
- **Pros**: Stable, easy to verify
- **Cons**: May waste vertical space
- **Use**: Fragile items, mixed pallets

**3. Zone Loading (Stop-Sequence)**
- Group shipments by delivery stop
- Load last-off-first (LIFO)
- **Pros**: Minimizes handling at delivery
- **Cons**: May reduce cube utilization
- **Use**: Multi-stop routes, LTL

**4. Weight-Forward Loading**
- Heavy items toward front (over drive axles)
- Light items toward back
- **Pros**: Better weight distribution, handling
- **Cons**: May not maximize cube
- **Use**: Heavy/bulky loads, long haul

**5. Tetris/3D Bin Packing**
- Optimize placement like Tetris game
- Use algorithms to maximize density
- **Pros**: Best cube utilization
- **Cons**: Complex, may be impractical to execute
- **Use**: Irregular shapes, high-value freight

---

## Mathematical Formulation

### 3D Bin Packing Problem

**Decision Variables:**
- x[i,j] = 1 if item i placed in truck j, 0 otherwise
- pos[i] = (x, y, z) position of item i in truck
- orient[i] = orientation of item i (rotation)

**Parameters:**
- L[i], W[i], H[i] = length, width, height of item i
- weight[i] = weight of item i
- TL, TW, TH = truck length, width, height
- T_weight = truck weight capacity
- n = number of items
- m = number of available trucks

**Objective:**

```
Minimize: Number of trucks used

Subject to:
  All items assigned
  No overlapping items
  Weight limits respected
  Stability constraints satisfied
```

**Constraints:**

```python
# 1. Each item assigned to exactly one truck
for i in items:
    Σ x[i,j] = 1  for all j in trucks

# 2. Items within truck boundaries
for i in items:
    for j in trucks:
        if x[i,j] = 1:
            pos[i].x + L[i] <= TL
            pos[i].y + W[i] <= TW
            pos[i].z + H[i] <= TH

# 3. No overlapping (simplified)
for i, k in items (i != k):
    for j in trucks:
        if x[i,j] = 1 and x[k,j] = 1:
            # One of these must be true:
            pos[i].x + L[i] <= pos[k].x  OR
            pos[k].x + L[k] <= pos[i].x  OR
            pos[i].y + W[i] <= pos[k].y  OR
            pos[k].y + W[k] <= pos[i].y  OR
            pos[i].z + H[i] <= pos[k].z  OR
            pos[k].z + H[k] <= pos[i].z

# 4. Weight capacity
for j in trucks:
    Σ (weight[i] × x[i,j]) <= T_weight  for all i

# 5. Support constraint (item must rest on floor or another item)
for i in items:
    if pos[i].z > 0:
        must have sufficient support area underneath

# 6. Stackability
for i, k in items:
    if item i on top of item k:
        stackable[k] must be True
        weight_on_top[k] <= max_stack_weight[k]
```

This is an NP-hard problem, so practical solutions use heuristics.

---

## Load Building Algorithms

### First-Fit Decreasing (FFD) Heuristic

```python
import numpy as np
import pandas as pd

def first_fit_decreasing_load_building(shipments, truck_capacity):
    """
    First-Fit Decreasing heuristic for load building

    Algorithm:
    1. Sort shipments by volume (largest first)
    2. For each shipment, try to fit in first truck with space
    3. If doesn't fit, create new truck

    Parameters:
    -----------
    shipments : DataFrame
        Columns: shipment_id, weight, volume, length, width, height
    truck_capacity : dict
        {'weight': max_weight, 'volume': max_volume}

    Returns:
    --------
    Load plan with truck assignments
    """

    # Sort by volume (largest first)
    shipments_sorted = shipments.sort_values('volume', ascending=False).copy()

    trucks = []
    current_truck = {
        'truck_id': 1,
        'shipments': [],
        'total_weight': 0,
        'total_volume': 0
    }

    for idx, shipment in shipments_sorted.iterrows():
        ship_weight = shipment['weight']
        ship_volume = shipment['volume']

        # Try to fit in current truck
        if (current_truck['total_weight'] + ship_weight <= truck_capacity['weight'] and
            current_truck['total_volume'] + ship_volume <= truck_capacity['volume']):

            # Fits in current truck
            current_truck['shipments'].append(shipment['shipment_id'])
            current_truck['total_weight'] += ship_weight
            current_truck['total_volume'] += ship_volume

        else:
            # Doesn't fit, start new truck
            trucks.append(current_truck)

            current_truck = {
                'truck_id': len(trucks) + 1,
                'shipments': [shipment['shipment_id']],
                'total_weight': ship_weight,
                'total_volume': ship_volume
            }

    # Add last truck
    if current_truck['shipments']:
        trucks.append(current_truck)

    # Calculate utilization
    for truck in trucks:
        truck['weight_util'] = (truck['total_weight'] / truck_capacity['weight']) * 100
        truck['volume_util'] = (truck['total_volume'] / truck_capacity['volume']) * 100

    return pd.DataFrame(trucks)


# Example usage
shipments = pd.DataFrame({
    'shipment_id': [f'S{i:03d}' for i in range(1, 51)],
    'weight': np.random.uniform(500, 5000, 50),  # lbs
    'volume': np.random.uniform(50, 500, 50),    # cubic feet
    'length': np.random.uniform(3, 8, 50),       # feet
    'width': np.random.uniform(3, 4, 50),
    'height': np.random.uniform(3, 6, 50)
})

truck_capacity = {
    'weight': 45000,  # lbs (typical 53' dry van)
    'volume': 4000    # cubic feet
}

load_plan = first_fit_decreasing_load_building(shipments, truck_capacity)

print("Load Building Results (First-Fit Decreasing):")
print(f"Total Trucks: {len(load_plan)}")
print(f"\nTruck Summary:")
print(load_plan[['truck_id', 'total_weight', 'total_volume',
                 'weight_util', 'volume_util']])

print(f"\nAverage Utilization:")
print(f"  Weight: {load_plan['weight_util'].mean():.1f}%")
print(f"  Volume: {load_plan['volume_util'].mean():.1f}%")
```

### Best-Fit Decreasing with Route Sequence

```python
def best_fit_with_route_sequence(shipments, truck_capacity, route_sequence):
    """
    Best-fit load building considering delivery sequence

    Ensure items delivered first are loaded last (LIFO)

    Parameters:
    -----------
    shipments : DataFrame
        With route_stop column indicating delivery order
    truck_capacity : dict
    route_sequence : list
        Ordered list of stops

    Returns:
    --------
    Load plan with sequence constraints
    """

    # Group shipments by route stop
    shipments_by_stop = shipments.groupby('route_stop')

    trucks = []

    # Reverse route sequence (load last stop first)
    for stop in reversed(route_sequence):
        if stop not in shipments_by_stop.groups:
            continue

        stop_shipments = shipments_by_stop.get_group(stop)
        stop_shipments_sorted = stop_shipments.sort_values('volume', ascending=False)

        # Try to fit stop's shipments into existing trucks
        for idx, shipment in stop_shipments_sorted.iterrows():
            ship_weight = shipment['weight']
            ship_volume = shipment['volume']

            placed = False

            # Try existing trucks (prefer truck with most remaining space)
            for truck in sorted(trucks,
                              key=lambda t: (truck_capacity['volume'] - t['total_volume']),
                              reverse=True):

                if (truck['total_weight'] + ship_weight <= truck_capacity['weight'] and
                    truck['total_volume'] + ship_volume <= truck_capacity['volume']):

                    # Fits in this truck
                    truck['shipments'].append(shipment['shipment_id'])
                    truck['stops'].add(stop)
                    truck['total_weight'] += ship_weight
                    truck['total_volume'] += ship_volume
                    placed = True
                    break

            if not placed:
                # Create new truck
                trucks.append({
                    'truck_id': len(trucks) + 1,
                    'shipments': [shipment['shipment_id']],
                    'stops': {stop},
                    'total_weight': ship_weight,
                    'total_volume': ship_volume
                })

    # Calculate utilization
    for truck in trucks:
        truck['weight_util'] = (truck['total_weight'] / truck_capacity['weight']) * 100
        truck['volume_util'] = (truck['total_volume'] / truck_capacity['volume']) * 100
        truck['num_stops'] = len(truck['stops'])
        truck['stops'] = list(truck['stops'])

    return pd.DataFrame(trucks)


# Example with route stops
shipments_routed = shipments.copy()
shipments_routed['route_stop'] = np.random.choice(['Stop_A', 'Stop_B', 'Stop_C', 'Stop_D'], 50)

route_sequence = ['Stop_A', 'Stop_B', 'Stop_C', 'Stop_D']

load_plan_routed = best_fit_with_route_sequence(
    shipments_routed, truck_capacity, route_sequence
)

print("\nLoad Building with Route Sequence:")
print(load_plan_routed[['truck_id', 'num_stops', 'total_weight', 'weight_util']])
```

### 3D Bin Packing Heuristic

```python
class Container3D:
    """Represent a truck/container for 3D packing"""

    def __init__(self, length, width, height, weight_limit):
        self.length = length
        self.width = width
        self.height = height
        self.weight_limit = weight_limit
        self.items = []
        self.total_weight = 0
        self.spaces = [(0, 0, 0, length, width, height)]  # Available spaces

    def can_fit(self, item_length, item_width, item_height, item_weight):
        """Check if item can fit in any available space"""

        if self.total_weight + item_weight > self.weight_limit:
            return False

        for space in self.spaces:
            sx, sy, sz, sl, sw, sh = space

            # Try all 6 orientations
            orientations = [
                (item_length, item_width, item_height),
                (item_length, item_height, item_width),
                (item_width, item_length, item_height),
                (item_width, item_height, item_length),
                (item_height, item_length, item_width),
                (item_height, item_width, item_length)
            ]

            for l, w, h in orientations:
                if l <= sl and w <= sw and h <= sh:
                    return True, space, (l, w, h)

        return False, None, None

    def place_item(self, item_id, item_length, item_width, item_height, item_weight):
        """Place item in best available space"""

        can_fit_result = self.can_fit(item_length, item_width, item_height, item_weight)

        if can_fit_result[0]:
            space, orientation = can_fit_result[1], can_fit_result[2]
            sx, sy, sz, sl, sw, sh = space
            l, w, h = orientation

            # Place item at corner of space
            self.items.append({
                'item_id': item_id,
                'position': (sx, sy, sz),
                'dimensions': (l, w, h),
                'weight': item_weight
            })

            self.total_weight += item_weight

            # Remove used space and create new available spaces
            self.spaces.remove(space)

            # Create new spaces (simplified - guillotine cuts)
            # Right space
            if sl - l > 0:
                self.spaces.append((sx + l, sy, sz, sl - l, sw, sh))

            # Front space
            if sw - w > 0:
                self.spaces.append((sx, sy + w, sz, l, sw - w, sh))

            # Top space
            if sh - h > 0:
                self.spaces.append((sx, sy, sz + h, l, w, sh - h))

            # Sort spaces by position (bottom-left-front first)
            self.spaces.sort(key=lambda s: (s[2], s[1], s[0]))

            return True

        return False


def pack_3d_containers(items, container_dims, container_weight_limit):
    """
    Pack items into containers using 3D bin packing

    Parameters:
    -----------
    items : DataFrame
        Columns: item_id, length, width, height, weight
    container_dims : tuple
        (length, width, height) of container
    container_weight_limit : float

    Returns:
    --------
    List of packed containers
    """

    # Sort items by volume (largest first)
    items_sorted = items.copy()
    items_sorted['volume'] = (items_sorted['length'] *
                             items_sorted['width'] *
                             items_sorted['height'])
    items_sorted = items_sorted.sort_values('volume', ascending=False)

    containers = []
    current_container = Container3D(*container_dims, container_weight_limit)

    for idx, item in items_sorted.iterrows():
        placed = current_container.place_item(
            item['item_id'],
            item['length'],
            item['width'],
            item['height'],
            item['weight']
        )

        if not placed:
            # Start new container
            containers.append(current_container)
            current_container = Container3D(*container_dims, container_weight_limit)

            # Try again with new container
            placed = current_container.place_item(
                item['item_id'],
                item['length'],
                item['width'],
                item['height'],
                item['weight']
            )

            if not placed:
                print(f"Warning: Could not place item {item['item_id']}")

    # Add last container
    if current_container.items:
        containers.append(current_container)

    return containers


# Example
container_dims = (53, 8.5, 9)  # 53' trailer: length, width, height (feet)
container_weight_limit = 45000  # lbs

# Convert shipments to feet for dimensions
items_3d = shipments.copy()

containers = pack_3d_containers(items_3d, container_dims, container_weight_limit)

print(f"\n3D Bin Packing Results:")
print(f"Total Containers: {len(containers)}")

for i, container in enumerate(containers):
    volume_used = sum(
        item['dimensions'][0] * item['dimensions'][1] * item['dimensions'][2]
        for item in container.items
    )
    total_volume = container.length * container.width * container.height

    print(f"\nContainer {i+1}:")
    print(f"  Items: {len(container.items)}")
    print(f"  Weight: {container.total_weight:,.0f} lbs "
          f"({container.total_weight / container_weight_limit * 100:.1f}%)")
    print(f"  Volume: {volume_used / total_volume * 100:.1f}% utilized")
```

---

## Advanced Load Building Techniques

### Weight Distribution and Axle Loads

```python
def calculate_axle_weights(items_in_truck, truck_length=53):
    """
    Calculate weight on each axle to ensure compliance

    Truck has:
    - Steer axle (front)
    - Drive axles (middle)
    - Trailer axles (rear)

    Parameters:
    -----------
    items_in_truck : list
        Items with position and weight
    truck_length : float
        Truck length in feet

    Returns:
    --------
    Axle weights and compliance
    """

    # Axle positions (simplified)
    steer_position = 0
    drive_position = 20  # feet from front
    trailer_position = 43  # feet from front

    steer_weight = 0
    drive_weight = 0
    trailer_weight = 0

    # Calculate center of gravity for each item
    for item in items_in_truck:
        position_x = item['position'][0]  # Distance from front
        item_cog_x = position_x + item['dimensions'][0] / 2
        item_weight = item['weight']

        # Distribute weight to axles based on distance
        # Simplified: closest axle gets weight

        dist_to_steer = abs(item_cog_x - steer_position)
        dist_to_drive = abs(item_cog_x - drive_position)
        dist_to_trailer = abs(item_cog_x - trailer_position)

        min_dist = min(dist_to_steer, dist_to_drive, dist_to_trailer)

        if min_dist == dist_to_steer:
            steer_weight += item_weight
        elif min_dist == dist_to_drive:
            drive_weight += item_weight
        else:
            trailer_weight += item_weight

    # Legal limits (example - varies by jurisdiction)
    limits = {
        'steer': 12000,   # lbs
        'drive': 34000,   # lbs (tandem)
        'trailer': 34000  # lbs (tandem)
    }

    compliant = (
        steer_weight <= limits['steer'] and
        drive_weight <= limits['drive'] and
        trailer_weight <= limits['trailer']
    )

    return {
        'steer_weight': steer_weight,
        'drive_weight': drive_weight,
        'trailer_weight': trailer_weight,
        'total_weight': steer_weight + drive_weight + trailer_weight,
        'compliant': compliant,
        'violations': {
            'steer': max(0, steer_weight - limits['steer']),
            'drive': max(0, drive_weight - limits['drive']),
            'trailer': max(0, trailer_weight - limits['trailer'])
        }
    }


# Example
if len(containers) > 0:
    axle_weights = calculate_axle_weights(containers[0].items)

    print("\nAxle Weight Distribution:")
    print(f"  Steer Axle: {axle_weights['steer_weight']:,.0f} lbs")
    print(f"  Drive Axle: {axle_weights['drive_weight']:,.0f} lbs")
    print(f"  Trailer Axle: {axle_weights['trailer_weight']:,.0f} lbs")
    print(f"  Total: {axle_weights['total_weight']:,.0f} lbs")
    print(f"  Compliant: {'Yes' if axle_weights['compliant'] else 'No'}")
```

### Load Optimization with Incompatibilities

```python
def load_with_incompatibilities(shipments, truck_capacity, incompatible_pairs):
    """
    Load building with product incompatibility constraints

    Some products cannot be shipped together:
    - Food and chemicals
    - Different temperature requirements
    - Hazmat restrictions

    Parameters:
    -----------
    shipments : DataFrame
    truck_capacity : dict
    incompatible_pairs : list of tuples
        [(product_type_1, product_type_2), ...]

    Returns:
    --------
    Load plan respecting incompatibilities
    """

    from pulp import *

    # Create optimization model
    prob = LpProblem("Load_Building_Incompatibility", LpMinimize)

    # Maximum trucks needed (upper bound)
    max_trucks = len(shipments)
    trucks = range(max_trucks)

    # Decision variables
    # x[i,j] = 1 if shipment i in truck j
    x = LpVariable.dicts("load",
                        [(i, j) for i in shipments.index for j in trucks],
                        cat='Binary')

    # y[j] = 1 if truck j is used
    y = LpVariable.dicts("use_truck", trucks, cat='Binary')

    # Objective: minimize number of trucks
    prob += lpSum([y[j] for j in trucks]), "Minimize_Trucks"

    # Constraints

    # 1. Each shipment in exactly one truck
    for i in shipments.index:
        prob += lpSum([x[i, j] for j in trucks]) == 1, f"Shipment_{i}"

    # 2. Weight capacity
    for j in trucks:
        prob += lpSum([
            shipments.loc[i, 'weight'] * x[i, j]
            for i in shipments.index
        ]) <= truck_capacity['weight'] * y[j], f"Weight_{j}"

    # 3. Volume capacity
    for j in trucks:
        prob += lpSum([
            shipments.loc[i, 'volume'] * x[i, j]
            for i in shipments.index
        ]) <= truck_capacity['volume'] * y[j], f"Volume_{j}"

    # 4. Incompatibility constraints
    for (type1, type2) in incompatible_pairs:
        # Find shipments of each type
        shipments_type1 = shipments[shipments['product_type'] == type1].index
        shipments_type2 = shipments[shipments['product_type'] == type2].index

        # For each truck, can't have both types
        for j in trucks:
            # If any type1 in truck j, no type2 can be in truck j
            for i1 in shipments_type1:
                for i2 in shipments_type2:
                    prob += x[i1, j] + x[i2, j] <= 1, \
                            f"Incompatible_{i1}_{i2}_{j}"

    # 5. Link shipment assignment to truck usage
    for j in trucks:
        for i in shipments.index:
            prob += x[i, j] <= y[j], f"Link_{i}_{j}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    trucks_used = []
    for j in trucks:
        if y[j].varValue > 0.5:
            truck_shipments = [
                i for i in shipments.index
                if x[i, j].varValue > 0.5
            ]

            if truck_shipments:
                total_weight = shipments.loc[truck_shipments, 'weight'].sum()
                total_volume = shipments.loc[truck_shipments, 'volume'].sum()

                trucks_used.append({
                    'truck_id': j + 1,
                    'shipments': truck_shipments,
                    'num_shipments': len(truck_shipments),
                    'total_weight': total_weight,
                    'total_volume': total_volume,
                    'weight_util': total_weight / truck_capacity['weight'] * 100,
                    'volume_util': total_volume / truck_capacity['volume'] * 100
                })

    return {
        'status': LpStatus[prob.status],
        'trucks': pd.DataFrame(trucks_used),
        'num_trucks': len(trucks_used)
    }


# Example
shipments_typed = shipments.copy()
shipments_typed['product_type'] = np.random.choice(
    ['Food', 'Chemical', 'Electronics', 'Apparel'], 50
)

incompatible_pairs = [
    ('Food', 'Chemical'),
    ('Electronics', 'Chemical')
]

result_incomp = load_with_incompatibilities(
    shipments_typed, truck_capacity, incompatible_pairs
)

print(f"\nLoad Building with Incompatibilities:")
print(f"Status: {result_incomp['status']}")
print(f"Trucks Required: {result_incomp['num_trucks']}")
print("\nTruck Details:")
print(result_incomp['trucks'][['truck_id', 'num_shipments', 'weight_util', 'volume_util']])
```

---

## Tools & Libraries

### Load Building Software

**Transportation Management Systems (TMS):**
- **MercuryGate TMS**: Load optimization and planning
- **Oracle Transportation Management**: Load planning module
- **Blue Yonder (JDA) TMS**: Load building optimization
- **E2open TMS**: Automated load optimization

**Specialized Load Planning:**
- **TOPS Load Planning**: 3D load optimization
- **CargoWiz**: Container and truck load planning
- **CubiScan**: Dimensioning and load planning
- **Cargo Optimizer**: Advanced load building
- **LoadMaster**: Truck and container loading

**Warehouse Management Systems:**
- **Manhattan WMS**: Integrated load building
- **SAP EWM**: Load planning and optimization

### Python Libraries

```python
# Optimization
from pulp import *  # MIP modeling
from ortools.linear_solver import pywraplp  # Google OR-Tools

# 3D Packing
from py3dbp import Packer, Bin, Item  # 3D bin packing library

# Geometry and Visualization
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
```

---

## Common Challenges & Solutions

### Challenge: Cube vs. Weight Trade-Off

**Problem:**
- Reach weight capacity before filling volume (dense products)
- OR reach volume capacity with weight remaining (bulky, light items)
- "Cubing out" vs "weighing out"

**Solutions:**
- Mix dense and light shipments in same load
- Use freight class to identify imbalances
- Prioritize based on freight cost ($/lb vs $/cuft)
- Consider multi-stop routes to mix freight types
- Use dimensioners to capture accurate cube data

### Challenge: Route Sequence Conflicts

**Problem:**
- Optimal load packing conflicts with delivery sequence
- Need to unload 3rd stop before 1st stop (wrong order)
- Excessive re-handling at delivery

**Solutions:**
- Load in reverse delivery order (LIFO)
- Use zone loading (designate areas per stop)
- Accept lower utilization for multi-stop routes
- Consider direct shipments for conflicting stops
- Palletize by stop (stop 1 = pallets 1-5, etc.)

### Challenge: Product Incompatibilities

**Problem:**
- Food cannot ship with chemicals (contamination)
- Temperature zones (frozen, chilled, ambient)
- Hazmat regulations (incompatible classes)
- Odor contamination (fish, perfume)

**Solutions:**
- Separate trucks for incompatible products
- Physical barriers or partitions in truck
- Strict loading zones (front = food, back = non-food)
- Proper packaging and sealing
- Track incompatibility matrix in TMS/WMS

### Challenge: Irregular Package Shapes

**Problem:**
- Non-rectangular items (drums, coils, machinery)
- Can't efficiently pack with standard algorithm
- Wasted space around irregular shapes

**Solutions:**
- Custom 3D modeling for complex items
- Use dunnage/filling materials
- Dedicated trucks for oversized items
- Floor load for heavy irregular items
- Photography and 3D scanning for accurate models

### Challenge: Last-Minute Changes

**Problem:**
- Orders added/cancelled after load planned
- Must re-optimize on the fly
- Already-loaded trucks need adjustments

**Solutions:**
- Reserve 10-15% capacity for changes
- Real-time re-optimization algorithms
- Load building "windows" (finalize 2 hours before ship)
- Flexible loading sequence (add-ons go specific spots)
- Communicate cut-off times clearly

---

## Output Format

### Load Plan Report

**Truck Load Plan - Truck #TRK-001**

**Truck Specifications:**
- Type: 53' Dry Van
- Capacity: 45,000 lbs, 4,000 cu ft
- Dimensions: 53' L × 8.5' W × 9' H

**Load Summary:**

| Metric | Value | Utilization |
|--------|-------|-------------|
| Total Weight | 42,850 lbs | 95% |
| Total Volume | 3,420 cu ft | 86% |
| Number of Pallets | 24 | |
| Number of Shipments | 18 | |
| Number of Stops | 3 | |

**Shipments Included:**

| Shipment | Customer | Stop | Weight | Volume | Dimensions |
|----------|----------|------|--------|--------|------------|
| S001 | Acme Corp | 1 | 2,400 lbs | 180 cuft | 4×4×6 ft |
| S002 | Beta Inc | 1 | 1,850 lbs | 145 cuft | 4×4×5 ft |
| S005 | Gamma LLC | 2 | 3,200 lbs | 220 cuft | 4×4×7 ft |
| ... | ... | ... | ... | ... | ... |

**Load Sequence (Front to Back):**

```
Zone 1 (Stop 3 - Last Off): Shipments S015-S018
  - 8 pallets
  - 12,450 lbs
  - Positions: Rows 1-2

Zone 2 (Stop 2): Shipments S005-S014
  - 10 pallets
  - 18,200 lbs
  - Positions: Rows 3-5

Zone 3 (Stop 1 - First Off): Shipments S001-S004
  - 6 pallets
  - 12,200 lbs
  - Positions: Rows 6-7 (rear)
```

**Weight Distribution:**

- Steer Axle: 11,200 lbs (93% of 12,000 limit) ✓
- Drive Axle: 32,850 lbs (97% of 34,000 limit) ✓
- Trailer Axle: 31,650 lbs (93% of 34,000 limit) ✓
- **Total: 42,850 lbs - COMPLIANT**

**Load Diagram:**

```
Front (Cab)                                           Rear (Doors)
|------------|------------|------------|------------|------------|
| Zone 3     | Zone 2                  | Zone 1                 |
| Stop 1     | Stop 2                  | Stop 3                 |
| (First Off)| (Second Off)            | (Last Off)             |
|------------|------------|------------|------------|------------|
  Rows 6-7     Rows 3-5                  Rows 1-2
  6 pallets    10 pallets                8 pallets
```

**Performance vs. Alternative Plans:**

| Plan | Trucks | Avg Weight Util | Avg Cube Util | Cost |
|------|--------|-----------------|---------------|------|
| Optimized (Current) | 3 | 94% | 85% | $2,850 |
| Route-First Loading | 4 | 78% | 72% | $3,800 |
| Manual Loading | 4 | 81% | 68% | $3,800 |
| **Savings** | **25%** | | | **$950** |

**Recommendations:**
1. Excellent utilization - well-balanced load
2. Consider adding 2 more pallets (capacity available)
3. Monitor axle weights during loading

---

## Questions to Ask

If you need more context:
1. What type of trucks/trailers (dry van, reefer, flatbed)?
2. What are the trailer dimensions and weight limits?
3. What's your daily shipment volume?
4. Are loads single-stop or multi-stop?
5. What's your current cube/weight utilization?
6. Do you have product incompatibilities or restrictions?
7. What load planning method do you currently use?
8. Do you have accurate dimensions for shipments?

---

## Related Skills

- **pallet-loading**: For optimizing pallet configuration
- **container-loading-optimization**: For shipping containers
- **vehicle-loading-optimization**: For various vehicle types
- **3d-bin-packing**: For 3D packing algorithms
- **route-optimization**: For coordinating load building with routes
- **freight-optimization**: For freight cost optimization
- **knapsack-problems**: For theoretical background on packing
- **warehouse-slotting-optimization**: For staging shipments before loading
