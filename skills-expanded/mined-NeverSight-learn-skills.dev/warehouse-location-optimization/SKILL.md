---
name: warehouse-location-optimization
description: When the user wants to optimize warehouse locations, design warehouse networks, or determine optimal warehouse placement for distribution. Also use when the user mentions "warehouse siting," "warehouse network design," "storage facility location," "fulfillment center location," "regional warehouse optimization," "warehouse consolidation," or "distribution warehouse placement." For general facility location, see facility-location-problem. For distribution centers, see distribution-center-network.
---

# Warehouse Location Optimization

You are an expert in warehouse location optimization and distribution network design. Your goal is to help determine optimal warehouse locations and network configurations to minimize total logistics costs while meeting service requirements and capacity constraints.

## Initial Assessment

Before optimizing warehouse locations, understand:

1. **Network Scope**
   - Greenfield (new network) or brownfield (existing facilities)?
   - National, regional, or global network?
   - Single-echelon or multi-echelon distribution?
   - Number of existing vs. potential new warehouses?

2. **Warehouse Characteristics**
   - Warehouse types? (regional, local, fulfillment centers)
   - Capacity constraints? (storage, throughput)
   - Fixed costs (lease, construction, equipment)?
   - Operating costs (labor, utilities, management)?
   - Warehouse sizes (small, medium, large)?

3. **Demand Profile**
   - Customer locations and demands?
   - Demand variability and seasonality?
   - Product types and storage requirements?
   - Service level requirements (delivery time, fill rate)?
   - Order profiles (B2B, B2C, omnichannel)?

4. **Supply Sources**
   - Manufacturing plants or suppliers?
   - Import/export through ports?
   - Cross-docking requirements?
   - Inbound transportation modes?

5. **Cost Components**
   - Warehouse fixed costs (lease, capital)?
   - Operating costs (labor, utilities, management)?
   - Inbound transportation (suppliers → warehouses)?
   - Outbound transportation (warehouses → customers)?
   - Inventory holding costs?
   - Service failure penalties?

---

## Warehouse Location Decision Framework

### Strategic Decisions

**Long-term (3-10 years):**
- Number of warehouses in network
- Warehouse locations (geographic positioning)
- Warehouse sizes and types
- Technology investments
- Network structure design

**Medium-term (1-3 years):**
- Capacity adjustments
- Lease vs. own decisions
- 3PL partnerships
- Seasonal capacity planning

**Short-term (< 1 year):**
- Inventory allocation
- Order fulfillment assignment
- Routing and scheduling

### Key Trade-offs

**Fixed Costs vs. Transportation:**
- More warehouses → Higher fixed costs
- More warehouses → Lower outbound transport (closer to customers)
- Fewer warehouses → Lower fixed costs, higher transport

**Inventory vs. Service:**
- More warehouses → More safety stock needed
- Centralized → Less inventory, potentially slower service
- Decentralized → More inventory, faster service

**Flexibility vs. Efficiency:**
- Many small warehouses → More flexible, higher cost
- Few large warehouses → Economies of scale, less flexible

---

## Mathematical Formulations

### Multi-Product Warehouse Location Model

**Sets:**
- I: Set of potential warehouse locations
- J: Set of customers
- K: Set of products
- S: Set of suppliers/sources

**Parameters:**
- f_i: Fixed cost to open warehouse at location i
- Q_i: Capacity of warehouse i (storage or throughput)
- d_{jk}: Demand of customer j for product k
- c_{ij}: Unit transportation cost from warehouse i to customer j
- c_{si}: Unit inbound cost from supplier s to warehouse i
- h_k: Inventory holding cost for product k
- α: Inventory coefficient (safety stock factor)

**Decision Variables:**
- y_i ∈ {0,1}: 1 if warehouse i is opened
- x_{ijk} ∈ [0,1]: Fraction of customer j's demand for product k served by warehouse i
- z_{sik}: Flow of product k from supplier s to warehouse i

**Objective Function:**
```
Minimize:
  Fixed costs:
    Σ_i f_i × y_i

  + Outbound transportation:
    Σ_i Σ_j Σ_k c_{ij} × d_{jk} × x_{ijk}

  + Inbound transportation:
    Σ_s Σ_i Σ_k c_{si} × z_{sik}

  + Inventory holding:
    α × Σ_i Σ_k h_k × (Σ_j d_{jk} × x_{ijk})
```

**Constraints:**
```
1. Demand satisfaction:
   Σ_i x_{ijk} = 1,  ∀j ∈ J, ∀k ∈ K

2. Warehouse capacity:
   Σ_j Σ_k d_{jk} × x_{ijk} ≤ Q_i × y_i,  ∀i ∈ I

3. Serve only from open warehouses:
   x_{ijk} ≤ y_i,  ∀i ∈ I, ∀j ∈ J, ∀k ∈ K

4. Inbound-outbound flow balance:
   Σ_s z_{sik} = Σ_j d_{jk} × x_{ijk},  ∀i ∈ I, ∀k ∈ K

5. Binary and non-negativity:
   y_i ∈ {0,1},  ∀i ∈ I
   x_{ijk} ≥ 0,  ∀i,j,k
   z_{sik} ≥ 0,  ∀s,i,k
```

### Service-Constrained Warehouse Location

**Additional Parameters:**
- T_j: Maximum acceptable delivery time for customer j
- t_{ij}: Delivery time from warehouse i to customer j

**Service Constraint:**
```
Only serve customer j from warehouse i if delivery time acceptable:
x_{ijk} = 0  if  t_{ij} > T_j
```

Or as constraint:
```
x_{ijk} ≤ y_i × I(t_{ij} ≤ T_j),  ∀i,j,k

where I(condition) = 1 if condition true, 0 otherwise
```

---

## Solution Methods

### 1. MIP Model with PuLP

```python
from pulp import *
import numpy as np
import pandas as pd

def solve_warehouse_location(warehouse_data, customer_data,
                             transport_costs_out, transport_costs_in=None,
                             supplier_locations=None, products=None):
    """
    Solve multi-product warehouse location problem

    Args:
        warehouse_data: DataFrame with columns [warehouse_id, fixed_cost, capacity]
        customer_data: DataFrame with columns [customer_id, demand, lat, lon]
        transport_costs_out: cost matrix [warehouses x customers] or per-distance rate
        transport_costs_in: optional inbound costs
        supplier_locations: optional supplier data
        products: optional product list

    Returns:
        optimal solution
    """

    n_warehouses = len(warehouse_data)
    n_customers = len(customer_data)

    # Create problem
    prob = LpProblem("Warehouse_Location", LpMinimize)

    # Decision variables
    # y[i] = 1 if warehouse i is opened
    y = LpVariable.dicts("warehouse",
                         warehouse_data.index,
                         cat='Binary')

    # x[i,j] = fraction of customer j served by warehouse i
    x = LpVariable.dicts("service",
                         [(i, j) for i in warehouse_data.index
                          for j in customer_data.index],
                         lowBound=0, upBound=1, cat='Continuous')

    # Objective: Minimize total cost
    # Fixed costs
    fixed_cost_expr = lpSum([
        warehouse_data.loc[i, 'fixed_cost'] * y[i]
        for i in warehouse_data.index
    ])

    # Transportation costs
    transport_cost_expr = lpSum([
        transport_costs_out[i][j] * customer_data.loc[j, 'demand'] * x[i,j]
        for i in warehouse_data.index
        for j in customer_data.index
    ])

    prob += fixed_cost_expr + transport_cost_expr, "Total_Cost"

    # Constraints

    # 1. Each customer fully served
    for j in customer_data.index:
        prob += (
            lpSum([x[i,j] for i in warehouse_data.index]) == 1,
            f"Demand_Customer_{j}"
        )

    # 2. Warehouse capacity constraints
    for i in warehouse_data.index:
        prob += (
            lpSum([customer_data.loc[j, 'demand'] * x[i,j]
                   for j in customer_data.index]) <=
            warehouse_data.loc[i, 'capacity'] * y[i],
            f"Capacity_Warehouse_{i}"
        )

    # 3. Serve only from open warehouses
    for i in warehouse_data.index:
        for j in customer_data.index:
            prob += (
                x[i,j] <= y[i],
                f"Open_{i}_{j}"
            )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=600))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        open_warehouses = [i for i in warehouse_data.index
                          if y[i].varValue > 0.5]

        # Customer assignments
        assignments = {}
        for j in customer_data.index:
            assignments[j] = []
            for i in warehouse_data.index:
                if x[i,j].varValue > 0.01:
                    assignments[j].append({
                        'warehouse': i,
                        'fraction': x[i,j].varValue
                    })

        # Calculate warehouse utilization
        utilization = {}
        for i in open_warehouses:
            used_capacity = sum(
                customer_data.loc[j, 'demand'] * x[i,j].varValue
                for j in customer_data.index
            )
            utilization[i] = (used_capacity /
                            warehouse_data.loc[i, 'capacity'] * 100)

        # Cost breakdown
        total_fixed_cost = sum(
            warehouse_data.loc[i, 'fixed_cost']
            for i in open_warehouses
        )

        total_transport_cost = sum(
            transport_costs_out[i][j] *
            customer_data.loc[j, 'demand'] *
            x[i,j].varValue
            for i in warehouse_data.index
            for j in customer_data.index
        )

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'fixed_cost': total_fixed_cost,
            'transport_cost': total_transport_cost,
            'open_warehouses': open_warehouses,
            'num_warehouses': len(open_warehouses),
            'assignments': assignments,
            'utilization': utilization,
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
if __name__ == "__main__":
    import numpy as np
    import pandas as pd

    np.random.seed(42)

    # Warehouse data: 8 potential locations
    warehouse_data = pd.DataFrame({
        'warehouse_id': range(8),
        'fixed_cost': [500000, 450000, 600000, 520000,
                      480000, 550000, 490000, 530000],
        'capacity': [10000, 8000, 12000, 9000, 8500, 11000, 9500, 10500],
        'lat': np.random.uniform(30, 45, 8),
        'lon': np.random.uniform(-120, -70, 8)
    })
    warehouse_data.index = warehouse_data['warehouse_id']

    # Customer data: 30 customers
    customer_data = pd.DataFrame({
        'customer_id': range(30),
        'demand': np.random.uniform(100, 500, 30),
        'lat': np.random.uniform(30, 45, 30),
        'lon': np.random.uniform(-120, -70, 30)
    })
    customer_data.index = customer_data['customer_id']

    # Calculate transportation costs (simplified: Euclidean distance × rate)
    transport_rate = 0.5  # $ per unit per distance unit

    transport_costs_out = np.zeros((len(warehouse_data), len(customer_data)))
    for i in warehouse_data.index:
        for j in customer_data.index:
            distance = np.sqrt(
                (warehouse_data.loc[i, 'lat'] - customer_data.loc[j, 'lat'])**2 +
                (warehouse_data.loc[i, 'lon'] - customer_data.loc[j, 'lon'])**2
            )
            transport_costs_out[i][j] = distance * transport_rate

    print("="*70)
    print("WAREHOUSE LOCATION OPTIMIZATION")
    print("="*70)
    print(f"Potential warehouses: {len(warehouse_data)}")
    print(f"Customers: {len(customer_data)}")
    print(f"Total demand: {customer_data['demand'].sum():,.0f} units")

    # Solve
    result = solve_warehouse_location(warehouse_data, customer_data,
                                     transport_costs_out)

    print(f"\n{'='*70}")
    print(f"SOLUTION")
    print(f"{'='*70}")
    print(f"Status: {result['status']}")
    print(f"Total Cost: ${result['total_cost']:,.2f}")
    print(f"  Fixed Costs: ${result['fixed_cost']:,.2f} "
          f"({result['fixed_cost']/result['total_cost']*100:.1f}%)")
    print(f"  Transport Costs: ${result['transport_cost']:,.2f} "
          f"({result['transport_cost']/result['total_cost']*100:.1f}%)")
    print(f"\nWarehouses Opened: {result['num_warehouses']}")
    print(f"Warehouse IDs: {result['open_warehouses']}")

    print(f"\nWarehouse Utilization:")
    for wh_id in result['open_warehouses']:
        capacity = warehouse_data.loc[wh_id, 'capacity']
        util = result['utilization'][wh_id]
        print(f"  Warehouse {wh_id}: {util:.1f}% (capacity={capacity:,.0f})")

    print(f"\nSolve Time: {result['solve_time']:.2f} seconds")
```

### 2. Gravity Location Model

```python
def gravity_location_model(customer_locations, customer_demands,
                          num_warehouses=None):
    """
    Gravity/Center-of-Gravity model for warehouse location

    Places warehouses at demand-weighted centroids

    Simple but effective heuristic for initial solutions

    Args:
        customer_locations: array of [lat, lon] for each customer
        customer_demands: customer demand weights
        num_warehouses: number of warehouses (if None, finds single location)

    Returns:
        optimal warehouse location(s)
    """
    from sklearn.cluster import KMeans

    customer_locations = np.array(customer_locations)
    customer_demands = np.array(customer_demands)

    if num_warehouses is None or num_warehouses == 1:
        # Single warehouse: weighted centroid
        total_demand = customer_demands.sum()

        center_lat = (customer_locations[:, 0] * customer_demands).sum() / total_demand
        center_lon = (customer_locations[:, 1] * customer_demands).sum() / total_demand

        return np.array([[center_lat, center_lon]])

    else:
        # Multiple warehouses: use weighted K-means clustering
        kmeans = KMeans(n_clusters=num_warehouses, random_state=42)

        # Weight samples by demand (repeat points proportional to demand)
        weights = (customer_demands / customer_demands.min()).astype(int)
        weighted_locations = []

        for i, loc in enumerate(customer_locations):
            weighted_locations.extend([loc] * weights[i])

        weighted_locations = np.array(weighted_locations)

        # Fit clustering
        kmeans.fit(weighted_locations)

        return kmeans.cluster_centers_


# Example usage
customer_locs = np.random.rand(50, 2) * 100  # 50 customers
customer_dems = np.random.uniform(100, 1000, 50)

# Find optimal locations for 3 warehouses
warehouse_locations = gravity_location_model(customer_locs, customer_dems,
                                            num_warehouses=3)

print("Optimal warehouse locations (gravity model):")
for i, loc in enumerate(warehouse_locations):
    print(f"  Warehouse {i+1}: ({loc[0]:.2f}, {loc[1]:.2f})")
```

### 3. Coverage-Based Location

```python
def coverage_based_warehouse_location(customer_locations, service_radius,
                                     potential_warehouses=None):
    """
    Warehouse location with service coverage constraints

    Ensure all customers within service radius of at least one warehouse

    Args:
        customer_locations: customer coordinates
        service_radius: maximum service distance
        potential_warehouses: candidate warehouse locations
                            (if None, use customer locations)

    Returns:
        minimum set of warehouses for full coverage
    """

    if potential_warehouses is None:
        potential_warehouses = customer_locations

    n_warehouses = len(potential_warehouses)
    n_customers = len(customer_locations)

    # Calculate coverage matrix
    # coverage[i][j] = 1 if warehouse i can serve customer j
    coverage = np.zeros((n_warehouses, n_customers))

    for i in range(n_warehouses):
        for j in range(n_customers):
            distance = np.linalg.norm(
                potential_warehouses[i] - customer_locations[j]
            )
            if distance <= service_radius:
                coverage[i][j] = 1

    # Solve set covering problem
    prob = LpProblem("Coverage_Warehouse_Location", LpMinimize)

    # Decision variables: y[i] = 1 if warehouse i is opened
    y = LpVariable.dicts("warehouse", range(n_warehouses), cat='Binary')

    # Objective: Minimize number of warehouses
    prob += lpSum([y[i] for i in range(n_warehouses)]), "Num_Warehouses"

    # Constraints: Each customer covered by at least one warehouse
    for j in range(n_customers):
        prob += (
            lpSum([coverage[i][j] * y[i] for i in range(n_warehouses)]) >= 1,
            f"Coverage_Customer_{j}"
        )

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        open_warehouses = [i for i in range(n_warehouses)
                          if y[i].varValue > 0.5]

        # Determine which warehouse serves each customer
        assignments = {}
        for j in range(n_customers):
            # Assign to nearest warehouse that can serve
            min_distance = float('inf')
            assigned_warehouse = None

            for i in open_warehouses:
                if coverage[i][j] == 1:
                    distance = np.linalg.norm(
                        potential_warehouses[i] - customer_locations[j]
                    )
                    if distance < min_distance:
                        min_distance = distance
                        assigned_warehouse = i

            assignments[j] = assigned_warehouse

        return {
            'status': LpStatus[prob.status],
            'num_warehouses': len(open_warehouses),
            'open_warehouses': open_warehouses,
            'warehouse_locations': [potential_warehouses[i]
                                  for i in open_warehouses],
            'assignments': assignments
        }

    return {'status': LpStatus[prob.status]}


# Example
customer_locs = np.random.rand(40, 2) * 100
potential_wh_locs = np.random.rand(15, 2) * 100
service_radius = 25

result = coverage_based_warehouse_location(customer_locs, service_radius,
                                          potential_wh_locs)

print(f"Minimum warehouses for coverage: {result['num_warehouses']}")
print(f"Warehouse indices: {result['open_warehouses']}")
```

---

## Heuristic Approaches

### 1. Greedy Opening Heuristic

```python
def greedy_warehouse_opening(warehouse_costs, customer_demands,
                            transport_costs, capacities):
    """
    Greedy heuristic: open warehouses one at a time

    Select warehouse that gives maximum cost reduction

    Args:
        warehouse_costs: fixed costs for each warehouse
        customer_demands: customer demands
        transport_costs: matrix [warehouses x customers]
        capacities: warehouse capacities

    Returns:
        heuristic solution
    """
    n_warehouses = len(warehouse_costs)
    n_customers = len(customer_demands)

    open_warehouses = []
    unserved_customers = set(range(n_customers))

    def calculate_total_cost(open_whs, assignments):
        """Calculate total cost for given configuration"""
        fixed = sum(warehouse_costs[i] for i in open_whs)
        transport = sum(
            transport_costs[assignments[j]][j] * customer_demands[j]
            for j in range(n_customers) if j in assignments
        )
        return fixed + transport

    # Iteratively open warehouses
    while unserved_customers:
        best_warehouse = None
        best_cost = float('inf')
        best_assignments = None

        # Try opening each unopened warehouse
        for wh in range(n_warehouses):
            if wh in open_warehouses:
                continue

            test_warehouses = open_warehouses + [wh]

            # Assign customers greedily to nearest warehouse
            test_assignments = {}
            remaining_capacity = {w: capacities[w] for w in test_warehouses}

            # Sort customers by closest distance to this new warehouse
            customer_distances = [
                (transport_costs[wh][j], j) for j in unserved_customers
            ]
            customer_distances.sort()

            for dist, cust in customer_distances:
                # Assign to nearest warehouse with capacity
                assigned = False
                for w in sorted(test_warehouses,
                              key=lambda x: transport_costs[x][cust]):
                    if remaining_capacity[w] >= customer_demands[cust]:
                        test_assignments[cust] = w
                        remaining_capacity[w] -= customer_demands[cust]
                        assigned = True
                        break

                if not assigned:
                    test_assignments[cust] = min(test_warehouses,
                                                key=lambda x: transport_costs[x][cust])

            # Calculate cost
            test_cost = calculate_total_cost(test_warehouses, test_assignments)

            if test_cost < best_cost:
                best_cost = test_cost
                best_warehouse = wh
                best_assignments = test_assignments

        # Open best warehouse
        if best_warehouse is not None:
            open_warehouses.append(best_warehouse)
            unserved_customers = {c for c in unserved_customers
                                if c not in best_assignments}

            # Update assignments for served customers
            if not unserved_customers:
                assignments = best_assignments
                break
        else:
            break

    total_cost = calculate_total_cost(open_warehouses, assignments)

    return {
        'open_warehouses': open_warehouses,
        'assignments': assignments,
        'total_cost': total_cost,
        'method': 'Greedy Opening'
    }
```

### 2. Savings-Based Consolidation

```python
def savings_based_consolidation(warehouse_costs, customer_demands,
                               transport_costs, initial_warehouses=None):
    """
    Savings-based heuristic for warehouse consolidation

    Start with many warehouses, consolidate based on savings

    Args:
        warehouse_costs: fixed costs
        customer_demands: demands
        transport_costs: transport cost matrix
        initial_warehouses: starting warehouse set

    Returns:
        consolidated solution
    """
    n_warehouses = len(warehouse_costs)
    n_customers = len(customer_demands)

    # Start with all warehouses if not specified
    if initial_warehouses is None:
        open_warehouses = set(range(n_warehouses))
    else:
        open_warehouses = set(initial_warehouses)

    def assign_customers(whs):
        """Assign each customer to nearest warehouse"""
        assignments = {}
        for j in range(n_customers):
            nearest = min(whs, key=lambda i: transport_costs[i][j])
            assignments[j] = nearest
        return assignments

    def calculate_cost(whs, assignments):
        """Calculate total cost"""
        fixed = sum(warehouse_costs[i] for i in whs)
        transport = sum(
            transport_costs[assignments[j]][j] * customer_demands[j]
            for j in range(n_customers)
        )
        return fixed + transport

    improved = True
    while improved and len(open_warehouses) > 1:
        improved = False

        current_assignments = assign_customers(open_warehouses)
        current_cost = calculate_cost(open_warehouses, current_assignments)

        # Try closing each warehouse
        best_warehouse_to_close = None
        best_cost_after_closing = current_cost

        for wh in list(open_warehouses):
            # Test closing this warehouse
            test_warehouses = open_warehouses - {wh}
            test_assignments = assign_customers(test_warehouses)
            test_cost = calculate_cost(test_warehouses, test_assignments)

            # Check if closing reduces cost
            if test_cost < best_cost_after_closing:
                best_cost_after_closing = test_cost
                best_warehouse_to_close = wh
                improved = True

        # Close best warehouse if improvement found
        if improved:
            open_warehouses.remove(best_warehouse_to_close)

    final_assignments = assign_customers(open_warehouses)
    final_cost = calculate_cost(open_warehouses, final_assignments)

    return {
        'open_warehouses': list(open_warehouses),
        'assignments': final_assignments,
        'total_cost': final_cost,
        'method': 'Savings-Based Consolidation'
    }
```

---

## Complete Warehouse Location Solver

```python
class WarehouseLocationSolver:
    """
    Comprehensive warehouse location optimization solver
    """

    def __init__(self):
        self.warehouse_data = None
        self.customer_data = None
        self.transport_costs = None
        self.solution = None

    def load_problem(self, warehouse_data, customer_data,
                    transport_costs=None, transport_rate=None):
        """
        Load problem data

        Args:
            warehouse_data: DataFrame with warehouse info
            customer_data: DataFrame with customer info
            transport_costs: cost matrix or None
            transport_rate: if transport_costs None, calculate from rate
        """
        self.warehouse_data = warehouse_data
        self.customer_data = customer_data

        if transport_costs is not None:
            self.transport_costs = transport_costs
        elif transport_rate is not None:
            # Calculate costs from distances
            self.transport_costs = self._calculate_transport_costs(transport_rate)
        else:
            raise ValueError("Must provide transport_costs or transport_rate")

        print(f"Loaded warehouse location problem:")
        print(f"  Potential warehouses: {len(warehouse_data)}")
        print(f"  Customers: {len(customer_data)}")
        print(f"  Total demand: {customer_data['demand'].sum():,.0f}")

    def _calculate_transport_costs(self, rate):
        """Calculate transport costs from coordinates and rate"""
        costs = np.zeros((len(self.warehouse_data), len(self.customer_data)))

        for i in self.warehouse_data.index:
            for j in self.customer_data.index:
                dist = np.sqrt(
                    (self.warehouse_data.loc[i, 'lat'] -
                     self.customer_data.loc[j, 'lat'])**2 +
                    (self.warehouse_data.loc[i, 'lon'] -
                     self.customer_data.loc[j, 'lon'])**2
                )
                costs[i][j] = dist * rate

        return costs

    def solve_exact(self, time_limit=600):
        """Solve with MIP (exact)"""
        print("\nSolving with MIP (exact method)...")
        return solve_warehouse_location(
            self.warehouse_data,
            self.customer_data,
            self.transport_costs
        )

    def solve_heuristic(self, method='greedy'):
        """
        Solve with heuristic

        Args:
            method: 'greedy', 'gravity', 'coverage', 'savings'
        """
        print(f"\nSolving with {method} heuristic...")

        if method == 'greedy':
            return greedy_warehouse_opening(
                self.warehouse_data['fixed_cost'].values,
                self.customer_data['demand'].values,
                self.transport_costs,
                self.warehouse_data['capacity'].values
            )

        elif method == 'gravity':
            customer_locs = self.customer_data[['lat', 'lon']].values
            customer_dems = self.customer_data['demand'].values

            # Estimate number of warehouses from capacity
            total_demand = customer_dems.sum()
            avg_capacity = self.warehouse_data['capacity'].mean()
            num_whs = max(1, int(np.ceil(total_demand / avg_capacity * 1.2)))

            locations = gravity_location_model(customer_locs, customer_dems,
                                             num_warehouses=num_whs)

            # Match to nearest potential warehouses
            open_whs = []
            for loc in locations:
                nearest = None
                min_dist = float('inf')
                for i in self.warehouse_data.index:
                    wh_loc = self.warehouse_data.loc[i, ['lat', 'lon']].values
                    dist = np.linalg.norm(loc - wh_loc)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = i
                open_whs.append(nearest)

            return {'open_warehouses': open_whs, 'method': 'Gravity'}

        else:
            raise ValueError(f"Unknown method: {method}")

    def compare_solutions(self, methods=['greedy', 'savings', 'exact']):
        """Compare multiple solution methods"""
        import pandas as pd
        import time

        results = []

        for method in methods:
            start_time = time.time()

            try:
                if method == 'exact':
                    solution = self.solve_exact()
                else:
                    solution = self.solve_heuristic(method)

                solve_time = time.time() - start_time

                results.append({
                    'Method': method,
                    'Total Cost': solution['total_cost'],
                    'Warehouses': len(solution['open_warehouses']),
                    'Time (s)': f"{solve_time:.2f}"
                })

            except Exception as e:
                print(f"Error with {method}: {e}")

        df = pd.DataFrame(results)

        if len(df) > 0:
            best_cost = df['Total Cost'].min()
            df['Gap %'] = ((df['Total Cost'] - best_cost) / best_cost * 100).round(2)

        return df

    def visualize_network(self, solution, title="Warehouse Network"):
        """Visualize warehouse network"""
        import matplotlib.pyplot as plt

        plt.figure(figsize=(14, 10))

        # Plot customers (blue circles)
        plt.scatter(self.customer_data['lon'],
                   self.customer_data['lat'],
                   c='lightblue', s=50, alpha=0.6,
                   label='Customers')

        # Plot all potential warehouses (gray)
        plt.scatter(self.warehouse_data['lon'],
                   self.warehouse_data['lat'],
                   c='lightgray', s=200, alpha=0.3,
                   marker='s', label='Potential Warehouses')

        # Plot open warehouses (red)
        open_wh_data = self.warehouse_data.loc[solution['open_warehouses']]
        plt.scatter(open_wh_data['lon'],
                   open_wh_data['lat'],
                   c='red', s=300, alpha=0.8,
                   marker='s', label='Open Warehouses',
                   edgecolors='black', linewidths=2)

        # Draw assignments
        if 'assignments' in solution:
            for cust_id, assignment in solution['assignments'].items():
                if isinstance(assignment, list):
                    wh_id = assignment[0]['warehouse']
                else:
                    wh_id = assignment

                cust_loc = self.customer_data.loc[cust_id, ['lon', 'lat']].values
                wh_loc = self.warehouse_data.loc[wh_id, ['lon', 'lat']].values

                plt.plot([cust_loc[0], wh_loc[0]],
                        [cust_loc[1], wh_loc[1]],
                        'k-', alpha=0.1, linewidth=0.5)

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


# Complete example
if __name__ == "__main__":
    print("="*70)
    print("WAREHOUSE LOCATION OPTIMIZATION - COMPLETE EXAMPLE")
    print("="*70)

    np.random.seed(42)

    # Generate problem data
    n_warehouses = 10
    n_customers = 50

    warehouse_df = pd.DataFrame({
        'warehouse_id': range(n_warehouses),
        'fixed_cost': np.random.uniform(400000, 700000, n_warehouses),
        'capacity': np.random.uniform(5000, 15000, n_warehouses),
        'lat': np.random.uniform(30, 45, n_warehouses),
        'lon': np.random.uniform(-120, -70, n_warehouses)
    })
    warehouse_df.index = warehouse_df['warehouse_id']

    customer_df = pd.DataFrame({
        'customer_id': range(n_customers),
        'demand': np.random.uniform(100, 800, n_customers),
        'lat': np.random.uniform(30, 45, n_customers),
        'lon': np.random.uniform(-120, -70, n_customers)
    })
    customer_df.index = customer_df['customer_id']

    # Create solver
    solver = WarehouseLocationSolver()
    solver.load_problem(warehouse_df, customer_df, transport_rate=0.5)

    # Compare solutions
    print("\n" + "="*70)
    print("COMPARING SOLUTION METHODS")
    print("="*70)

    comparison = solver.compare_solutions(['greedy', 'exact'])
    print("\n" + comparison.to_string(index=False))

    # Detailed solution
    print("\n" + "="*70)
    print("DETAILED OPTIMAL SOLUTION")
    print("="*70)

    best_solution = solver.solve_exact()

    print(f"Total Cost: ${best_solution['total_cost']:,.2f}")
    print(f"  Fixed: ${best_solution['fixed_cost']:,.2f} "
          f"({best_solution['fixed_cost']/best_solution['total_cost']*100:.1f}%)")
    print(f"  Transport: ${best_solution['transport_cost']:,.2f} "
          f"({best_solution['transport_cost']/best_solution['total_cost']*100:.1f}%)")

    print(f"\nWarehouses Opened: {best_solution['num_warehouses']}")
    for wh_id in best_solution['open_warehouses']:
        util = best_solution['utilization'][wh_id]
        cap = warehouse_df.loc[wh_id, 'capacity']
        cost = warehouse_df.loc[wh_id, 'fixed_cost']
        print(f"  Warehouse {wh_id}: Util={util:.1f}%, "
              f"Cap={cap:,.0f}, Cost=${cost:,.0f}")

    # Visualize
    solver.visualize_network(best_solution,
                            title="Optimal Warehouse Network")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- **PuLP**: MIP modeling
- **Pyomo**: Advanced optimization
- **OR-Tools**: Google optimization
- **Gurobi/CPLEX**: Commercial solvers

**Data & Analysis:**
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: Clustering, ML

**Geospatial:**
- **geopy**: Distance calculations
- **folium**: Interactive maps
- **geopandas**: Geospatial data

**Visualization:**
- **matplotlib**: Plotting
- **plotly**: Interactive viz
- **seaborn**: Statistical viz

### Commercial Software

- **Llamasoft (Coupa)**: Supply chain network design
- **LLamasoft Design**: Warehouse optimization
- **SAP IBP**: Integrated business planning
- **Blue Yonder**: Supply chain platform
- **o9 Solutions**: Planning platform

---

## Common Challenges & Solutions

### Challenge: Multi-Echelon Networks

**Problem:**
- Plants → Regional DCs → Local warehouses → Customers
- Complex flow patterns
- Multiple decisions layers

**Solutions:**
- Hierarchical decomposition
- Multi-stage optimization
- Simultaneous optimization if tractable
- Iterative refinement

### Challenge: Seasonal Demand

**Problem:**
- Demand varies significantly by season
- Warehouse decisions long-term
- Peak capacity requirements

**Solutions:**
- Model peak season explicitly
- Include flexibility/surge capacity
- Temporary warehouses for peak
- Third-party logistics (3PL) options
- Multi-period models

### Challenge: Inventory Considerations

**Problem:**
- Warehouse location affects inventory levels
- More warehouses → more safety stock
- Trade-off not captured in simple models

**Solutions:**
- Include inventory costs in model
- Square root law for safety stock
- Risk pooling benefits of centralization
- Multi-echelon inventory optimization

### Challenge: Real-World Constraints

**Problem:**
- Zoning regulations
- Labor availability
- Real estate availability
- Infrastructure (ports, rails, highways)
- Tax incentives

**Solutions:**
- Include as constraints in model
- Scenario analysis
- Post-optimization feasibility checks
- Collaboration with site selection experts

---

## Output Format

### Warehouse Location Solution Report

**Problem Instance:**
- Candidate Warehouses: 15
- Customers: 100
- Total Annual Demand: 125,000 units
- Planning Horizon: 5 years

**Optimal Network Configuration:**

| Metric | Value |
|--------|-------|
| Total Annual Cost | $8,247,500 |
| Fixed Costs | $2,450,000 (29.7%) |
| Outbound Transport | $4,823,000 (58.5%) |
| Inbound Transport | $974,500 (11.8%) |
| Warehouses Opened | 4 |
| Average Utilization | 78.3% |
| Service Coverage | 100% |

**Open Warehouses:**

| WH ID | Location | Fixed Cost | Capacity | Utilization | Customers Served |
|-------|----------|------------|----------|-------------|------------------|
| 3 | Dallas, TX | $650,000 | 35,000 | 82.1% | 28 |
| 7 | Atlanta, GA | $580,000 | 30,000 | 76.8% | 24 |
| 11 | Los Angeles, CA | $720,000 | 40,000 | 81.4% | 31 |
| 14 | Chicago, IL | $500,000 | 25,000 | 72.9% | 17 |

**Network Statistics:**
- Average distance to customer: 287 miles
- Maximum distance to customer: 612 miles
- Average outbound transport cost per unit: $38.58
- Capacity buffer: 21.7% (for growth/seasonality)

---

## Questions to Ask

1. Is this a greenfield (new network) or brownfield (existing) analysis?
2. How many potential warehouse locations?
3. How many customers? What are their locations and demands?
4. What are the warehouse fixed costs (lease/construction)?
5. Operating costs (labor, utilities, management)?
6. Warehouse capacities or capacity options?
7. What are transportation costs? (rates or distance-based)
8. Service requirements? (delivery time, coverage distance)
9. Are there existing facilities that must remain?
10. Planning horizon? (1 year, 3 years, 10 years)
11. Demand variability and growth projections?
12. Multi-echelon network? (plants, DCs, local warehouses)
13. Product characteristics? (value, weight, storage requirements)
14. Inventory holding costs important?

---

## Related Skills

- **facility-location-problem**: General facility location theory
- **distribution-center-network**: DC-specific network design
- **network-design**: End-to-end supply chain network
- **hub-location-problem**: Hub-and-spoke networks
- **set-covering-problem**: Coverage-based location
- **inventory-optimization**: Inventory-location trade-offs
- **network-flow-optimization**: Flow allocation in networks
- **vehicle-routing-problem**: Last-mile delivery from warehouses
- **multi-echelon-inventory**: Inventory across network levels
