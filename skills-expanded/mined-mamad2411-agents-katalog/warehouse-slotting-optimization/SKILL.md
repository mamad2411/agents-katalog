---
name: warehouse-slotting-optimization
description: When the user wants to optimize warehouse slot assignments, improve pick efficiency, or design warehouse layouts. Also use when the user mentions "slotting optimization," "slot assignment," "ABC slotting," "pick path optimization," "storage location assignment," "warehouse layout optimization," or "forward pick locations." For picker routing, see picker-routing-optimization. For warehouse design, see warehouse-design.
---

# Warehouse Slotting Optimization

You are an expert in warehouse slotting optimization and storage location assignment. Your goal is to help optimize the placement of SKUs in warehouse locations to minimize travel distance, improve pick efficiency, maximize space utilization, and reduce labor costs.

## Initial Assessment

Before optimizing slotting, understand:

1. **Warehouse Characteristics**
   - Warehouse layout? (zones, aisles, levels)
   - Total storage locations and capacity?
   - Pick zones (forward pick, reserve, bulk)?
   - Equipment types? (forklifts, pickers, automated systems)
   - Current slotting method? (manual, ABC analysis, random)

2. **Product Profile**
   - Number of SKUs?
   - Product dimensions and weight?
   - Velocity (picks per day/week)?
   - Seasonality and demand patterns?
   - Cube movement (cubic feet × picks)?

3. **Operational Constraints**
   - FIFO/FEFO requirements?
   - Hazmat or compatibility restrictions?
   - Temperature zones?
   - Max weight per location/level?
   - Replenishment frequency?

4. **Business Objectives**
   - Primary goal? (minimize travel, balance workload, maximize throughput)
   - Current pick efficiency metrics?
   - Expected order profile changes?
   - Slotting refresh frequency?

---

## Slotting Optimization Framework

### Slotting Principles

**1. Golden Zone Principle**
- Place fast movers in most accessible locations
- Eye level (waist to shoulder height) is optimal
- Minimize bending and reaching
- Reduce picker fatigue

**2. Cube-per-Order Index (COI)**
- Formula: COI = Cubic Volume / Orders per Period
- Lower COI = More picks per cubic foot = Better slot candidate
- Prioritize high-pick, low-cube items in forward pick

**3. ABC Velocity Analysis**
- **A items**: Top 20% SKUs, 80% of picks → Prime locations
- **B items**: Next 30% SKUs, 15% of picks → Secondary locations
- **C items**: Bottom 50% SKUs, 5% of picks → Reserve locations

**4. Correlated Picks**
- Items frequently ordered together should be close
- Reduces travel between picks
- Cluster analysis on order history

**5. Product Affinity**
- Group similar products (size, category, handling)
- Improves replenishment efficiency
- Facilitates cross-training

---

## Mathematical Formulation

### Quadratic Assignment Problem (QAP)

Slotting optimization is fundamentally a Quadratic Assignment Problem:

**Decision Variables:**
- x[i,j] = 1 if SKU i is assigned to location j, 0 otherwise

**Objective:**
Minimize total travel distance weighted by pick frequency

```
minimize: Σ Σ Σ Σ (f[i,k] × d[j,l] × x[i,j] × x[k,l])
          i k j l

where:
- f[i,k] = frequency SKU i and k are picked together
- d[j,l] = distance between location j and l
- x[i,j] = 1 if SKU i assigned to location j
```

**Constraints:**

```python
# 1. Each SKU assigned to exactly one location
for i in SKUs:
    Σ x[i,j] = 1  for all j in Locations

# 2. Each location holds at most one SKU (can be relaxed)
for j in Locations:
    Σ x[i,j] ≤ 1  for all i in SKUs

# 3. Capacity constraints
for j in Locations:
    Σ (size[i] × x[i,j]) ≤ capacity[j]  for all i

# 4. Compatibility constraints (hazmat, temperature, etc.)
for i in SKUs:
    for j in Locations:
        if not compatible(i, j):
            x[i,j] = 0
```

---

## Slotting Algorithms

### ABC Slotting (Basic)

```python
import pandas as pd
import numpy as np

def abc_slotting_analysis(sku_data):
    """
    Perform ABC analysis for warehouse slotting

    Parameters:
    -----------
    sku_data : DataFrame with columns
        - sku_id: Product identifier
        - picks_per_month: Number of picks
        - cube_per_unit: Cubic feet per unit
        - units_per_pick: Average units per pick

    Returns:
    --------
    DataFrame with ABC classification and slotting recommendations
    """

    df = sku_data.copy()

    # Calculate total cube moved
    df['cube_moved'] = (df['picks_per_month'] *
                        df['units_per_pick'] *
                        df['cube_per_unit'])

    # Calculate Cube-per-Order Index (COI)
    df['coi'] = df['cube_per_unit'] / (df['picks_per_month'] + 1)

    # Sort by picks (velocity)
    df = df.sort_values('picks_per_month', ascending=False)

    # Calculate cumulative percentage of picks
    df['cumulative_picks'] = df['picks_per_month'].cumsum()
    total_picks = df['picks_per_month'].sum()
    df['pick_percentage'] = (df['cumulative_picks'] / total_picks) * 100

    # ABC Classification
    df['abc_class'] = pd.cut(
        df['pick_percentage'],
        bins=[0, 80, 95, 100],
        labels=['A', 'B', 'C']
    )

    # Slotting recommendations
    def get_zone_recommendation(row):
        if row['abc_class'] == 'A':
            if row['coi'] < 0.1:
                return 'Forward Pick - Golden Zone'
            else:
                return 'Forward Pick - Lower Priority'
        elif row['abc_class'] == 'B':
            return 'Forward Pick - Edge Locations'
        else:
            return 'Reserve Storage'

    df['recommended_zone'] = df.apply(get_zone_recommendation, axis=1)

    # Priority score (lower is better)
    df['priority_score'] = (
        df['pick_percentage'].rank() * 0.5 +
        df['coi'].rank(ascending=False) * 0.3 +
        df['cube_moved'].rank(ascending=False) * 0.2
    )

    return df.sort_values('priority_score')


# Example usage
sku_data = pd.DataFrame({
    'sku_id': [f'SKU{i:04d}' for i in range(1, 101)],
    'picks_per_month': np.random.randint(1, 1000, 100),
    'cube_per_unit': np.random.uniform(0.5, 10, 100),
    'units_per_pick': np.random.randint(1, 5, 100)
})

slotting_analysis = abc_slotting_analysis(sku_data)

print("Top 10 SKUs for Golden Zone:")
print(slotting_analysis.head(10)[['sku_id', 'picks_per_month',
                                    'coi', 'abc_class', 'recommended_zone']])

print(f"\nABC Distribution:")
print(slotting_analysis['abc_class'].value_counts())
```

### Correlated Picks Analysis

```python
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform

def analyze_pick_correlation(order_lines_data):
    """
    Analyze which SKUs are frequently picked together

    Parameters:
    -----------
    order_lines_data : DataFrame with columns
        - order_id: Order identifier
        - sku_id: Product identifier
        - quantity: Units picked

    Returns:
    --------
    Correlation matrix and clustered SKU groups
    """

    # Create SKU co-occurrence matrix
    pivot = order_lines_data.pivot_table(
        index='order_id',
        columns='sku_id',
        values='quantity',
        fill_value=0,
        aggfunc='sum'
    )

    # Binary: SKU was in order or not
    binary_matrix = (pivot > 0).astype(int)

    # Calculate correlation between SKUs
    correlation_matrix = binary_matrix.corr()

    # Calculate pick affinity score
    # How often SKU i and j appear together / total orders
    n_orders = len(pivot)
    co_occurrence = binary_matrix.T.dot(binary_matrix)
    affinity_matrix = co_occurrence / n_orders

    # Cluster SKUs based on pick patterns
    n_clusters = min(10, len(pivot.columns) // 5)

    if len(pivot.columns) > 1:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(binary_matrix.T)

        sku_clusters = pd.DataFrame({
            'sku_id': pivot.columns,
            'cluster': clusters
        })

        # Add cluster size
        cluster_sizes = sku_clusters['cluster'].value_counts()
        sku_clusters['cluster_size'] = sku_clusters['cluster'].map(cluster_sizes)

    else:
        sku_clusters = pd.DataFrame({
            'sku_id': pivot.columns,
            'cluster': 0,
            'cluster_size': len(pivot.columns)
        })

    return {
        'correlation_matrix': correlation_matrix,
        'affinity_matrix': affinity_matrix,
        'sku_clusters': sku_clusters,
        'binary_matrix': binary_matrix
    }


def get_top_correlations(correlation_matrix, top_n=20):
    """Get top N SKU pairs with highest correlation"""

    # Get upper triangle (avoid duplicates)
    mask = np.triu(np.ones_like(correlation_matrix), k=1).astype(bool)
    upper_tri = correlation_matrix.where(mask)

    # Stack and sort
    correlations = upper_tri.stack().sort_values(ascending=False)

    return correlations.head(top_n)


# Example usage
order_lines = pd.DataFrame({
    'order_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5],
    'sku_id': ['A', 'B', 'C', 'A', 'B', 'A', 'D', 'E', 'B', 'C', 'A', 'B', 'C', 'F'],
    'quantity': [1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2]
})

correlation_analysis = analyze_pick_correlation(order_lines)
print("SKU Clusters (items to slot near each other):")
print(correlation_analysis['sku_clusters'].sort_values('cluster'))

top_corr = get_top_correlations(correlation_analysis['correlation_matrix'])
print("\nTop Correlated SKU Pairs:")
print(top_corr)
```

### Optimization Model: Slotting Assignment

```python
from pulp import *
import numpy as np

def optimize_slotting(skus, locations, pick_frequencies, distances,
                      sku_sizes, location_capacities, constraints=None):
    """
    Optimize warehouse slotting using Mixed-Integer Programming

    Parameters:
    -----------
    skus : list
        SKU identifiers
    locations : list
        Location identifiers
    pick_frequencies : dict
        {sku: picks_per_period}
    distances : dict
        {location: distance_from_depot} or distance matrix
    sku_sizes : dict
        {sku: cubic_feet}
    location_capacities : dict
        {location: max_cubic_feet}
    constraints : dict, optional
        Additional constraints (compatibility, etc.)

    Returns:
    --------
    Optimal slotting assignment
    """

    # Create problem
    prob = LpProblem("Warehouse_Slotting", LpMinimize)

    # Decision variables: x[i,j] = 1 if SKU i assigned to location j
    x = LpVariable.dicts("assign",
                         [(i, j) for i in skus for j in locations],
                         cat='Binary')

    # Objective: Minimize total travel distance weighted by pick frequency
    # Assuming distance is from central depot/staging area to location
    prob += lpSum([
        pick_frequencies.get(i, 0) * distances.get(j, 0) * x[i, j]
        for i in skus for j in locations
    ]), "Total_Weighted_Distance"

    # Constraints

    # 1. Each SKU must be assigned to exactly one location
    for i in skus:
        prob += lpSum([x[i, j] for j in locations]) == 1, f"SKU_{i}_Assignment"

    # 2. Each location can hold at most one SKU (can be relaxed)
    for j in locations:
        prob += lpSum([x[i, j] for i in skus]) <= 1, f"Location_{j}_Capacity_Count"

    # 3. Physical capacity constraints
    for j in locations:
        prob += lpSum([
            sku_sizes.get(i, 0) * x[i, j] for i in skus
        ]) <= location_capacities.get(j, float('inf')), f"Location_{j}_Volume"

    # 4. Additional constraints (if provided)
    if constraints and 'incompatible' in constraints:
        for (sku, loc) in constraints['incompatible']:
            if sku in skus and loc in locations:
                prob += x[sku, loc] == 0, f"Incompatible_{sku}_{loc}"

    if constraints and 'required' in constraints:
        for (sku, loc) in constraints['required']:
            if sku in skus and loc in locations:
                prob += x[sku, loc] == 1, f"Required_{sku}_{loc}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    assignments = {}
    for i in skus:
        for j in locations:
            if x[i, j].varValue > 0.5:
                assignments[i] = j
                break

    # Calculate metrics
    total_distance = sum(
        pick_frequencies.get(sku, 0) * distances.get(loc, 0)
        for sku, loc in assignments.items()
    )

    utilization = {}
    for j in locations:
        used = sum(
            sku_sizes.get(i, 0)
            for i, assigned_loc in assignments.items()
            if assigned_loc == j
        )
        capacity = location_capacities.get(j, 1)
        utilization[j] = (used / capacity * 100) if capacity > 0 else 0

    return {
        'status': LpStatus[prob.status],
        'assignments': assignments,
        'total_weighted_distance': total_distance,
        'location_utilization': utilization,
        'objective_value': value(prob.objective)
    }


# Example usage
skus = [f'SKU{i}' for i in range(1, 21)]
locations = [f'A{i:02d}' for i in range(1, 26)]  # 25 locations for 20 SKUs

# Generate sample data
np.random.seed(42)
pick_frequencies = {sku: np.random.randint(10, 1000) for sku in skus}
distances = {loc: np.random.uniform(10, 100) for loc in locations}
sku_sizes = {sku: np.random.uniform(1, 5) for sku in skus}
location_capacities = {loc: 10.0 for loc in locations}

# Add some constraints
constraints = {
    'incompatible': [('SKU1', 'A01'), ('SKU5', 'A25')],  # Example incompatibilities
}

result = optimize_slotting(
    skus, locations, pick_frequencies, distances,
    sku_sizes, location_capacities, constraints
)

print(f"Optimization Status: {result['status']}")
print(f"Total Weighted Distance: {result['total_weighted_distance']:,.2f}")
print(f"\nTop 10 Assignments (by pick frequency):")

# Sort by pick frequency
sorted_skus = sorted(skus, key=lambda s: pick_frequencies[s], reverse=True)[:10]
for sku in sorted_skus:
    loc = result['assignments'][sku]
    print(f"  {sku} → {loc} (picks: {pick_frequencies[sku]}, distance: {distances[loc]:.1f})")
```

### Hungarian Algorithm for Simple Assignment

```python
from scipy.optimize import linear_sum_assignment
import numpy as np

def hungarian_slotting(skus, locations, cost_matrix):
    """
    Use Hungarian algorithm for simple one-to-one slotting

    Parameters:
    -----------
    skus : list
        SKU identifiers
    locations : list
        Location identifiers
    cost_matrix : 2D array
        Cost[i,j] = cost of assigning sku i to location j

    Returns:
    --------
    Optimal assignment (when # SKUs = # locations)
    """

    # Ensure square matrix (pad if needed)
    n_skus = len(skus)
    n_locs = len(locations)

    if n_skus != n_locs:
        # Pad with dummy SKUs or locations
        max_dim = max(n_skus, n_locs)
        padded_cost = np.full((max_dim, max_dim), np.max(cost_matrix) * 10)
        padded_cost[:n_skus, :n_locs] = cost_matrix
        cost_matrix = padded_cost

    # Solve using Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Extract valid assignments (not dummy)
    assignments = {}
    total_cost = 0

    for i, j in zip(row_ind, col_ind):
        if i < n_skus and j < n_locs:
            assignments[skus[i]] = locations[j]
            total_cost += cost_matrix[i, j]

    return {
        'assignments': assignments,
        'total_cost': total_cost,
        'row_indices': row_ind[:n_skus],
        'col_indices': col_ind[:n_skus]
    }


# Example: Assign 10 SKUs to 10 best locations
skus = [f'SKU{i}' for i in range(1, 11)]
locations = [f'LOC{i}' for i in range(1, 11)]

# Cost = Pick frequency × Distance
# Lower cost = better assignment
np.random.seed(42)
pick_freq = np.random.randint(50, 500, 10)
distances = np.random.uniform(5, 50, 10)

# Cost matrix: each row is a SKU, each column is a location
cost_matrix = np.outer(pick_freq, distances)

result = hungarian_slotting(skus, locations, cost_matrix)

print("Hungarian Algorithm Assignment:")
print(f"Total Cost: {result['total_cost']:,.2f}")
print("\nAssignments:")
for sku, loc in result['assignments'].items():
    i = skus.index(sku)
    j = locations.index(loc)
    print(f"  {sku} → {loc} (cost: {cost_matrix[i,j]:,.2f})")
```

---

## Advanced Slotting Techniques

### Dynamic Slotting

```python
import pandas as pd
from datetime import datetime, timedelta

class DynamicSlottingOptimizer:
    """
    Dynamic slotting that adapts to changing demand patterns
    """

    def __init__(self, warehouse_layout, refresh_frequency='weekly'):
        self.warehouse_layout = warehouse_layout
        self.refresh_frequency = refresh_frequency
        self.slotting_history = []
        self.current_slotting = {}

    def calculate_velocity_trend(self, historical_picks, window_days=30):
        """
        Calculate velocity trends for each SKU

        Returns trending up, stable, or trending down
        """

        df = historical_picks.copy()
        df['date'] = pd.to_datetime(df['date'])

        # Calculate rolling average
        recent_end = df['date'].max()
        recent_start = recent_end - timedelta(days=window_days)
        older_start = recent_start - timedelta(days=window_days)

        recent_picks = df[df['date'] >= recent_start].groupby('sku_id')['picks'].sum()
        older_picks = df[
            (df['date'] >= older_start) & (df['date'] < recent_start)
        ].groupby('sku_id')['picks'].sum()

        velocity_change = (recent_picks - older_picks) / (older_picks + 1)

        trends = {}
        for sku in velocity_change.index:
            change = velocity_change[sku]
            if change > 0.2:
                trends[sku] = 'trending_up'
            elif change < -0.2:
                trends[sku] = 'trending_down'
            else:
                trends[sku] = 'stable'

        return trends

    def seasonal_adjustment(self, sku_id, current_month):
        """
        Apply seasonal factors to velocity
        """

        # Example seasonal factors (would be learned from historical data)
        seasonal_factors = {
            'toy_sku': {11: 2.5, 12: 3.0, 1: 0.5},  # Holiday season
            'apparel_sku': {3: 1.5, 4: 1.3, 9: 1.4, 10: 1.2},  # Spring/Fall
        }

        # Default factor
        return seasonal_factors.get(sku_id, {}).get(current_month, 1.0)

    def recommend_reslotting(self, current_slotting, velocity_trends,
                            threshold_change=0.3):
        """
        Recommend which SKUs should be reslotted
        """

        reslot_candidates = []

        for sku, current_zone in current_slotting.items():
            trend = velocity_trends.get(sku, 'stable')

            # High priority: trending up items in poor locations
            if trend == 'trending_up' and current_zone in ['Reserve', 'C_Zone']:
                reslot_candidates.append({
                    'sku': sku,
                    'reason': 'Trending up, needs better location',
                    'priority': 'High',
                    'current_zone': current_zone,
                    'recommended_zone': 'Forward Pick'
                })

            # Low priority: trending down items in prime locations
            elif trend == 'trending_down' and current_zone == 'Golden Zone':
                reslot_candidates.append({
                    'sku': sku,
                    'reason': 'Trending down, free up prime space',
                    'priority': 'Medium',
                    'current_zone': current_zone,
                    'recommended_zone': 'B_Zone or Reserve'
                })

        return pd.DataFrame(reslot_candidates)

    def minimize_disruption(self, old_slotting, new_slotting, max_moves=50):
        """
        Minimize number of moves when implementing new slotting

        Use cycle counting approach: only move most impactful SKUs
        """

        moves_needed = []

        for sku in new_slotting:
            old_loc = old_slotting.get(sku)
            new_loc = new_slotting.get(sku)

            if old_loc != new_loc:
                # Calculate impact of this move
                impact = self.calculate_move_impact(sku, old_loc, new_loc)
                moves_needed.append({
                    'sku': sku,
                    'from': old_loc,
                    'to': new_loc,
                    'impact': impact
                })

        # Sort by impact, take top N moves
        moves_df = pd.DataFrame(moves_needed)
        if len(moves_df) > 0:
            moves_df = moves_df.sort_values('impact', ascending=False)
            return moves_df.head(max_moves)

        return moves_df

    def calculate_move_impact(self, sku, old_loc, new_loc):
        """
        Estimate benefit of moving SKU from old to new location
        """
        # Simplified: would use actual distances and pick frequencies
        # Higher impact = more important to move
        return np.random.uniform(0, 100)  # Placeholder


# Example usage
optimizer = DynamicSlottingOptimizer(warehouse_layout={})

# Simulate historical picks
historical_data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=90),
    'sku_id': np.random.choice(['SKU1', 'SKU2', 'SKU3', 'SKU4', 'SKU5'], 90),
    'picks': np.random.randint(10, 200, 90)
})

velocity_trends = optimizer.calculate_velocity_trend(historical_data)
print("Velocity Trends:")
print(velocity_trends)

current_slotting = {
    'SKU1': 'Golden Zone',
    'SKU2': 'Forward Pick',
    'SKU3': 'Reserve',
    'SKU4': 'C_Zone',
    'SKU5': 'Forward Pick'
}

recommendations = optimizer.recommend_reslotting(current_slotting, velocity_trends)
print("\nReslotting Recommendations:")
print(recommendations)
```

### Forward Pick Location Sizing

```python
def calculate_forward_pick_size(sku_data, replenishment_frequency='daily'):
    """
    Determine optimal forward pick location size for each SKU

    Balance between:
    - Minimizing forward pick space (expensive)
    - Minimizing replenishment trips (labor cost)

    Parameters:
    -----------
    sku_data : DataFrame with columns
        - sku_id
        - daily_picks (average)
        - units_per_pick
        - cube_per_unit
        - replenishment_cost ($ per trip)

    Returns:
    --------
    Recommended forward pick capacity for each SKU
    """

    df = sku_data.copy()

    # Calculate daily cube picked
    df['daily_cube_picked'] = (df['daily_picks'] *
                                df['units_per_pick'] *
                                df['cube_per_unit'])

    # Determine replenishment period
    replen_days = {
        'daily': 1,
        'every_2_days': 2,
        'weekly': 7
    }
    days = replen_days.get(replenishment_frequency, 1)

    # Forward pick size = days of inventory
    df['forward_pick_cube'] = df['daily_cube_picked'] * days * 1.2  # 20% buffer

    # Round up to standard bin sizes
    standard_sizes = [1, 2, 4, 8, 16, 32]  # cubic feet

    def round_to_standard(size):
        for std_size in standard_sizes:
            if size <= std_size:
                return std_size
        return standard_sizes[-1]

    df['recommended_bin_size'] = df['forward_pick_cube'].apply(round_to_standard)

    # Calculate annual replenishment trips
    df['annual_replen_trips'] = (365 / days) * (df['recommended_bin_size'] > 0)
    df['annual_replen_cost'] = df['annual_replen_trips'] * df['replenishment_cost']

    # Calculate space cost (assuming $10/sq ft/year, 8 ft ceiling)
    space_cost_per_cuft = 10 / 8
    df['annual_space_cost'] = df['recommended_bin_size'] * space_cost_per_cuft

    df['total_annual_cost'] = df['annual_replen_cost'] + df['annual_space_cost']

    return df[[
        'sku_id', 'daily_picks', 'daily_cube_picked',
        'forward_pick_cube', 'recommended_bin_size',
        'annual_replen_trips', 'total_annual_cost'
    ]]


# Example
sku_data = pd.DataFrame({
    'sku_id': [f'SKU{i}' for i in range(1, 11)],
    'daily_picks': np.random.randint(5, 100, 10),
    'units_per_pick': np.random.uniform(1, 3, 10),
    'cube_per_unit': np.random.uniform(0.1, 2, 10),
    'replenishment_cost': np.full(10, 5.0)  # $5 per replenishment
})

forward_pick_sizing = calculate_forward_pick_size(sku_data, 'every_2_days')
print("Forward Pick Location Sizing:")
print(forward_pick_sizing)
```

---

## Tools & Libraries

### Slotting Software

**Commercial Solutions:**
- **Manhattan WMS**: Advanced slotting module
- **Blue Yonder (JDA) WMS**: AI-driven slotting
- **SAP EWM**: Extended warehouse management slotting
- **HighJump WMS**: Task-based slotting optimization
- **Körber Supply Chain**: Dynamic slotting
- **Infor WMS**: Velocity-based slotting

**Specialized Slotting Tools:**
- **EasySlot**: Standalone slotting optimizer
- **SlotSmart**: Cloud-based slotting
- **Warehousing Efficiency Solutions**: Slotting consulting + software

### Python Libraries

```python
# Optimization
from pulp import *  # Linear programming
from scipy.optimize import linear_sum_assignment  # Hungarian algorithm
from ortools.linear_solver import pywraplp  # Google OR-Tools

# Data Analysis
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans  # Clustering for product affinity
from scipy.spatial.distance import cdist  # Distance calculations

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # Interactive warehouse heatmaps
```

---

## Common Challenges & Solutions

### Challenge: Seasonal Demand Shifts

**Problem:**
- Summer vs. winter products have different velocities
- Holiday season drastically changes pick patterns
- Back-to-school surge

**Solutions:**
- Implement seasonal slotting profiles (3-4 per year)
- Use rolling 30-day velocity for classification
- Reserve flex zones for seasonal items
- Pre-slot before season starts (proactive)
- Use forward pick overflow areas
- Monitor velocity weekly during transitions

### Challenge: Product Proliferation

**Problem:**
- Too many SKUs for available forward pick slots
- New SKUs constantly added
- Long tail of slow movers

**Solutions:**
- Stricter ABC cutoffs (only top 15-20% in forward pick)
- Implement each-pick for C items from reserve
- Consolidate similar SKUs
- Phase out slow movers
- Use dynamic slotting (continuous reoptimization)
- Multi-SKU per location for small items

### Challenge: Physical Constraints

**Problem:**
- Weight limits on upper shelves
- Incompatible products (hazmat, temperature)
- Oversized items don't fit standard slots

**Solutions:**
- Add weight constraints to optimization model
- Pre-assign zones by product type
- Dedicated bulk pick areas
- Floor stacking for heavy/large items
- Use equipment-specific zones
- Multi-deep pallet racking for reserves

### Challenge: Replenishment Disruption

**Problem:**
- Replenishment congestion during pick waves
- Forklift traffic interferes with pickers
- Running out of forward pick inventory

**Solutions:**
- Schedule replenishment between pick waves
- Use separate replenishment aisles
- Implement min/max replenishment triggers
- Right-size forward pick locations
- Two-deep forward pick (A/B positions)
- Automated replenishment (AS/RS, shuttles)

### Challenge: Resistance to Change

**Problem:**
- Pickers resist new slotting
- Muscle memory disrupted
- Short-term productivity drop

**Solutions:**
- Implement gradually (zone by zone)
- Communicate benefits clearly
- Provide updated pick face maps
- Allow 2-week learning curve
- Use voice/RF directed picking (tells location)
- Track and celebrate improvements
- Involve experienced pickers in design

### Challenge: Data Quality

**Problem:**
- Inaccurate pick history
- Missing product dimensions
- Unknown product velocity for new items

**Solutions:**
- Clean historical data (remove outliers, returns)
- Physical audit of product dimensions
- Cube scan on receiving
- Proxy velocity from similar products
- Use category averages for new SKUs
- Start with conservative slotting, adjust after 30 days

---

## Output Format

### Slotting Optimization Report

**Executive Summary:**
- Current picking efficiency: 120 lines/hour
- Projected improvement: 145 lines/hour (+21%)
- Total SKUs analyzed: 2,450
- SKUs requiring relocation: 347 (14%)
- Estimated implementation time: 3 weeks
- ROI: 6 months

**ABC Analysis Results:**

| Category | # SKUs | % of SKUs | % of Picks | Avg Pick/Month | Zone Assignment |
|----------|--------|-----------|------------|----------------|-----------------|
| A | 245 | 10% | 75% | 850 | Golden Zone |
| B | 612 | 25% | 20% | 180 | Forward Pick |
| C | 1,593 | 65% | 5% | 12 | Reserve Storage |

**Top 25 SKUs - Golden Zone Placement:**

| SKU | Description | Picks/Month | COI | Current Loc | Optimal Loc | Travel Savings |
|-----|-------------|-------------|-----|-------------|-------------|----------------|
| SKU1234 | Widget A | 1,245 | 0.05 | C-15-3 | A-01-2 | 3,850 ft/mo |
| SKU2345 | Gadget B | 1,123 | 0.08 | B-08-1 | A-01-3 | 3,200 ft/mo |
| ... | ... | ... | ... | ... | ... | ... |

**Product Affinity Clusters:**

```
Cluster 1 (Office Supplies): 45 SKUs
  - Frequently ordered together
  - Recommend: Aisle A1-A2

Cluster 2 (Electronics): 32 SKUs
  - High correlation in order patterns
  - Recommend: Aisle B1-B2

...
```

**Implementation Plan:**

*Phase 1 - Week 1:* Golden Zone (A items)
- Move top 50 SKUs to optimal locations
- Expected: 50% of total benefit
- Minimal disruption

*Phase 2 - Week 2:* Forward Pick (B items)
- Optimize 200 SKU locations
- Expected: 30% additional benefit

*Phase 3 - Week 3:* Reserve Storage (C items)
- Consolidate and organize
- Expected: 20% additional benefit

**Expected Benefits:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| Avg Pick Travel (ft) | 2,850 | 2,100 | -26% |
| Picks per Hour | 120 | 145 | +21% |
| Daily Labor Hours | 180 | 150 | -17% |
| Annual Labor Cost | $540K | $450K | -$90K |
| Forward Pick Utilization | 68% | 89% | +21 pts |

**Maintenance Plan:**
- Weekly velocity monitoring
- Monthly ABC reclassification
- Quarterly full slotting review
- Seasonal profile changes (4x/year)
- Continuous improvement (1% moves/week)

---

## Questions to Ask

If you need more context:
1. How many SKUs and storage locations do you have?
2. What's your current pick efficiency (lines/hour)?
3. Do you have forward pick and reserve zones?
4. How often do you currently re-slot?
5. What WMS or slotting software do you use?
6. Are there seasonal demand patterns?
7. What are physical constraints (weight, temperature, hazmat)?
8. How is replenishment currently scheduled?

---

## Related Skills

- **picker-routing-optimization**: For optimizing pick path given slotting
- **warehouse-design**: For overall layout and zone design
- **order-batching-optimization**: For batching orders to pick together
- **wave-planning-optimization**: For planning pick waves
- **task-assignment-problem**: For assigning pickers to zones
- **inventory-optimization**: For forward pick inventory levels
- **demand-forecasting**: For predicting future velocity changes
- **abc-analysis**: For product classification
