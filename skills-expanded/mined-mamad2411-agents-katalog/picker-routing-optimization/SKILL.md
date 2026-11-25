---
name: picker-routing-optimization
description: When the user wants to optimize picker routes, minimize travel distance in warehouses, or improve picking efficiency. Also use when the user mentions "pick path optimization," "warehouse routing," "travel distance minimization," "TSP in warehouses," "S-shape routing," or "optimal pick sequence." For order batching, see order-batching-optimization. For warehouse slotting, see warehouse-slotting-optimization.
---

# Picker Routing Optimization

You are an expert in warehouse picker routing and travel path optimization. Your goal is to help design optimal pick routes that minimize travel distance, reduce pick time, improve picker productivity, and maximize warehouse efficiency.

## Initial Assessment

Before optimizing picker routing, understand:

1. **Warehouse Layout**
   - Layout type (grid, diagonal, mixed)?
   - Number of aisles and length?
   - Aisle width (two-way or one-way)?
   - Cross-aisles (mid-points, ends only)?
   - Pick face configuration (single-sided, double-sided)?
   - Depot/staging location?

2. **Picking Constraints**
   - Pick method (discrete, batch, zone)?
   - Equipment (walk, picker cart, forklift, reach truck)?
   - Can skip aisles if no picks?
   - Can traverse aisles both ways?
   - Can cross aisles mid-way?
   - Pick list sequence flexibility?

3. **Order Characteristics**
   - Average picks per order/batch?
   - Pick density (picks per aisle)?
   - Pick distribution across warehouse?
   - Item location patterns?

4. **Current Performance**
   - Current routing method?
   - Average travel distance per order?
   - Picks per hour?
   - Picker feedback on routes?

---

## Picker Routing Framework

### Routing Strategies

**1. S-Shape (Traversal) Routing**
- Enter each aisle with picks, traverse completely
- Exit at far end, skip to next aisle with picks
- **Pros**: Simple, no backtracking within aisles
- **Cons**: May traverse empty portions of aisles
- **Efficiency**: Moderate (60-70% of optimal)

**2. Return Routing**
- Enter aisle, pick items, return to same end
- Move to next aisle
- **Pros**: Very simple, predictable
- **Cons**: High backtracking, longest distance
- **Efficiency**: Poor (40-50% of optimal)
- **Use**: Narrow aisles, one-way traffic only

**3. Midpoint Routing**
- If picks in front half, use return from front
- If picks in back half, traverse to back
- Requires cross-aisle in middle
- **Pros**: Better than pure S-shape or return
- **Cons**: Requires cross-aisle infrastructure
- **Efficiency**: Good (70-80% of optimal)

**4. Largest Gap Routing**
- Identify largest gap between picks in aisle
- Enter/exit to avoid traversing largest gap
- **Pros**: Adapts to pick distribution
- **Cons**: More complex, requires calculation
- **Efficiency**: Very good (80-90% of optimal)

**5. Optimal Routing (TSP-based)**
- Solve as Traveling Salesman Problem
- Find shortest path visiting all picks
- **Pros**: Best possible route
- **Cons**: Complex computation (NP-hard)
- **Efficiency**: Optimal (100%)

### Routing Objectives

```
Primary Goal:
  Minimize total travel distance

Secondary Goals:
  - Minimize pick time (travel + access)
  - Balance picker workload
  - Respect aisle traffic constraints
  - Maintain pick accuracy (logical sequence)

Constraints:
  - Aisle layout (can't cut through racks)
  - One-way aisles (directional constraints)
  - Congestion (avoid other pickers)
  - Equipment limitations (turning radius, height)
```

---

## Mathematical Formulation

### Warehouse as a Graph

Model warehouse as a directed graph G = (V, E):

**Vertices (V):**
- Pick locations
- Aisle endpoints
- Cross-aisle intersections
- Depot (start/end point)

**Edges (E):**
- Travel segments between vertices
- Edge weights = distance or time
- Directed edges for one-way aisles

**Routing Problem:**
```
Find shortest path from depot visiting all pick locations
and returning to depot

This is a variant of the Traveling Salesman Problem (TSP)
with special structure (rectilinear geometry)
```

### TSP Formulation for Warehouse

**Decision Variables:**
- x[i,j] = 1 if picker travels from location i to j, 0 otherwise
- u[i] = position of location i in route (for subtour elimination)

**Parameters:**
- d[i,j] = distance from location i to j
- P = set of pick locations
- depot = start/end point

**Objective:**

```
Minimize: Σ Σ (d[i,j] × x[i,j])  for all i,j in (P ∪ {depot})
```

**Constraints:**

```python
# 1. Leave each location exactly once (except depot twice - start and end)
for i in P:
    Σ x[i,j] = 1  for all j != i

# 2. Enter each location exactly once
for j in P:
    Σ x[i,j] = 1  for all i != j

# 3. Flow conservation
for k in P:
    Σ x[i,k] = Σ x[k,j]  for all i,j

# 4. Start and end at depot
Σ x[depot,j] = 1  for all j in P
Σ x[i,depot] = 1  for all i in P

# 5. Subtour elimination (Miller-Tucker-Zemlin)
for i,j in P:
    u[i] - u[j] + n × x[i,j] <= n - 1

# 6. Aisle constraints (can't pass through racks)
for i,j not adjacent:
    if no path exists:
        x[i,j] = 0
```

---

## Routing Algorithms

### S-Shape Routing

```python
import numpy as np
import pandas as pd

def s_shape_routing(picks, aisles, cross_aisle_locations):
    """
    S-Shape routing algorithm

    Parameters:
    -----------
    picks : DataFrame
        Columns: pick_id, aisle, position_in_aisle, side (left/right)
    aisles : dict
        {aisle_id: {'length': length, 'width': width}}
    cross_aisle_locations : dict
        {aisle_id: [positions...]}  # Where cross-aisles exist

    Returns:
    --------
    Route sequence and total distance
    """

    # Group picks by aisle
    picks_by_aisle = picks.groupby('aisle')

    route = []
    total_distance = 0
    current_position = 0  # Start at position 0 (front of warehouse)
    current_aisle = 0  # Start at aisle 0

    # Get aisles with picks (sorted)
    aisles_with_picks = sorted(picks_by_aisle.groups.keys())

    for aisle_id in aisles_with_picks:
        aisle_picks = picks_by_aisle.get_group(aisle_id).sort_values('position_in_aisle')

        # Move to aisle (cross-aisle travel)
        cross_aisle_distance = abs(aisle_id - current_aisle) * aisles[0].get('width', 10)
        total_distance += cross_aisle_distance

        # Determine entry point (front or back)
        # For S-shape: alternate front and back entry
        aisle_index = aisles_with_picks.index(aisle_id)

        if aisle_index % 2 == 0:
            # Enter from front, traverse to back
            entry_position = 0
            exit_position = aisles[aisle_id]['length']
            picks_order = aisle_picks.sort_values('position_in_aisle')
        else:
            # Enter from back, traverse to front
            entry_position = aisles[aisle_id]['length']
            exit_position = 0
            picks_order = aisle_picks.sort_values('position_in_aisle', ascending=False)

        # Move to entry point
        total_distance += abs(entry_position - current_position)

        # Traverse aisle and pick items
        for idx, pick in picks_order.iterrows():
            route.append({
                'pick_id': pick['pick_id'],
                'aisle': aisle_id,
                'position': pick['position_in_aisle'],
                'sequence': len(route) + 1
            })

        # Add traversal distance
        total_distance += abs(exit_position - entry_position)

        current_position = exit_position
        current_aisle = aisle_id

    # Return to depot
    total_distance += abs(current_position - 0)
    total_distance += abs(current_aisle - 0) * aisles[0].get('width', 10)

    return {
        'route': pd.DataFrame(route),
        'total_distance': total_distance,
        'num_picks': len(picks)
    }


# Example usage
picks = pd.DataFrame({
    'pick_id': [f'P{i:03d}' for i in range(1, 21)],
    'aisle': np.random.randint(1, 11, 20),  # 10 aisles
    'position_in_aisle': np.random.uniform(0, 100, 20),  # 100 ft aisles
    'side': np.random.choice(['left', 'right'], 20)
})

aisles = {i: {'length': 100, 'width': 12} for i in range(1, 11)}
cross_aisles = {i: [0, 100] for i in range(1, 11)}  # Front and back only

result = s_shape_routing(picks, aisles, cross_aisles)
print(f"S-Shape Routing:")
print(f"Total Distance: {result['total_distance']:.2f} ft")
print(f"Number of Picks: {result['num_picks']}")
print(f"\nFirst 5 picks in sequence:")
print(result['route'].head())
```

### Largest Gap Routing

```python
def largest_gap_routing(picks, aisles):
    """
    Largest gap routing algorithm

    For each aisle:
    - If picks only in front half: enter and return from front
    - If picks only in back half: enter and return from back
    - If picks in both halves: enter from one side, exit from other (S-shape)
      but choose entry/exit to minimize distance

    Parameters:
    -----------
    picks : DataFrame
        Pick locations
    aisles : dict
        Aisle specifications

    Returns:
    --------
    Optimized route
    """

    picks_by_aisle = picks.groupby('aisle')

    route = []
    total_distance = 0
    current_position = 0
    current_aisle = 0

    aisles_with_picks = sorted(picks_by_aisle.groups.keys())

    for aisle_id in aisles_with_picks:
        aisle_picks = picks_by_aisle.get_group(aisle_id).sort_values('position_in_aisle')
        aisle_length = aisles[aisle_id]['length']

        # Find largest gap between consecutive picks
        positions = sorted(aisle_picks['position_in_aisle'].tolist())

        # Add aisle endpoints to gap calculation
        gaps = []
        gaps.append({'gap_size': positions[0] - 0,
                    'start': 0, 'end': positions[0]})

        for i in range(len(positions) - 1):
            gaps.append({'gap_size': positions[i+1] - positions[i],
                        'start': positions[i], 'end': positions[i+1]})

        gaps.append({'gap_size': aisle_length - positions[-1],
                    'start': positions[-1], 'end': aisle_length})

        largest_gap = max(gaps, key=lambda x: x['gap_size'])

        # Determine routing strategy based on largest gap location
        if largest_gap['start'] == 0:
            # Largest gap at front, enter from back
            entry_position = aisle_length
            exit_position = aisle_length
            picks_order = aisle_picks.sort_values('position_in_aisle', ascending=False)

        elif largest_gap['end'] == aisle_length:
            # Largest gap at back, enter from front
            entry_position = 0
            exit_position = 0
            picks_order = aisle_picks.sort_values('position_in_aisle')

        else:
            # Largest gap in middle, traverse around it
            # Enter from front, exit from back (or vice versa)
            # Choose direction that minimizes total travel

            # Option 1: Front to back
            dist1 = aisle_length - largest_gap['gap_size']

            # Option 2: Back to front
            dist2 = aisle_length - largest_gap['gap_size']

            # Both same for middle gaps, so use S-shape logic
            if current_position < aisle_length / 2:
                entry_position = 0
                exit_position = aisle_length
                picks_order = aisle_picks.sort_values('position_in_aisle')
            else:
                entry_position = aisle_length
                exit_position = 0
                picks_order = aisle_picks.sort_values('position_in_aisle', ascending=False)

        # Move to aisle
        cross_aisle_distance = abs(aisle_id - current_aisle) * aisles[0].get('width', 10)
        total_distance += cross_aisle_distance

        # Move to entry point
        total_distance += abs(entry_position - current_position)

        # Pick items
        for idx, pick in picks_order.iterrows():
            route.append({
                'pick_id': pick['pick_id'],
                'aisle': aisle_id,
                'position': pick['position_in_aisle'],
                'sequence': len(route) + 1
            })

        # Calculate actual travel distance in aisle (excluding largest gap if avoided)
        if entry_position == exit_position:
            # Return routing
            furthest_pick = picks_order.iloc[-1]['position_in_aisle']
            aisle_travel = 2 * abs(furthest_pick - entry_position)
        else:
            # Traversal routing (minus largest gap if skipped)
            aisle_travel = abs(exit_position - entry_position)

        total_distance += aisle_travel

        current_position = exit_position
        current_aisle = aisle_id

    # Return to depot
    total_distance += abs(current_position - 0)
    total_distance += abs(current_aisle - 0) * aisles[0].get('width', 10)

    return {
        'route': pd.DataFrame(route) if route else pd.DataFrame(),
        'total_distance': total_distance,
        'num_picks': len(picks)
    }


result_lg = largest_gap_routing(picks, aisles)
print(f"\nLargest Gap Routing:")
print(f"Total Distance: {result_lg['total_distance']:.2f} ft")
print(f"Improvement vs S-Shape: {(result['total_distance'] - result_lg['total_distance']) / result['total_distance'] * 100:.1f}%")
```

### TSP-Based Optimal Routing

```python
from scipy.spatial.distance import pdist, squareform
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def tsp_optimal_routing(picks, warehouse_graph):
    """
    Optimal routing using TSP solver (Google OR-Tools)

    Parameters:
    -----------
    picks : DataFrame
        Pick locations with x, y coordinates
    warehouse_graph : dict
        Distance matrix considering warehouse layout constraints

    Returns:
    --------
    Optimal route
    """

    # Create distance matrix
    # In real warehouse, distance is constrained by aisles (not Euclidean)
    # Use warehouse_graph or calculate Manhattan distance

    locations = picks[['x', 'y']].values
    n_locations = len(locations)

    # Add depot (0, 0)
    depot_location = np.array([[0, 0]])
    all_locations = np.vstack([depot_location, locations])

    # Calculate distance matrix (Manhattan distance for warehouse)
    def manhattan_distance(loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    n = len(all_locations)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = manhattan_distance(
                    all_locations[i], all_locations[j]
                )

    # Convert to integer (OR-Tools requirement)
    distance_matrix = (distance_matrix * 100).astype(int)

    # Create routing model
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)  # n locations, 1 vehicle, depot=0
    routing = pywrapcp.RoutingModel(manager)

    # Create distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 10

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # Extract route
        route = []
        index = routing.Start(0)
        total_distance = 0

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            if node > 0:  # Skip depot at start
                route.append({
                    'pick_id': picks.iloc[node - 1]['pick_id'],
                    'x': picks.iloc[node - 1]['x'],
                    'y': picks.iloc[node - 1]['y'],
                    'sequence': len(route) + 1
                })

            next_index = solution.Value(routing.NextVar(index))
            total_distance += routing.GetArcCostForVehicle(index, next_index, 0)
            index = next_index

        return {
            'route': pd.DataFrame(route),
            'total_distance': total_distance / 100,  # Convert back from integer
            'num_picks': len(picks),
            'optimal': True
        }

    return {'route': pd.DataFrame(), 'total_distance': 0, 'optimal': False}


# Example with coordinates
picks_with_coords = pd.DataFrame({
    'pick_id': [f'P{i:03d}' for i in range(1, 21)],
    'x': np.random.uniform(0, 100, 20),  # x coordinate (across aisles)
    'y': np.random.uniform(0, 100, 20),  # y coordinate (down aisle)
})

# Note: In real implementation, would use actual warehouse graph
# that respects aisle structure

result_tsp = tsp_optimal_routing(picks_with_coords, warehouse_graph={})
if result_tsp['optimal']:
    print(f"\nTSP Optimal Routing:")
    print(f"Total Distance: {result_tsp['total_distance']:.2f} ft")
    print(f"First 5 picks:")
    print(result_tsp['route'].head())
```

---

## Advanced Routing Techniques

### Dynamic Routing with Congestion Avoidance

```python
class DynamicRouter:
    """
    Dynamic routing that adapts to warehouse congestion
    """

    def __init__(self, warehouse_layout, real_time_tracking=False):
        self.warehouse_layout = warehouse_layout
        self.real_time_tracking = real_time_tracking
        self.picker_locations = {}  # {picker_id: (aisle, position)}
        self.congestion_map = {}  # {aisle: congestion_level}

    def update_picker_location(self, picker_id, aisle, position):
        """Update picker location for congestion tracking"""
        self.picker_locations[picker_id] = (aisle, position)
        self.update_congestion_map()

    def update_congestion_map(self):
        """Calculate congestion level for each aisle"""
        aisle_counts = {}
        for picker_id, (aisle, position) in self.picker_locations.items():
            aisle_counts[aisle] = aisle_counts.get(aisle, 0) + 1

        # Congestion level: number of pickers / aisle capacity
        for aisle in self.warehouse_layout['aisles']:
            count = aisle_counts.get(aisle, 0)
            capacity = 3  # Assume max 3 pickers per aisle comfortably
            self.congestion_map[aisle] = count / capacity

    def route_with_congestion(self, picks, picker_id):
        """
        Calculate route considering current congestion

        Penalize aisles with high congestion
        """

        # Start with base routing algorithm (e.g., largest gap)
        base_route = largest_gap_routing(picks, self.warehouse_layout['aisles'])

        if not self.real_time_tracking:
            return base_route

        # Adjust route based on congestion
        # Re-sequence to visit less congested aisles first

        route_df = base_route['route'].copy()
        route_df['aisle'] = picks.set_index('pick_id').loc[route_df['pick_id'], 'aisle'].values
        route_df['congestion'] = route_df['aisle'].map(self.congestion_map).fillna(0)

        # Sort picks within each priority group by congestion
        route_df = route_df.sort_values(['congestion', 'aisle'])
        route_df['sequence'] = range(1, len(route_df) + 1)

        return {
            'route': route_df,
            'total_distance': base_route['total_distance'] * 1.05,  # Slight penalty for re-sequencing
            'congestion_adjusted': True
        }


# Example usage
warehouse_layout = {
    'aisles': list(range(1, 11)),
    'aisle_specs': {i: {'length': 100, 'width': 12} for i in range(1, 11)}
}

router = DynamicRouter(warehouse_layout, real_time_tracking=True)

# Simulate other pickers
router.update_picker_location('picker_1', aisle=3, position=50)
router.update_picker_location('picker_2', aisle=3, position=30)
router.update_picker_location('picker_3', aisle=7, position=60)

# Route new picker
route_dynamic = router.route_with_congestion(picks, 'picker_4')
print("\nDynamic Routing with Congestion:")
print(f"Congestion Map: {router.congestion_map}")
```

### Multi-Level Warehouse Routing

```python
def multi_level_routing(picks, levels, vertical_travel_time=30):
    """
    Routing for multi-level warehouses (mezzanines, multi-story)

    Parameters:
    -----------
    picks : DataFrame
        Picks with level, aisle, position
    levels : list
        Available levels
    vertical_travel_time : float
        Seconds to move between levels

    Returns:
    --------
    Optimized route considering vertical travel
    """

    # Group picks by level
    picks_by_level = picks.groupby('level')

    # Strategy: Minimize level changes
    # Visit all picks on one level before moving to next

    route = []
    total_distance = 0
    total_time = 0
    current_level = 1  # Start at ground level

    # Determine optimal level sequence
    # Heuristic: Ground level first, then upper levels in order

    level_sequence = sorted(picks_by_level.groups.keys())

    for level in level_sequence:
        level_picks = picks_by_level.get_group(level)

        # Move to level (vertical travel)
        if level != current_level:
            level_changes = abs(level - current_level)
            total_time += level_changes * vertical_travel_time
            current_level = level

        # Route within level (use largest gap or TSP)
        level_route = largest_gap_routing(
            level_picks,
            aisles={i: {'length': 100, 'width': 12} for i in range(1, 11)}
        )

        # Add to total route
        level_route_df = level_route['route']
        level_route_df['level'] = level
        route.append(level_route_df)

        total_distance += level_route['total_distance']

    # Combine all levels
    full_route = pd.concat(route, ignore_index=True)
    full_route['sequence'] = range(1, len(full_route) + 1)

    return {
        'route': full_route,
        'total_distance': total_distance,
        'total_time': total_time,
        'num_picks': len(picks),
        'levels_visited': len(level_sequence)
    }


# Example
picks_multi_level = pd.DataFrame({
    'pick_id': [f'P{i:03d}' for i in range(1, 31)],
    'level': np.random.choice([1, 2, 3], 30),
    'aisle': np.random.randint(1, 11, 30),
    'position_in_aisle': np.random.uniform(0, 100, 30),
})

result_ml = multi_level_routing(picks_multi_level, levels=[1, 2, 3])
print("\nMulti-Level Routing:")
print(f"Total Distance: {result_ml['total_distance']:.2f} ft")
print(f"Vertical Travel Time: {result_ml['total_time']:.0f} sec")
print(f"Levels Visited: {result_ml['levels_visited']}")
```

---

## Tools & Libraries

### Routing Software

**Warehouse Management Systems:**
- **Manhattan WMS**: Optimized pick path generation
- **Blue Yonder (JDA) WMS**: AI-driven routing
- **SAP EWM**: Pick-by-order and pick-by-wave routing
- **HighJump WMS**: Dynamic routing with real-time updates

**Specialized Optimization:**
- **Lucas Systems**: Voice-directed picking with optimized routes
- **Voxware**: Voice picking with intelligent routing
- **Google OR-Tools**: Open-source routing optimization
- **Gurobi/CPLEX**: Commercial optimization solvers

### Python Libraries

```python
# Routing Optimization
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from scipy.optimize import linear_sum_assignment
import networkx as nx  # Graph algorithms

# TSP Solvers
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing

# Distance Calculations
from scipy.spatial.distance import pdist, squareform, cityblock
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import matplotlib.patches as patches
```

---

## Common Challenges & Solutions

### Challenge: One-Way Aisles

**Problem:**
- Narrow aisles, only one-way traffic
- Can't use S-shape (can't traverse both directions)
- Must return from entry point

**Solutions:**
- Use return routing as baseline
- Optimize entry/exit points (front vs back)
- Use midpoint if cross-aisle available
- Consider widening key aisles for two-way traffic
- Implement aisle direction alternation (odd/even)

### Challenge: Congestion and Blocking

**Problem:**
- Multiple pickers in same aisle
- Blocking and waiting time
- Routes become longer due to avoidance

**Solutions:**
- Real-time routing with congestion awareness
- Stagger picker start times (offset by 5-10 min)
- Zone-based picking (dedicate aisles to pickers)
- Dynamic re-routing via mobile app/voice system
- Traffic flow analysis to identify bottlenecks

### Challenge: Large Pick Lists

**Problem:**
- 100+ pick locations in single order/batch
- TSP becomes computationally expensive
- Real-time routing not feasible

**Solutions:**
- Use heuristics (largest gap, S-shape) instead of TSP
- Divide into smaller batches
- Pre-compute routes offline (for recurring orders)
- Use approximate TSP (LKH, Christofides)
- Time limit on optimization (best route in 5 seconds)

### Challenge: Variable Pick Times

**Problem:**
- Some picks take 5 seconds, others 60 seconds
- Heavy items, high shelves, quantity picks
- Distance-based routing ignores time variability

**Solutions:**
- Weight edges by time, not distance
- Include pick time in route optimization
- Sequence difficult picks first (when picker fresh)
- Pre-stage heavy/bulky items (separate workflow)
- Use time-motion studies to calibrate

### Challenge: Layout Changes

**Problem:**
- Warehouse layout changes (slotting refresh)
- Routes become suboptimal
- Pickers confused by location changes

**Solutions:**
- Re-compute routes after slotting changes
- Gradual rollout (zone by zone)
- Update WMS location master immediately
- Train pickers on new layout
- Use RF/voice to direct (location-agnostic)

---

## Output Format

### Picker Routing Report

**Route Optimization Analysis - Order #12345**

**Pick List Summary:**
- Total Picks: 42 lines
- Aisles Involved: 8 aisles (2, 4, 5, 7, 9, 11, 13, 15)
- Warehouse Zones: A (18 picks), B (15 picks), C (9 picks)

**Routing Comparison:**

| Method | Distance (ft) | Est. Time (min) | Improvement |
|--------|---------------|-----------------|-------------|
| Return Routing | 1,845 | 28.5 | Baseline |
| S-Shape Routing | 1,124 | 17.4 | 39% |
| Largest Gap | 892 | 13.8 | 52% |
| TSP Optimal | 834 | 12.9 | 55% |

**Recommended Route (Largest Gap):**

```
Sequence | Pick ID | SKU | Aisle | Position | Side | Qty |
---------|---------|-----|-------|----------|------|-----|
1 | P001 | SKU_A | 2 | 15.3 | L | 2 |
2 | P002 | SKU_B | 2 | 28.7 | R | 1 |
3 | P003 | SKU_C | 2 | 45.2 | L | 3 |
4 | [Cross to Aisle 4]
5 | P008 | SKU_H | 4 | 82.1 | R | 1 |
6 | P009 | SKU_I | 4 | 67.3 | L | 2 |
...
```

**Route Visualization:**

```
Depot (Start)
  ↓
Aisle 2 [Enter Front → Pick 3 items → Exit Front]
  ↓
Cross-Aisle Travel (2 → 4)
  ↓
Aisle 4 [Enter Back → Pick 5 items → Exit Front]
  ↓
Cross-Aisle Travel (4 → 5)
  ↓
Aisle 5 [Enter Front → Pick 4 items → Exit Front]
...
  ↓
Return to Depot (End)

Total Distance: 892 ft
Estimated Time: 13.8 minutes (assuming 100 ft/min walk + 10 sec/pick)
```

**Performance Metrics:**
- Distance per Pick: 21.2 ft/pick
- Estimated Picks per Hour: 182 (vs. 145 with return routing)
- Productivity Improvement: +26%

---

## Questions to Ask

If you need more context:
1. What's your warehouse layout (grid, cross-aisles)?
2. Are aisles one-way or two-way?
3. What picking method (discrete, batch, zone)?
4. What's your average picks per order/batch?
5. What routing method do you currently use?
6. What's your current picks per hour?
7. Do you have WMS with routing capability?
8. Any congestion or blocking issues?

---

## Related Skills

- **traveling-salesman-problem**: For TSP algorithms and theory
- **order-batching-optimization**: For creating optimal batches to route
- **warehouse-slotting-optimization**: For SKU placement affecting routes
- **wave-planning-optimization**: For wave design impacting routing
- **network-flow-optimization**: For warehouse flow modeling
- **graph-algorithms**: For shortest path and routing
- **metaheuristic-optimization**: For large-scale routing problems
