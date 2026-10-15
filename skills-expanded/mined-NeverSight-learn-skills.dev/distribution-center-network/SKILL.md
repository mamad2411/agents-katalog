---
name: distribution-center-network
description: When the user wants to design distribution center networks, optimize DC placement and flows, or configure multi-echelon distribution systems. Also use when the user mentions "DC network design," "distribution network optimization," "multi-echelon distribution," "regional DC placement," "distribution strategy," "fulfillment network design," or "supply chain network configuration." For warehouse location, see warehouse-location-optimization. For general facility location, see facility-location-problem.
---

# Distribution Center Network Design

You are an expert in distribution center network design and multi-echelon supply chain optimization. Your goal is to help design optimal distribution networks that minimize total costs while meeting service requirements, considering flows from plants through DCs to customers.

## Initial Assessment

Before designing DC networks, understand:

1. **Network Structure**
   - Current network configuration?
   - Single-echelon (DCs → customers only)?
   - Multi-echelon (plants → DCs → customers)?
   - Direct shipments allowed? (plants → customers)
   - Cross-docking operations?

2. **Facility Tiers**
   - Manufacturing plants/sources?
   - Regional distribution centers (RDCs)?
   - Local distribution centers (LDCs)?
   - Forward stocking locations (FSLs)?
   - Customer locations?

3. **Product Characteristics**
   - Product variety (SKUs)?
   - Product families or categories?
   - Storage requirements (ambient, refrigerated, hazmat)?
   - Value density (value per volume/weight)?
   - Shelf life and perishability?

4. **Flow Patterns**
   - Where do products originate? (domestic plants, imports, suppliers)
   - Where is demand? (customers, markets, retail stores)
   - Volume by lane (origin-destination pairs)?
   - Seasonal patterns?
   - Growth projections?

5. **Cost Structure**
   - Plant/source costs (production, handling)?
   - DC fixed costs (lease, capital, setup)?
   - DC operating costs (handling, labor, utilities)?
   - Transportation costs (inbound, inter-DC, outbound)?
   - Inventory costs (working inventory, safety stock)?
   - Service penalty costs (late delivery, lost sales)?

---

## Distribution Network Design Framework

### Network Configuration Options

**1. Direct Shipment (0-Echelon)**
```
Plants/Sources → Customers
```
- **Pros**: No intermediate handling, lowest transit time
- **Cons**: High transportation costs for small shipments
- **Best for**: High-value, time-sensitive, large orders

**2. Single-Echelon (1-Echelon)**
```
Plants/Sources → Distribution Centers → Customers
```
- **Pros**: Consolidation benefits, economies of scale
- **Cons**: Additional handling, inventory at DCs
- **Best for**: Most B2B and retail distribution

**3. Two-Echelon (2-Echelon)**
```
Plants → Regional DCs → Local DCs → Customers
```
- **Pros**: Better market coverage, faster delivery
- **Cons**: More complex, higher inventory, more facilities
- **Best for**: Large geographic areas, high service requirements

**4. Hybrid Network**
```
Plants ─→ Regional DCs ─→ Customers
     └─→ Direct ────────┘
```
- **Pros**: Flexibility, optimize by product/customer
- **Cons**: Complex planning and execution
- **Best for**: Differentiated service strategies

### Key Design Decisions

**Strategic (Long-term):**
- Number of echelons
- Number and location of DCs
- DC sizes and capacities
- Technology and automation levels
- Ownership (own vs. outsource/3PL)

**Tactical (Medium-term):**
- Product-DC assignments
- Customer-DC assignments
- Inventory positioning
- Transportation modes
- Seasonality strategies

**Operational (Short-term):**
- Order fulfillment assignments
- Replenishment decisions
- Vehicle routing
- Load consolidation

---

## Mathematical Formulations

### Multi-Echelon DC Network Design Model

**Sets:**
- P: Plants/sources
- D: Potential DC locations
- C: Customers
- K: Products

**Parameters:**
- f_d: Fixed cost to open DC d
- Q_d: Capacity of DC d
- c_{pd}: Unit cost from plant p to DC d
- c_{dc}: Unit cost from DC d to customer c
- c_{pc}: Unit cost from plant p directly to customer c (if allowed)
- d_{ck}: Demand of customer c for product k
- α_k: Unit inventory cost for product k at DC
- s_{pk}: Supply/production capacity of plant p for product k

**Decision Variables:**
- y_d ∈ {0,1}: 1 if DC d is opened
- x_{pdk}: Flow of product k from plant p to DC d
- z_{dck}: Flow of product k from DC d to customer c
- w_{pck}: Flow of product k from plant p directly to customer c (if direct shipping allowed)

**Objective Function:**
```
Minimize:
  DC fixed costs:
    Σ_d f_d × y_d

  + Inbound transportation (plant → DC):
    Σ_p Σ_d Σ_k c_{pd} × x_{pdk}

  + Outbound transportation (DC → customer):
    Σ_d Σ_c Σ_k c_{dc} × z_{dck}

  + Direct shipment costs (if allowed):
    Σ_p Σ_c Σ_k c_{pc} × w_{pck}

  + DC inventory costs:
    Σ_d Σ_k α_k × (Σ_c z_{dck})
```

**Constraints:**
```
1. Demand satisfaction:
   Σ_d z_{dck} + Σ_p w_{pck} = d_{ck},  ∀c ∈ C, ∀k ∈ K

2. DC capacity:
   Σ_c Σ_k z_{dck} ≤ Q_d × y_d,  ∀d ∈ D

3. Flow balance at DCs:
   Σ_p x_{pdk} = Σ_c z_{dck},  ∀d ∈ D, ∀k ∈ K

4. Plant capacity:
   Σ_d x_{pdk} + Σ_c w_{pck} ≤ s_{pk},  ∀p ∈ P, ∀k ∈ K

5. Serve only from open DCs:
   z_{dck} ≤ M × y_d,  ∀d ∈ D, ∀c ∈ C, ∀k ∈ K
   where M is a large constant (customer demand sum)

6. Non-negativity and binary:
   y_d ∈ {0,1},  ∀d ∈ D
   x_{pdk}, z_{dck}, w_{pck} ≥ 0
```

### Service-Level Constrained Model

**Additional Parameters:**
- T_c: Maximum acceptable delivery time for customer c
- t_{dc}: Delivery time from DC d to customer c
- SL: Minimum service level (e.g., 95% of demand met within time)

**Service Constraints:**
```
1. Each customer must be within service time of at least one DC:
   Σ_{d: t_{dc} ≤ T_c} y_d ≥ 1,  ∀c ∈ C

2. Or aggregate service level:
   Σ_c Σ_{d: t_{dc} ≤ T_c} z_{dck} ≥ SL × Σ_c d_{ck},  ∀k ∈ K
```

---

## Solution Methods

### 1. Multi-Echelon MIP Model

```python
from pulp import *
import numpy as np
import pandas as pd

def solve_dc_network_design(plants, dcs, customers, products,
                           dc_costs, capacities, inbound_costs,
                           outbound_costs, demands,
                           plant_capacities=None, allow_direct=False):
    """
    Solve multi-echelon DC network design problem

    Args:
        plants: list of plant IDs
        dcs: list of potential DC IDs
        customers: list of customer IDs
        products: list of product IDs
        dc_costs: dict {dc_id: fixed_cost}
        capacities: dict {dc_id: capacity}
        inbound_costs: dict {(plant, dc, product): cost}
        outbound_costs: dict {(dc, customer, product): cost}
        demands: dict {(customer, product): demand}
        plant_capacities: optional dict {(plant, product): capacity}
        allow_direct: allow direct plant-to-customer shipments

    Returns:
        optimal network design solution
    """

    # Create problem
    prob = LpProblem("DC_Network_Design", LpMinimize)

    # Decision variables
    # y[d] = 1 if DC d is opened
    y = LpVariable.dicts("DC", dcs, cat='Binary')

    # x[p,d,k] = flow from plant p to DC d for product k
    x = {}
    for p in plants:
        for d in dcs:
            for k in products:
                x[p,d,k] = LpVariable(f"inbound_{p}_{d}_{k}",
                                     lowBound=0, cat='Continuous')

    # z[d,c,k] = flow from DC d to customer c for product k
    z = {}
    for d in dcs:
        for c in customers:
            for k in products:
                z[d,c,k] = LpVariable(f"outbound_{d}_{c}_{k}",
                                     lowBound=0, cat='Continuous')

    # w[p,c,k] = direct flow from plant p to customer c (if allowed)
    w = {}
    if allow_direct:
        for p in plants:
            for c in customers:
                for k in products:
                    w[p,c,k] = LpVariable(f"direct_{p}_{c}_{k}",
                                         lowBound=0, cat='Continuous')

    # Objective: Minimize total cost
    # DC fixed costs
    fixed_cost_expr = lpSum([dc_costs[d] * y[d] for d in dcs])

    # Inbound transportation costs
    inbound_expr = lpSum([
        inbound_costs.get((p,d,k), 0) * x[p,d,k]
        for p in plants for d in dcs for k in products
    ])

    # Outbound transportation costs
    outbound_expr = lpSum([
        outbound_costs.get((d,c,k), 0) * z[d,c,k]
        for d in dcs for c in customers for k in products
    ])

    prob += fixed_cost_expr + inbound_expr + outbound_expr, "Total_Cost"

    # Constraints

    # 1. Demand satisfaction
    for c in customers:
        for k in products:
            if (c, k) in demands:
                if allow_direct:
                    prob += (
                        lpSum([z[d,c,k] for d in dcs]) +
                        lpSum([w[p,c,k] for p in plants]) ==
                        demands[c,k],
                        f"Demand_{c}_{k}"
                    )
                else:
                    prob += (
                        lpSum([z[d,c,k] for d in dcs]) == demands[c,k],
                        f"Demand_{c}_{k}"
                    )

    # 2. DC capacity constraints
    for d in dcs:
        prob += (
            lpSum([z[d,c,k]
                   for c in customers for k in products]) <=
            capacities[d] * y[d],
            f"Capacity_DC_{d}"
        )

    # 3. Flow balance at DCs
    for d in dcs:
        for k in products:
            prob += (
                lpSum([x[p,d,k] for p in plants]) ==
                lpSum([z[d,c,k] for c in customers]),
                f"Flow_Balance_{d}_{k}"
            )

    # 4. Plant capacity constraints (if specified)
    if plant_capacities:
        for p in plants:
            for k in products:
                if (p, k) in plant_capacities:
                    if allow_direct:
                        prob += (
                            lpSum([x[p,d,k] for d in dcs]) +
                            lpSum([w[p,c,k] for c in customers]) <=
                            plant_capacities[p,k],
                            f"Plant_Capacity_{p}_{k}"
                        )
                    else:
                        prob += (
                            lpSum([x[p,d,k] for d in dcs]) <=
                            plant_capacities[p,k],
                            f"Plant_Capacity_{p}_{k}"
                        )

    # 5. Serve only from open DCs (big-M constraint)
    for d in dcs:
        for c in customers:
            for k in products:
                if (c, k) in demands:
                    M = demands[c,k]  # Big-M value
                    prob += (
                        z[d,c,k] <= M * y[d],
                        f"Open_DC_{d}_{c}_{k}"
                    )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=900))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        open_dcs = [d for d in dcs if y[d].varValue > 0.5]

        # Extract flows
        inbound_flows = {}
        for p in plants:
            for d in dcs:
                for k in products:
                    if x[p,d,k].varValue > 0.01:
                        inbound_flows[p,d,k] = x[p,d,k].varValue

        outbound_flows = {}
        for d in dcs:
            for c in customers:
                for k in products:
                    if z[d,c,k].varValue > 0.01:
                        outbound_flows[d,c,k] = z[d,c,k].varValue

        # Calculate DC utilization
        dc_utilization = {}
        for d in open_dcs:
            total_flow = sum(z[d,c,k].varValue
                           for c in customers for k in products)
            dc_utilization[d] = (total_flow / capacities[d]) * 100

        # Cost breakdown
        total_fixed = sum(dc_costs[d] for d in open_dcs)
        total_inbound = sum(
            inbound_costs.get((p,d,k), 0) * x[p,d,k].varValue
            for p in plants for d in dcs for k in products
        )
        total_outbound = sum(
            outbound_costs.get((d,c,k), 0) * z[d,c,k].varValue
            for d in dcs for c in customers for k in products
        )

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'fixed_cost': total_fixed,
            'inbound_cost': total_inbound,
            'outbound_cost': total_outbound,
            'open_dcs': open_dcs,
            'num_dcs': len(open_dcs),
            'inbound_flows': inbound_flows,
            'outbound_flows': outbound_flows,
            'dc_utilization': dc_utilization,
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
if __name__ == "__main__":
    # Network data
    plants = ['P1', 'P2', 'P3']
    dcs = ['DC1', 'DC2', 'DC3', 'DC4', 'DC5']
    customers = [f'C{i}' for i in range(1, 21)]  # 20 customers
    products = ['ProductA', 'ProductB', 'ProductC']

    # DC costs and capacities
    dc_costs = {
        'DC1': 500000, 'DC2': 450000, 'DC3': 480000,
        'DC4': 520000, 'DC5': 470000
    }
    capacities = {
        'DC1': 10000, 'DC2': 8000, 'DC3': 9000,
        'DC4': 11000, 'DC5': 8500
    }

    # Generate random costs (simplified)
    np.random.seed(42)

    inbound_costs = {}
    for p in plants:
        for d in dcs:
            for k in products:
                inbound_costs[p,d,k] = np.random.uniform(10, 50)

    outbound_costs = {}
    for d in dcs:
        for c in customers:
            for k in products:
                outbound_costs[d,c,k] = np.random.uniform(5, 30)

    # Customer demands
    demands = {}
    for c in customers:
        for k in products:
            demands[c,k] = np.random.uniform(50, 200)

    # Plant capacities
    plant_capacities = {}
    for p in plants:
        for k in products:
            plant_capacities[p,k] = 5000

    print("="*70)
    print("DISTRIBUTION CENTER NETWORK DESIGN")
    print("="*70)
    print(f"Plants: {len(plants)}")
    print(f"Potential DCs: {len(dcs)}")
    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")
    print(f"Total demand: {sum(demands.values()):,.0f} units")

    # Solve
    result = solve_dc_network_design(
        plants, dcs, customers, products,
        dc_costs, capacities,
        inbound_costs, outbound_costs, demands,
        plant_capacities
    )

    print(f"\n{'='*70}")
    print(f"OPTIMAL SOLUTION")
    print(f"{'='*70}")
    print(f"Status: {result['status']}")
    print(f"Total Cost: ${result['total_cost']:,.2f}")
    print(f"  Fixed Costs: ${result['fixed_cost']:,.2f} "
          f"({result['fixed_cost']/result['total_cost']*100:.1f}%)")
    print(f"  Inbound Transport: ${result['inbound_cost']:,.2f} "
          f"({result['inbound_cost']/result['total_cost']*100:.1f}%)")
    print(f"  Outbound Transport: ${result['outbound_cost']:,.2f} "
          f"({result['outbound_cost']/result['total_cost']*100:.1f}%)")

    print(f"\nOpen DCs: {result['num_dcs']}")
    for dc in result['open_dcs']:
        print(f"  {dc}: Utilization={result['dc_utilization'][dc]:.1f}%, "
              f"Capacity={capacities[dc]:,.0f}")

    print(f"\nSolve Time: {result['solve_time']:.2f} seconds")

    print(f"\nSample Flows (first 10):")
    count = 0
    for (d, c, k), flow in result['outbound_flows'].items():
        if count >= 10:
            break
        print(f"  {d} → {c} ({k}): {flow:.2f} units")
        count += 1
```

### 2. Network Flow Optimization

```python
def optimize_network_flows(open_dcs, plants, customers, products,
                          inbound_costs, outbound_costs, demands,
                          dc_capacities, plant_capacities):
    """
    Optimize flows through given DC network

    Given fixed DC locations, optimize product flows

    Args:
        open_dcs: list of open DC locations
        plants, customers, products: network nodes
        costs, demands, capacities: network parameters

    Returns:
        optimal flow pattern
    """

    prob = LpProblem("Network_Flow", LpMinimize)

    # Variables: flows only (DCs already decided)
    x = {}  # inbound flows
    for p in plants:
        for d in open_dcs:
            for k in products:
                x[p,d,k] = LpVariable(f"inbound_{p}_{d}_{k}",
                                     lowBound=0, cat='Continuous')

    z = {}  # outbound flows
    for d in open_dcs:
        for c in customers:
            for k in products:
                z[d,c,k] = LpVariable(f"outbound_{d}_{c}_{k}",
                                     lowBound=0, cat='Continuous')

    # Objective: Minimize transportation costs
    prob += (
        lpSum([inbound_costs.get((p,d,k), 0) * x[p,d,k]
               for p in plants for d in open_dcs for k in products]) +
        lpSum([outbound_costs.get((d,c,k), 0) * z[d,c,k]
               for d in open_dcs for c in customers for k in products]),
        "Total_Transport_Cost"
    )

    # Constraints

    # Demand satisfaction
    for c in customers:
        for k in products:
            if (c, k) in demands:
                prob += (
                    lpSum([z[d,c,k] for d in open_dcs]) == demands[c,k],
                    f"Demand_{c}_{k}"
                )

    # DC capacity
    for d in open_dcs:
        prob += (
            lpSum([z[d,c,k] for c in customers for k in products]) <=
            dc_capacities[d],
            f"DC_Capacity_{d}"
        )

    # Flow balance
    for d in open_dcs:
        for k in products:
            prob += (
                lpSum([x[p,d,k] for p in plants]) ==
                lpSum([z[d,c,k] for c in customers]),
                f"Balance_{d}_{k}"
            )

    # Plant capacity
    for p in plants:
        for k in products:
            if (p, k) in plant_capacities:
                prob += (
                    lpSum([x[p,d,k] for d in open_dcs]) <=
                    plant_capacities[p,k],
                    f"Plant_{p}_{k}"
                )

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        inbound_flows = {
            (p,d,k): x[p,d,k].varValue
            for p in plants for d in open_dcs for k in products
            if x[p,d,k].varValue > 0.01
        }

        outbound_flows = {
            (d,c,k): z[d,c,k].varValue
            for d in open_dcs for c in customers for k in products
            if z[d,c,k].varValue > 0.01
        }

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'inbound_flows': inbound_flows,
            'outbound_flows': outbound_flows
        }

    return {'status': LpStatus[prob.status]}
```

---

## Heuristic Approaches

### 1. Clustering-Based DC Selection

```python
from sklearn.cluster import KMeans

def clustering_based_dc_selection(customer_locations, customer_demands,
                                  potential_dc_locations, num_dcs):
    """
    Use demand-weighted clustering to select DC locations

    Args:
        customer_locations: array of customer coordinates
        customer_demands: customer demand weights
        potential_dc_locations: candidate DC coordinates
        num_dcs: number of DCs to select

    Returns:
        selected DC indices
    """

    # Cluster customers into num_dcs groups
    weights = (customer_demands / customer_demands.min()).astype(int)
    weighted_locations = []

    for i, loc in enumerate(customer_locations):
        weighted_locations.extend([loc] * weights[i])

    weighted_locations = np.array(weighted_locations)

    # K-means clustering
    kmeans = KMeans(n_clusters=num_dcs, random_state=42)
    kmeans.fit(weighted_locations)

    cluster_centers = kmeans.cluster_centers_

    # Match cluster centers to nearest potential DC locations
    selected_dcs = []
    for center in cluster_centers:
        # Find nearest potential DC to cluster center
        distances = [np.linalg.norm(center - dc_loc)
                    for dc_loc in potential_dc_locations]
        nearest_dc = np.argmin(distances)

        if nearest_dc not in selected_dcs:
            selected_dcs.append(nearest_dc)

    # If we have fewer DCs than requested (due to duplicates),
    # add next best options
    while len(selected_dcs) < num_dcs:
        best_dc = None
        best_total_dist = float('inf')

        for dc_idx in range(len(potential_dc_locations)):
            if dc_idx in selected_dcs:
                continue

            # Calculate total distance from this DC to all customers
            total_dist = sum(
                customer_demands[i] *
                np.linalg.norm(potential_dc_locations[dc_idx] - customer_locations[i])
                for i in range(len(customer_locations))
            )

            if total_dist < best_total_dist:
                best_total_dist = total_dist
                best_dc = dc_idx

        if best_dc is not None:
            selected_dcs.append(best_dc)
        else:
            break

    return selected_dcs
```

### 2. Iterative Location-Allocation

```python
def iterative_location_allocation(potential_dcs, customers, demands,
                                 transport_costs, dc_costs, capacities,
                                 num_dcs, max_iterations=50):
    """
    Iterative heuristic: alternate between location and allocation

    Args:
        potential_dcs: list of potential DC locations
        customers: list of customers
        demands: customer demands
        transport_costs: outbound transport costs
        dc_costs: DC fixed costs
        capacities: DC capacities
        num_dcs: number of DCs to open
        max_iterations: maximum iterations

    Returns:
        heuristic solution
    """

    # Initialize: select random DCs
    current_dcs = random.sample(potential_dcs, num_dcs)

    def allocate_customers(dcs):
        """Allocate each customer to nearest DC with capacity"""
        assignments = {}
        remaining_capacity = {d: capacities[d] for d in dcs}

        # Sort customers by total demand (largest first)
        sorted_customers = sorted(customers,
                                key=lambda c: demands[c],
                                reverse=True)

        for c in sorted_customers:
            # Find nearest DC with capacity
            best_dc = None
            min_cost = float('inf')

            for d in dcs:
                if remaining_capacity[d] >= demands[c]:
                    cost = transport_costs.get((d, c), float('inf'))
                    if cost < min_cost:
                        min_cost = cost
                        best_dc = d

            if best_dc:
                assignments[c] = best_dc
                remaining_capacity[best_dc] -= demands[c]
            else:
                # No capacity, assign to nearest anyway (infeasible)
                best_dc = min(dcs, key=lambda d: transport_costs.get((d,c), float('inf')))
                assignments[c] = best_dc

        return assignments

    def calculate_cost(dcs, assignments):
        """Calculate total cost"""
        fixed = sum(dc_costs[d] for d in dcs)
        transport = sum(
            transport_costs.get((assignments[c], c), 0) * demands[c]
            for c in customers if c in assignments
        )
        return fixed + transport

    best_dcs = current_dcs.copy()
    best_assignments = allocate_customers(current_dcs)
    best_cost = calculate_cost(current_dcs, best_assignments)

    for iteration in range(max_iterations):
        # Allocate customers to current DCs
        current_assignments = allocate_customers(current_dcs)

        # Relocate DCs: try swapping each open DC with each closed DC
        improved = False

        for open_dc in current_dcs:
            for closed_dc in potential_dcs:
                if closed_dc in current_dcs:
                    continue

                # Test swap
                test_dcs = [d if d != open_dc else closed_dc
                           for d in current_dcs]

                test_assignments = allocate_customers(test_dcs)
                test_cost = calculate_cost(test_dcs, test_assignments)

                if test_cost < best_cost - 1e-6:
                    best_cost = test_cost
                    best_dcs = test_dcs.copy()
                    best_assignments = test_assignments
                    current_dcs = test_dcs
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

    return {
        'open_dcs': best_dcs,
        'assignments': best_assignments,
        'total_cost': best_cost,
        'method': 'Iterative Location-Allocation'
    }
```

---

## Complete DC Network Solver

```python
class DCNetworkSolver:
    """
    Comprehensive Distribution Center Network Design Solver
    """

    def __init__(self):
        self.plants = None
        self.dcs = None
        self.customers = None
        self.products = None
        self.loaded = False

    def load_problem(self, network_data):
        """
        Load network design problem

        Args:
            network_data: dict with all problem data
                - plants, dcs, customers, products
                - costs, capacities, demands
        """
        self.plants = network_data['plants']
        self.dcs = network_data['dcs']
        self.customers = network_data['customers']
        self.products = network_data.get('products', ['Product1'])

        self.dc_costs = network_data['dc_costs']
        self.capacities = network_data['capacities']
        self.inbound_costs = network_data['inbound_costs']
        self.outbound_costs = network_data['outbound_costs']
        self.demands = network_data['demands']
        self.plant_capacities = network_data.get('plant_capacities')

        self.loaded = True

        print(f"Loaded DC network problem:")
        print(f"  Plants: {len(self.plants)}")
        print(f"  Potential DCs: {len(self.dcs)}")
        print(f"  Customers: {len(self.customers)}")
        print(f"  Products: {len(self.products)}")
        print(f"  Total demand: {sum(self.demands.values()):,.0f}")

    def solve_exact(self, allow_direct=False, time_limit=900):
        """Solve with exact MIP"""
        if not self.loaded:
            raise ValueError("Problem not loaded")

        print("\nSolving with exact MIP...")
        return solve_dc_network_design(
            self.plants, self.dcs, self.customers, self.products,
            self.dc_costs, self.capacities,
            self.inbound_costs, self.outbound_costs,
            self.demands, self.plant_capacities,
            allow_direct
        )

    def solve_heuristic(self, method='clustering', num_dcs=None):
        """Solve with heuristic method"""
        print(f"\nSolving with {method} heuristic...")

        # Methods require different inputs
        # Implementation would depend on available data
        raise NotImplementedError("Heuristic methods need coordinates")

    def analyze_scenarios(self, dc_counts):
        """
        Analyze different numbers of DCs

        Args:
            dc_counts: list of DC counts to test

        Returns:
            comparison of scenarios
        """
        import pandas as pd

        results = []

        for num_dcs in dc_counts:
            print(f"\nAnalyzing scenario with {num_dcs} DCs...")

            # This would require solving with a constraint on number of DCs
            # or using heuristics

            # Placeholder
            results.append({
                'Num_DCs': num_dcs,
                'Total_Cost': None,
                'Fixed_Cost': None,
                'Transport_Cost': None
            })

        return pd.DataFrame(results)

    def visualize_network(self, solution, coordinates=None):
        """Visualize DC network"""
        import matplotlib.pyplot as plt

        if coordinates is None:
            print("Coordinates required for visualization")
            return

        # Visualization code
        # Similar to previous examples
        pass


# Example usage
if __name__ == "__main__":
    # Create sample network data
    network_data = {
        'plants': ['P1', 'P2'],
        'dcs': ['DC1', 'DC2', 'DC3', 'DC4'],
        'customers': [f'C{i}' for i in range(1, 16)],
        'products': ['ProductA', 'ProductB'],
        'dc_costs': {
            'DC1': 400000, 'DC2': 380000,
            'DC3': 420000, 'DC4': 390000
        },
        'capacities': {
            'DC1': 8000, 'DC2': 7000,
            'DC3': 9000, 'DC4': 7500
        },
        'inbound_costs': {},
        'outbound_costs': {},
        'demands': {},
        'plant_capacities': {}
    }

    # Generate costs and demands
    np.random.seed(42)

    for p in network_data['plants']:
        for d in network_data['dcs']:
            for k in network_data['products']:
                network_data['inbound_costs'][p,d,k] = np.random.uniform(15, 40)

    for d in network_data['dcs']:
        for c in network_data['customers']:
            for k in network_data['products']:
                network_data['outbound_costs'][d,c,k] = np.random.uniform(8, 25)

    for c in network_data['customers']:
        for k in network_data['products']:
            network_data['demands'][c,k] = np.random.uniform(30, 150)

    for p in network_data['plants']:
        for k in network_data['products']:
            network_data['plant_capacities'][p,k] = 3000

    # Solve
    solver = DCNetworkSolver()
    solver.load_problem(network_data)

    solution = solver.solve_exact()

    print(f"\n{'='*70}")
    print(f"OPTIMAL NETWORK CONFIGURATION")
    print(f"{'='*70}")
    print(f"Total Cost: ${solution['total_cost']:,.2f}")
    print(f"DCs Opened: {solution['num_dcs']}")
    print(f"DC IDs: {solution['open_dcs']}")
```

---

## Tools & Libraries

### Python Libraries
- **PuLP/Pyomo**: MIP modeling
- **OR-Tools**: Network optimization
- **NetworkX**: Network analysis
- **scikit-learn**: Clustering
- **pandas/numpy**: Data handling

### Commercial Software
- **Llamasoft**: Network design platform
- **SAP IBP**: Integrated planning
- **Blue Yonder**: Supply chain suite
- **AIMMS**: Optimization modeling

---

## Common Challenges & Solutions

### Challenge: Large-Scale Networks
**Solution:** Decomposition, aggregation, heuristics

### Challenge: Multi-Product Complexity
**Solution:** Product aggregation, ABC analysis

### Challenge: Dynamic Demand
**Solution:** Stochastic models, robust optimization

### Challenge: Service Requirements
**Solution:** Service-level constraints, penalty costs

---

## Output Format

**Network Configuration:**
- Total Cost: $X
- Open DCs: Y locations
- Capacity utilization: Z%
- Service level: W%

---

## Questions to Ask

1. Network scope? (regional, national, global)
2. Current vs. greenfield design?
3. Number of plants/sources?
4. Product variety and characteristics?
5. Demand locations and volumes?
6. Service requirements?
7. Cost structure?
8. Planning horizon?

---

## Related Skills

- **facility-location-problem**: General location theory
- **warehouse-location-optimization**: Warehouse specifics
- **hub-location-problem**: Hub networks
- **network-flow-optimization**: Flow optimization
- **inventory-routing-problem**: Integrated inventory-routing
- **multi-echelon-inventory**: Inventory positioning
