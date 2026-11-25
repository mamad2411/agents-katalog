---
name: inventory-routing-problem
description: When the user wants to jointly optimize inventory and routing decisions, implement vendor-managed inventory (VMI) systems, or coordinate replenishment and delivery logistics. Also use when the user mentions "IRP," "inventory routing," "vendor-managed inventory," "VMI optimization," "integrated inventory and transportation," "delivery scheduling with inventory," "maritime inventory routing," "petrol station replenishment," or "coordinated inventory-distribution." For pure routing, see vehicle-routing-problem or route-optimization. For pure inventory, see inventory-optimization or multi-echelon-inventory.
---

# Inventory Routing Problem (IRP)

You are an expert in Inventory Routing Problems (IRP) and integrated inventory-distribution optimization. Your goal is to help jointly optimize inventory management and vehicle routing decisions to minimize total system costs including inventory holding, routing, and potential stockouts.

## Initial Assessment

Before solving inventory routing problems, understand:

1. **System Structure**
   - Vendor-managed inventory (VMI) or retailer-managed?
   - Number of customers/retailers?
   - Single depot or multiple?
   - Planning horizon (days, weeks)?
   - Frequency of deliveries?

2. **Inventory Characteristics**
   - Storage capacity at each location?
   - Current inventory levels?
   - Consumption/demand rates (deterministic or stochastic)?
   - Minimum inventory levels (safety stock)?
   - Maximum inventory levels (tank capacity, shelf space)?
   - Product shelf life or perishability?

3. **Routing Constraints**
   - Vehicle capacity (weight, volume)?
   - Number of vehicles available?
   - Maximum route duration or distance?
   - Time windows for deliveries?
   - Driver shift constraints?
   - Accessibility restrictions?

4. **Cost Structure**
   - Inventory holding costs at depot and customers?
   - Transportation costs (per mile, per vehicle, per route)?
   - Fixed cost per vehicle used?
   - Penalty costs for stockouts?
   - Setup/delivery fee per customer visit?

5. **Service Requirements**
   - Must prevent stockouts?
   - Minimum service frequency per customer?
   - Priority customers?
   - Contractual delivery requirements?

---

## IRP Fundamentals

### Problem Definition

The Inventory Routing Problem (IRP) integrates two classical problems:
1. **Inventory Management:** When and how much to replenish each customer
2. **Vehicle Routing:** How to efficiently route vehicles to serve customers

**Key Trade-off:**
- More frequent small deliveries → Higher routing costs, lower inventory
- Less frequent large deliveries → Lower routing costs, higher inventory

### Problem Variants

**1. Single-Period IRP**
- One-time routing and delivery decision
- Given current inventory levels
- Minimize routing cost subject to inventory constraints

**2. Multi-Period IRP**
- Plan deliveries over time horizon (T periods)
- Account for inventory dynamics
- Most realistic and most complex

**3. Deterministic vs. Stochastic IRP**
- Deterministic: Known consumption rates
- Stochastic: Uncertain demand, requires safety stock

**4. Maritime IRP (MIRP)**
- Ships instead of trucks
- Larger capacities, longer travel times
- Often used for petrol/chemical distribution

---

## Python Implementation: IRP Models

### Single-Period IRP with MIP

```python
import numpy as np
import pandas as pd
from pulp import *
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

class SinglePeriodIRP:
    """
    Single-Period Inventory Routing Problem

    Given:
    - Current inventory at each customer
    - Consumption rates
    - Vehicle capacity
    - Distance matrix

    Decide:
    - Which customers to visit
    - How much to deliver to each
    - Vehicle routes
    """

    def __init__(self, num_customers: int, customer_locations: np.ndarray,
                 depot_location: np.ndarray, current_inventory: np.ndarray,
                 consumption_rates: np.ndarray, max_inventory: np.ndarray,
                 vehicle_capacity: float, num_vehicles: int,
                 holding_cost: float = 1.0, routing_cost_per_km: float = 1.0):
        """
        Parameters:
        -----------
        num_customers : int
            Number of customer locations
        customer_locations : ndarray
            (n x 2) array of customer coordinates
        depot_location : ndarray
            (2,) depot coordinates
        current_inventory : ndarray
            Current inventory level at each customer
        consumption_rates : ndarray
            Daily consumption at each customer
        max_inventory : ndarray
            Maximum storage capacity at each customer
        vehicle_capacity : float
            Vehicle capacity (units)
        num_vehicles : int
            Number of vehicles available
        holding_cost : float
            Inventory holding cost per unit per day
        routing_cost_per_km : float
            Cost per kilometer traveled
        """
        self.n = num_customers
        self.customer_locations = customer_locations
        self.depot = depot_location
        self.I = current_inventory
        self.d = consumption_rates
        self.C = max_inventory
        self.Q = vehicle_capacity
        self.K = num_vehicles
        self.h = holding_cost
        self.c_routing = routing_cost_per_km

        # Calculate distance matrix
        all_locations = np.vstack([depot_location, customer_locations])
        self.dist_matrix = cdist(all_locations, all_locations, metric='euclidean')

    def solve_mip(self, time_until_next_delivery: int = 1) -> Dict:
        """
        Solve single-period IRP using Mixed-Integer Programming

        Decision variables:
        - x[i,j,k]: binary, 1 if vehicle k travels from i to j
        - y[i,k]: binary, 1 if customer i is visited by vehicle k
        - q[i]: quantity delivered to customer i
        """

        # Create problem
        prob = LpProblem("Single_Period_IRP", LpMinimize)

        # Nodes: 0 = depot, 1..n = customers
        nodes = range(self.n + 1)
        customers = range(1, self.n + 1)
        vehicles = range(self.K)

        # Decision variables
        # Routing variables
        x = {}
        for i in nodes:
            for j in nodes:
                for k in vehicles:
                    if i != j:
                        x[i, j, k] = LpVariable(f"x_{i}_{j}_{k}", cat='Binary')

        # Visit variables
        y = {}
        for i in customers:
            for k in vehicles:
                y[i, k] = LpVariable(f"y_{i}_{k}", cat='Binary')

        # Delivery quantities
        q = {i: LpVariable(f"q_{i}", lowBound=0) for i in customers}

        # Objective: Minimize routing cost + inventory holding cost
        routing_cost = lpSum([
            self.dist_matrix[i, j] * self.c_routing * x[i, j, k]
            for i in nodes for j in nodes for k in vehicles if i != j
        ])

        # Inventory after delivery
        inventory_after = {i: self.I[i - 1] + q[i] for i in customers}
        holding_cost = self.h * lpSum([inventory_after[i] for i in customers])

        prob += routing_cost + holding_cost

        # Constraints

        # 1. Each customer visited at most once
        for i in customers:
            prob += lpSum([y[i, k] for k in vehicles]) <= 1

        # 2. Visit variable linking
        for i in customers:
            for k in vehicles:
                prob += lpSum([x[j, i, k] for j in nodes if j != i]) == y[i, k]
                prob += lpSum([x[i, j, k] for j in nodes if j != i]) == y[i, k]

        # 3. Vehicle starts and ends at depot
        for k in vehicles:
            prob += lpSum([x[0, j, k] for j in customers]) <= 1
            prob += lpSum([x[i, 0, k] for i in customers]) <= 1
            prob += (lpSum([x[0, j, k] for j in customers]) ==
                    lpSum([x[i, 0, k] for i in customers]))

        # 4. Flow conservation
        for k in vehicles:
            for j in customers:
                prob += (lpSum([x[i, j, k] for i in nodes if i != j]) ==
                        lpSum([x[j, i, k] for i in nodes if i != j]))

        # 5. Vehicle capacity
        for k in vehicles:
            prob += lpSum([q[i] * y[i, k] for i in customers]) <= self.Q

        # 6. Delivery quantity constraints
        for i in customers:
            # Don't deliver more than capacity minus current inventory
            prob += q[i] <= (self.C[i - 1] - self.I[i - 1]) * lpSum([y[i, k]
                                                                      for k in vehicles])

            # If visited, deliver enough to avoid stockout until next delivery
            min_delivery = max(0, time_until_next_delivery * self.d[i - 1] - self.I[i - 1])
            prob += q[i] >= min_delivery * lpSum([y[i, k] for k in vehicles])

        # 7. Subtour elimination (MTZ formulation)
        u = {i: LpVariable(f"u_{i}", lowBound=0, upBound=self.n) for i in customers}

        for i in customers:
            for j in customers:
                for k in vehicles:
                    if i != j:
                        prob += u[i] - u[j] + self.n * x[i, j, k] <= self.n - 1

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        routes = self._extract_routes(x, vehicles, nodes)
        deliveries = {i: q[i].varValue if q[i].varValue else 0 for i in customers}

        total_distance = sum(
            self.dist_matrix[i, j] * x[i, j, k].varValue
            for i in nodes for j in nodes for k in vehicles
            if i != j and x[i, j, k].varValue > 0.5
        )

        total_delivery = sum(deliveries.values())

        return {
            'status': LpStatus[prob.status],
            'routes': routes,
            'deliveries': deliveries,
            'total_cost': value(prob.objective),
            'routing_cost': self.c_routing * total_distance,
            'holding_cost': self.h * sum(self.I[i - 1] + deliveries[i]
                                         for i in customers),
            'total_distance': total_distance,
            'total_delivery': total_delivery,
            'vehicles_used': len([r for r in routes if len(r) > 2])
        }

    def _extract_routes(self, x, vehicles, nodes):
        """Extract route sequences from solution"""

        routes = []

        for k in vehicles:
            route = [0]  # Start at depot
            current = 0

            while True:
                next_node = None
                for j in nodes:
                    if j != current and (current, j, k) in x:
                        if x[current, j, k].varValue > 0.5:
                            next_node = j
                            break

                if next_node is None or next_node == 0:
                    if len(route) > 1:
                        route.append(0)  # Return to depot
                        routes.append(route)
                    break

                route.append(next_node)
                current = next_node

        return routes

    def plot_solution(self, solution: Dict):
        """Visualize IRP solution"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Plot 1: Routes
        colors = plt.cm.tab10(np.linspace(0, 1, len(solution['routes'])))

        # Plot depot
        ax1.plot(self.depot[0], self.depot[1], 'rs', markersize=15,
                label='Depot', zorder=5)

        # Plot customers
        for i in range(self.n):
            ax1.plot(self.customer_locations[i, 0],
                    self.customer_locations[i, 1],
                    'bo', markersize=10, zorder=3)
            ax1.text(self.customer_locations[i, 0],
                    self.customer_locations[i, 1],
                    f'  {i+1}', fontsize=9)

        # Plot routes
        for route_idx, route in enumerate(solution['routes']):
            if len(route) > 2:
                route_coords = np.vstack([
                    self.depot if node == 0
                    else self.customer_locations[node - 1]
                    for node in route
                ])

                ax1.plot(route_coords[:, 0], route_coords[:, 1],
                        'o-', color=colors[route_idx], linewidth=2,
                        markersize=8, label=f'Route {route_idx + 1}',
                        alpha=0.7)

        ax1.set_xlabel('X Coordinate')
        ax1.set_ylabel('Y Coordinate')
        ax1.set_title('Vehicle Routes', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Inventory levels
        customer_ids = np.arange(1, self.n + 1)
        current_inv = self.I
        deliveries = [solution['deliveries'][i] for i in customer_ids]
        final_inv = current_inv + deliveries
        capacity = self.C

        x_pos = np.arange(self.n)
        width = 0.35

        ax2.bar(x_pos - width/2, current_inv, width, label='Current Inventory',
               alpha=0.7, color='orange')
        ax2.bar(x_pos + width/2, final_inv, width, label='After Delivery',
               alpha=0.7, color='green')
        ax2.plot(x_pos, capacity, 'r--', linewidth=2, label='Max Capacity')

        # Mark delivered customers
        delivered_customers = [i for i in customer_ids if deliveries[i - 1] > 0]
        if delivered_customers:
            ax2.scatter([c - 1 for c in delivered_customers],
                       [final_inv[c - 1] for c in delivered_customers],
                       s=200, marker='*', color='red', zorder=5,
                       label='Delivered')

        ax2.set_xlabel('Customer ID')
        ax2.set_ylabel('Inventory Level (units)')
        ax2.set_title('Inventory Levels Before and After', fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(customer_ids)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        return plt


# Example Usage
def example_single_period_irp():
    """Example: Single-period IRP with 8 customers"""

    print("\n" + "=" * 70)
    print("INVENTORY ROUTING PROBLEM (IRP): SINGLE-PERIOD")
    print("=" * 70)

    np.random.seed(42)

    # Problem setup
    num_customers = 8
    depot = np.array([50, 50])

    # Customer locations (random)
    customer_locations = np.random.rand(num_customers, 2) * 100

    # Current inventory (random, 20-80% of capacity)
    max_inventory = np.random.randint(80, 150, num_customers)
    current_inventory = max_inventory * np.random.uniform(0.2, 0.8, num_customers)

    # Consumption rates (units per day)
    consumption_rates = np.random.uniform(5, 20, num_customers)

    # Days until will stock out if not replenished
    days_until_stockout = current_inventory / consumption_rates

    print("\nProblem Data:")
    print(f"  Number of Customers: {num_customers}")
    print(f"  Vehicle Capacity: 200 units")
    print(f"  Number of Vehicles: 3")
    print(f"  Planning Period: 1 day")

    print("\n  Customer Inventory Status:")
    print(f"\n  {'Customer':<12} {'Current':<12} {'Capacity':<12} {'Usage/Day':<12} "
          f"{'Days to Stockout'}")
    print("  " + "-" * 65)

    for i in range(num_customers):
        print(f"  {i+1:<12} {current_inventory[i]:<12.0f} "
              f"{max_inventory[i]:<12.0f} {consumption_rates[i]:<12.1f} "
              f"{days_until_stockout[i]:<.1f}")

    # Create and solve IRP
    irp = SinglePeriodIRP(
        num_customers=num_customers,
        customer_locations=customer_locations,
        depot_location=depot,
        current_inventory=current_inventory,
        consumption_rates=consumption_rates,
        max_inventory=max_inventory,
        vehicle_capacity=200,
        num_vehicles=3,
        holding_cost=1.0,
        routing_cost_per_km=2.0
    )

    print("\nSolving IRP with MIP...")
    solution = irp.solve_mip(time_until_next_delivery=3)  # Plan for 3 days

    print(f"\n{'=' * 70}")
    print("OPTIMAL SOLUTION")
    print("=" * 70)

    print(f"\n{'Status:':<30} {solution['status']}")
    print(f"{'Total Cost:':<30} ${solution['total_cost']:,.2f}")
    print(f"{'Routing Cost:':<30} ${solution['routing_cost']:,.2f}")
    print(f"{'Holding Cost:':<30} ${solution['holding_cost']:,.2f}")
    print(f"{'Total Distance:':<30} {solution['total_distance']:.1f} km")
    print(f"{'Vehicles Used:':<30} {solution['vehicles_used']}")
    print(f"{'Total Delivered:':<30} {solution['total_delivery']:.0f} units")

    print("\n  Vehicle Routes and Deliveries:")
    for route_idx, route in enumerate(solution['routes']):
        if len(route) > 2:
            print(f"\n  Route {route_idx + 1}: ", end='')
            print(" → ".join([f"Depot" if node == 0 else f"Cust {node}"
                             for node in route]))

            route_delivery = sum(solution['deliveries'][node]
                               for node in route if node > 0)
            print(f"    Total delivery on route: {route_delivery:.0f} units")

            for node in route:
                if node > 0:
                    delivery = solution['deliveries'][node]
                    if delivery > 0:
                        print(f"      Customer {node}: Deliver {delivery:.0f} units")

    # Plot solution
    irp.plot_solution(solution)
    plt.savefig('/tmp/irp_single_period.png', dpi=300, bbox_inches='tight')
    print(f"\nSolution plot saved to /tmp/irp_single_period.png")

    return irp, solution


if __name__ == "__main__":
    example_single_period_irp()
```

---

## Multi-Period IRP

### Rolling Horizon Approach

```python
class MultiPeriodIRP:
    """
    Multi-Period IRP using rolling horizon approach

    Solve single-period IRP repeatedly, updating inventory levels
    """

    def __init__(self, single_period_irp: SinglePeriodIRP,
                 num_periods: int, delivery_frequency: int = 2):
        """
        Parameters:
        -----------
        single_period_irp : SinglePeriodIRP
            Single-period IRP model
        num_periods : int
            Number of periods to plan
        delivery_frequency : int
            Minimum periods between deliveries to same customer
        """
        self.irp = single_period_irp
        self.T = num_periods
        self.freq = delivery_frequency

        # Track inventory over time
        self.inventory_history = np.zeros((num_periods + 1, self.irp.n))
        self.inventory_history[0] = self.irp.I

        # Track deliveries
        self.delivery_history = []

        # Track routes
        self.route_history = []

    def solve_rolling_horizon(self) -> Dict:
        """Solve multi-period IRP using rolling horizon"""

        total_cost = 0
        total_distance = 0
        total_delivered = 0

        for t in range(self.T):
            print(f"  Period {t+1}/{self.T}...", end='')

            # Update current inventory in IRP model
            self.irp.I = self.inventory_history[t]

            # Solve single-period IRP
            solution = self.irp.solve_mip(time_until_next_delivery=self.freq)

            # Record solution
            self.route_history.append(solution['routes'])
            self.delivery_history.append(solution['deliveries'])

            # Update costs
            total_cost += solution['total_cost']
            total_distance += solution['total_distance']
            total_delivered += solution['total_delivery']

            # Update inventory for next period
            for i in range(1, self.irp.n + 1):
                delivered = solution['deliveries'][i]
                consumed = self.irp.d[i - 1]
                self.inventory_history[t + 1, i - 1] = (
                    self.inventory_history[t, i - 1] + delivered - consumed
                )

            print(f" Cost: ${solution['total_cost']:.2f}")

        return {
            'total_cost': total_cost,
            'total_distance': total_distance,
            'total_delivered': total_delivered,
            'avg_cost_per_period': total_cost / self.T,
            'inventory_history': self.inventory_history,
            'delivery_history': self.delivery_history,
            'route_history': self.route_history
        }


# Example: Multi-period
def example_multi_period_irp():
    """Example: 7-day multi-period IRP"""

    print("\n" + "=" * 70)
    print("MULTI-PERIOD INVENTORY ROUTING PROBLEM")
    print("=" * 70)

    np.random.seed(42)

    # Setup (smaller problem for multi-period)
    num_customers = 5
    depot = np.array([50, 50])
    customer_locations = np.random.rand(num_customers, 2) * 100

    max_inventory = np.array([100, 120, 80, 150, 100])
    current_inventory = np.array([80, 90, 60, 100, 70])
    consumption_rates = np.array([10, 15, 8, 20, 12])

    # Create single-period IRP
    irp = SinglePeriodIRP(
        num_customers=num_customers,
        customer_locations=customer_locations,
        depot_location=depot,
        current_inventory=current_inventory,
        consumption_rates=consumption_rates,
        max_inventory=max_inventory,
        vehicle_capacity=150,
        num_vehicles=2,
        holding_cost=0.5,
        routing_cost_per_km=2.0
    )

    # Create multi-period wrapper
    multi_irp = MultiPeriodIRP(irp, num_periods=7, delivery_frequency=2)

    print("\nSolving 7-day multi-period IRP...")
    print("  Using rolling horizon approach")

    solution = multi_irp.solve_rolling_horizon()

    print(f"\n{'=' * 70}")
    print("MULTI-PERIOD RESULTS (7 days)")
    print("=" * 70)

    print(f"\n{'Total Cost (7 days):':<30} ${solution['total_cost']:,.2f}")
    print(f"{'Average Cost per Day:':<30} ${solution['avg_cost_per_period']:,.2f}")
    print(f"{'Total Distance:':<30} {solution['total_distance']:.1f} km")
    print(f"{'Total Delivered:':<30} {solution['total_delivered']:.0f} units")

    # Plot inventory evolution
    fig, axes = plt.subplots(num_customers, 1, figsize=(12, 10))

    for i in range(num_customers):
        axes[i].plot(range(8), solution['inventory_history'][:, i],
                    marker='o', linewidth=2, color='blue')
        axes[i].axhline(y=max_inventory[i], color='red', linestyle='--',
                       label='Capacity')
        axes[i].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Mark delivery days
        for t in range(7):
            if multi_irp.delivery_history[t][i + 1] > 0:
                axes[i].plot(t, solution['inventory_history'][t, i],
                           'g^', markersize=12, label='Delivery' if t == 0 else '')

        axes[i].set_ylabel(f'Cust {i+1}\nInventory')
        axes[i].grid(True, alpha=0.3)
        if i == 0:
            axes[i].legend()

    axes[-1].set_xlabel('Day')
    plt.suptitle('Inventory Evolution Over 7 Days', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('/tmp/irp_multi_period.png', dpi=300, bbox_inches='tight')

    print(f"\nInventory evolution plot saved to /tmp/irp_multi_period.png")

    return multi_irp, solution


if __name__ == "__main__":
    example_multi_period_irp()
```

---

## Tools & Libraries

### Python Libraries
- `pulp`, `pyomo`: MIP modeling
- `ortools`: Google OR-Tools for routing
- `numpy`, `scipy`: Numerical computations

### Commercial Software
- **Blue Yonder TMS**: Transportation with VMI
- **Manhattan Associates**: WMS/TMS integration with inventory
- **SAP TM + EWM**: Integrated transportation and warehouse management
- **Oracle Transportation Management**: Route optimization with inventory
- **Descartes**: Routing with inventory considerations

---

## Common Challenges & Solutions

### Challenge: Problem Size and Complexity
**Problem:** Combinatorial explosion with many customers and periods
**Solutions:**
- Rolling horizon approach
- Cluster-first, route-second heuristics
- Decomposition methods
- Limit optimization time, use good heuristics

### Challenge: Demand Uncertainty
**Problem:** Stochastic consumption rates
**Solutions:**
- Safety stock at customers
- Robust optimization with demand scenarios
- Frequent replanning
- Risk pooling at depot

### Challenge: Time Windows and Service Requirements
**Problem:** Customers have delivery windows, minimum frequencies
**Solutions:**
- Add time window constraints to MIP
- Multi-objective optimization (cost vs. service)
- Penalty costs for violations
- Contract-based service level agreements

### Challenge: Heterogeneous Fleet
**Problem:** Different vehicle types (capacity, cost)
**Solutions:**
- Index vehicles by type in model
- Type-specific routing costs
- Preferential use of lower-cost vehicles

---

## Related Skills

- **vehicle-routing-problem**: Pure routing optimization
- **route-optimization**: Transportation planning
- **inventory-optimization**: Inventory management
- **multi-echelon-inventory**: Network inventory
- **network-design**: Strategic distribution network
- **fleet-management**: Vehicle fleet operations
- **demand-forecasting**: Consumption rate prediction
