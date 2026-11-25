---
name: network-flow-optimization
description: When the user wants to optimize network flows, solve minimum cost flow problems, or design flow networks. Also use when the user mentions "min cost flow," "maximum flow," "network flow problem," "transportation problem," "transshipment problem," "multi-commodity flow," "supply chain flow optimization," or "network capacity planning." For facility location, see facility-location-problem. For distribution networks, see distribution-center-network.
---

# Network Flow Optimization

You are an expert in network flow optimization and graph-based supply chain problems. Your goal is to help optimize flows through networks to minimize costs, maximize throughput, or balance multiple objectives while respecting capacity constraints and flow conservation.

## Initial Assessment

Before optimizing network flows, understand:

1. **Network Type**
   - Transportation problem? (sources → destinations, single commodity)
   - Transshipment problem? (intermediate nodes allowed)
   - Min-cost flow? (minimize cost given supplies and demands)
   - Max flow? (maximize total flow from source to sink)
   - Multi-commodity flow? (multiple products sharing network)

2. **Network Structure**
   - How many nodes? (sources, intermediate, sinks)
   - How many arcs/edges?
   - Directed or undirected?
   - Node types: supply nodes, demand nodes, transshipment nodes?
   - Network layers or echelons?

3. **Flow Characteristics**
   - Single commodity or multi-commodity?
   - Splittable flows? (can split along multiple paths)
   - Flow units? (tons, pallets, vehicles, data packets)
   - Time dimension? (static or dynamic flows)

4. **Capacities and Costs**
   - Arc capacities? (upper bounds on flows)
   - Node capacities? (throughput limits)
   - Flow costs per unit?
   - Fixed costs for using arcs?
   - Economies of scale?

5. **Supplies and Demands**
   - Supply at source nodes?
   - Demand at destination nodes?
   - Balanced network? (total supply = total demand)
   - Excess supply or unmet demand allowed?

---

## Network Flow Problem Framework

### Problem Classification

**1. Transportation Problem**
```
m sources → n destinations
- Single commodity
- Direct shipments only
- Minimize total transportation cost
```

**2. Transshipment Problem**
```
Sources → Intermediate nodes → Destinations
- Allows intermediate stops
- More flexible routing
- Includes warehouses, hubs, cross-docks
```

**3. Minimum Cost Flow Problem**
```
General network with supplies, demands, costs, capacities
- Most general formulation
- Subsumes transportation and transshipment
- Linear programming problem
```

**4. Maximum Flow Problem**
```
Single source → Single sink
- Maximize total flow
- Subject to arc capacities
- Applications: network capacity, throughput
```

**5. Multi-Commodity Flow**
```
Multiple products/commodities sharing network
- Product-specific demands
- Shared arc capacities
- More complex but realistic
```

---

## Mathematical Formulations

### Minimum Cost Flow Problem

**Network:**
- G = (N, A): Directed graph with nodes N and arcs A

**Parameters:**
- b_i: Net supply at node i
  - b_i > 0: supply node
  - b_i < 0: demand node (demand = -b_i)
  - b_i = 0: transshipment node
- c_{ij}: Unit cost on arc (i,j)
- u_{ij}: Capacity on arc (i,j)
- l_{ij}: Lower bound on arc (i,j) (often 0)

**Decision Variables:**
- x_{ij}: Flow on arc (i,j)

**Objective Function:**
```
Minimize: Σ_{(i,j) ∈ A} c_{ij} × x_{ij}
```

**Constraints:**
```
1. Flow conservation at each node:
   Σ_{j:(i,j)∈A} x_{ij} - Σ_{j:(j,i)∈A} x_{ji} = b_i,  ∀i ∈ N

   (Outflow - Inflow = Net Supply)

2. Arc capacity constraints:
   l_{ij} ≤ x_{ij} ≤ u_{ij},  ∀(i,j) ∈ A

3. Non-negativity (if no lower bounds):
   x_{ij} ≥ 0,  ∀(i,j) ∈ A

4. Balanced network:
   Σ_{i∈N} b_i = 0
   (Total supply = Total demand)
```

**Properties:**
- Linear programming problem
- Polynomial-time solvable
- Network simplex very efficient

### Transportation Problem

**Simplified formulation:**
- m sources with supplies s_i
- n destinations with demands d_j
- Cost c_{ij} to ship from source i to destination j

**Variables:**
- x_{ij}: Amount shipped from source i to destination j

**Objective:**
```
Minimize: Σ_i Σ_j c_{ij} × x_{ij}
```

**Constraints:**
```
1. Supply constraints:
   Σ_j x_{ij} ≤ s_i,  ∀i (sources)

2. Demand constraints:
   Σ_i x_{ij} ≥ d_j,  ∀j (destinations)

3. Non-negativity:
   x_{ij} ≥ 0,  ∀i,j
```

### Multi-Commodity Flow

**Additional notation:**
- K: Set of commodities/products
- b_i^k: Supply/demand of commodity k at node i
- c_{ij}^k: Cost per unit of commodity k on arc (i,j)
- u_{ij}: Total capacity on arc (i,j) (shared)

**Variables:**
- x_{ij}^k: Flow of commodity k on arc (i,j)

**Objective:**
```
Minimize: Σ_k Σ_{(i,j)∈A} c_{ij}^k × x_{ij}^k
```

**Constraints:**
```
1. Flow conservation per commodity:
   Σ_j x_{ij}^k - Σ_j x_{ji}^k = b_i^k,  ∀i ∈ N, ∀k ∈ K

2. Shared arc capacity:
   Σ_k x_{ij}^k ≤ u_{ij},  ∀(i,j) ∈ A

3. Non-negativity:
   x_{ij}^k ≥ 0,  ∀(i,j) ∈ A, ∀k ∈ K
```

---

## Solution Methods

### 1. Minimum Cost Flow with NetworkX

```python
import networkx as nx
import matplotlib.pyplot as plt

def solve_min_cost_flow_nx(nodes, arcs, supplies, costs, capacities):
    """
    Solve minimum cost flow using NetworkX

    Args:
        nodes: list of node IDs
        arcs: list of (source, target) tuples
        supplies: dict {node: supply} (negative for demand)
        costs: dict {(source, target): cost}
        capacities: dict {(source, target): capacity}

    Returns:
        optimal flow solution
    """

    # Create directed graph
    G = nx.DiGraph()

    # Add nodes with demands
    for node in nodes:
        demand = -supplies.get(node, 0)  # NetworkX uses demand (negative supply)
        G.add_node(node, demand=demand)

    # Add arcs with costs and capacities
    for (i, j) in arcs:
        G.add_edge(i, j,
                  weight=costs.get((i,j), 0),
                  capacity=capacities.get((i,j), float('inf')))

    # Solve min cost flow
    try:
        flow_dict = nx.min_cost_flow(G)

        # Extract flows
        flows = {}
        for i in flow_dict:
            for j in flow_dict[i]:
                if flow_dict[i][j] > 0:
                    flows[(i,j)] = flow_dict[i][j]

        # Calculate total cost
        total_cost = nx.cost_of_flow(G, flow_dict)

        return {
            'status': 'Optimal',
            'flows': flows,
            'total_cost': total_cost,
            'flow_dict': flow_dict
        }

    except nx.NetworkXUnfeasible:
        return {'status': 'Infeasible'}

    except Exception as e:
        return {'status': f'Error: {str(e)}'}


# Example usage
if __name__ == "__main__":
    # Example: Supply chain network
    # 2 plants → 2 DCs → 3 customers

    nodes = ['Plant1', 'Plant2', 'DC1', 'DC2',
             'Customer1', 'Customer2', 'Customer3']

    # Define arcs (directed edges)
    arcs = [
        # Plant to DC
        ('Plant1', 'DC1'), ('Plant1', 'DC2'),
        ('Plant2', 'DC1'), ('Plant2', 'DC2'),
        # DC to Customer
        ('DC1', 'Customer1'), ('DC1', 'Customer2'), ('DC1', 'Customer3'),
        ('DC2', 'Customer1'), ('DC2', 'Customer2'), ('DC2', 'Customer3')
    ]

    # Supplies (positive) and demands (negative)
    supplies = {
        'Plant1': 100,
        'Plant2': 150,
        'DC1': 0,  # Transshipment
        'DC2': 0,  # Transshipment
        'Customer1': -80,
        'Customer2': -90,
        'Customer3': -80
    }

    # Transportation costs
    costs = {
        ('Plant1', 'DC1'): 10, ('Plant1', 'DC2'): 12,
        ('Plant2', 'DC1'): 8, ('Plant2', 'DC2'): 11,
        ('DC1', 'Customer1'): 5, ('DC1', 'Customer2'): 7, ('DC1', 'Customer3'): 6,
        ('DC2', 'Customer1'): 6, ('DC2', 'Customer2'): 5, ('DC2', 'Customer3'): 8
    }

    # Arc capacities
    capacities = {
        ('Plant1', 'DC1'): 80, ('Plant1', 'DC2'): 70,
        ('Plant2', 'DC1'): 90, ('Plant2', 'DC2'): 100,
        ('DC1', 'Customer1'): 60, ('DC1', 'Customer2'): 70, ('DC1', 'Customer3'): 50,
        ('DC2', 'Customer1'): 70, ('DC2', 'Customer2'): 60, ('DC2', 'Customer3'): 80
    }

    print("="*70)
    print("MINIMUM COST FLOW PROBLEM")
    print("="*70)
    print(f"Nodes: {len(nodes)}")
    print(f"Arcs: {len(arcs)}")
    print(f"Total supply: {sum(v for v in supplies.values() if v > 0)}")
    print(f"Total demand: {-sum(v for v in supplies.values() if v < 0)}")

    result = solve_min_cost_flow_nx(nodes, arcs, supplies, costs, capacities)

    print(f"\n{'='*70}")
    print(f"OPTIMAL SOLUTION")
    print(f"{'='*70}")
    print(f"Status: {result['status']}")
    print(f"Total Cost: ${result['total_cost']:,.2f}")

    print(f"\nOptimal Flows:")
    for (i, j), flow in result['flows'].items():
        cost = costs.get((i,j), 0)
        capacity = capacities.get((i,j), 'inf')
        print(f"  {i:12} → {j:12}: {flow:6.1f} units "
              f"(cost=${cost}, capacity={capacity})")
```

### 2. Transportation Problem with PuLP

```python
from pulp import *
import numpy as np

def solve_transportation_problem(sources, destinations, supplies,
                                demands, costs):
    """
    Solve Transportation Problem

    Args:
        sources: list of source IDs
        destinations: list of destination IDs
        supplies: dict {source: supply}
        demands: dict {destination: demand}
        costs: dict {(source, dest): unit_cost}

    Returns:
        optimal transportation plan
    """

    # Create problem
    prob = LpProblem("Transportation", LpMinimize)

    # Decision variables
    x = {}
    for i in sources:
        for j in destinations:
            x[i,j] = LpVariable(f"ship_{i}_{j}", lowBound=0, cat='Continuous')

    # Objective: Minimize total transportation cost
    prob += (
        lpSum([costs[i,j] * x[i,j] for i in sources for j in destinations]),
        "Total_Cost"
    )

    # Constraints

    # 1. Supply constraints (can't ship more than available)
    for i in sources:
        prob += (
            lpSum([x[i,j] for j in destinations]) <= supplies[i],
            f"Supply_{i}"
        )

    # 2. Demand constraints (must meet all demand)
    for j in destinations:
        prob += (
            lpSum([x[i,j] for i in sources]) >= demands[j],
            f"Demand_{j}"
        )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=0))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        shipments = {}
        for i in sources:
            for j in destinations:
                if x[i,j].varValue > 0.01:
                    shipments[i,j] = x[i,j].varValue

        # Calculate utilization
        source_utilization = {}
        for i in sources:
            total_shipped = sum(x[i,j].varValue for j in destinations)
            source_utilization[i] = (total_shipped / supplies[i]) * 100

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'shipments': shipments,
            'source_utilization': source_utilization,
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
sources = ['Factory_A', 'Factory_B', 'Factory_C']
destinations = ['Market_1', 'Market_2', 'Market_3', 'Market_4']

supplies = {
    'Factory_A': 200,
    'Factory_B': 300,
    'Factory_C': 250
}

demands = {
    'Market_1': 150,
    'Market_2': 200,
    'Market_3': 180,
    'Market_4': 170
}

# Randomly generate costs
np.random.seed(42)
costs = {}
for i in sources:
    for j in destinations:
        costs[i,j] = np.random.uniform(10, 50)

print("\n" + "="*70)
print("TRANSPORTATION PROBLEM")
print("="*70)
print(f"Sources: {len(sources)}")
print(f"Destinations: {len(destinations)}")
print(f"Total supply: {sum(supplies.values())}")
print(f"Total demand: {sum(demands.values())}")

result = solve_transportation_problem(sources, destinations, supplies,
                                     demands, costs)

print(f"\n{'='*70}")
print(f"OPTIMAL SOLUTION")
print(f"{'='*70}")
print(f"Status: {result['status']}")
print(f"Total Cost: ${result['total_cost']:,.2f}")

print(f"\nOptimal Shipments:")
for (i, j), quantity in result['shipments'].items():
    cost_per_unit = costs[i,j]
    total_arc_cost = quantity * cost_per_unit
    print(f"  {i} → {j}: {quantity:.1f} units "
          f"(@${cost_per_unit:.2f}/unit = ${total_arc_cost:,.2f})")

print(f"\nSource Utilization:")
for source, util in result['source_utilization'].items():
    print(f"  {source}: {util:.1f}% ({supplies[source]} available)")
```

### 3. Multi-Commodity Flow

```python
def solve_multi_commodity_flow(nodes, arcs, products, supplies, costs,
                               arc_capacities):
    """
    Solve Multi-Commodity Flow Problem

    Args:
        nodes: list of nodes
        arcs: list of (source, target) tuples
        products: list of product IDs
        supplies: dict {(node, product): supply} (negative for demand)
        costs: dict {(source, target, product): cost}
        arc_capacities: dict {(source, target): shared capacity}

    Returns:
        optimal multi-commodity flow
    """

    prob = LpProblem("Multi_Commodity_Flow", LpMinimize)

    # Decision variables: x[i,j,k] = flow of product k on arc (i,j)
    x = {}
    for (i, j) in arcs:
        for k in products:
            x[i,j,k] = LpVariable(f"flow_{i}_{j}_{k}",
                                 lowBound=0, cat='Continuous')

    # Objective: Minimize total cost across all products
    prob += (
        lpSum([costs.get((i,j,k), 0) * x[i,j,k]
               for (i,j) in arcs for k in products]),
        "Total_Cost"
    )

    # Constraints

    # 1. Flow conservation for each product at each node
    for node in nodes:
        for k in products:
            # Outflow - Inflow = Supply
            outflow = lpSum([x[i,j,k] for (i,j) in arcs if i == node])
            inflow = lpSum([x[i,j,k] for (i,j) in arcs if j == node])

            prob += (
                outflow - inflow == supplies.get((node, k), 0),
                f"Flow_Conservation_{node}_{k}"
            )

    # 2. Shared arc capacity constraints
    for (i, j) in arcs:
        prob += (
            lpSum([x[i,j,k] for k in products]) <= arc_capacities.get((i,j), float('inf')),
            f"Capacity_{i}_{j}"
        )

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=600))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] in ['Optimal', 'Feasible']:
        flows = {}
        for (i,j) in arcs:
            for k in products:
                if x[i,j,k].varValue > 0.01:
                    flows[i,j,k] = x[i,j,k].varValue

        # Calculate arc utilization
        arc_utilization = {}
        for (i,j) in arcs:
            total_flow = sum(x[i,j,k].varValue for k in products)
            capacity = arc_capacities.get((i,j), float('inf'))
            if capacity != float('inf'):
                arc_utilization[i,j] = (total_flow / capacity) * 100

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'flows': flows,
            'arc_utilization': arc_utilization,
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'solve_time': solve_time
        }


# Example usage
nodes = ['Plant', 'DC1', 'DC2', 'Customer1', 'Customer2']
arcs = [
    ('Plant', 'DC1'), ('Plant', 'DC2'),
    ('DC1', 'Customer1'), ('DC1', 'Customer2'),
    ('DC2', 'Customer1'), ('DC2', 'Customer2')
]
products = ['ProductA', 'ProductB', 'ProductC']

# Product-specific supplies/demands
supplies = {
    ('Plant', 'ProductA'): 100,
    ('Plant', 'ProductB'): 150,
    ('Plant', 'ProductC'): 120,
    ('Customer1', 'ProductA'): -40,
    ('Customer1', 'ProductB'): -60,
    ('Customer1', 'ProductC'): -50,
    ('Customer2', 'ProductA'): -60,
    ('Customer2', 'ProductB'): -90,
    ('Customer2', 'ProductC'): -70
}

# Product-specific costs
costs = {}
for (i,j) in arcs:
    for k in products:
        costs[i,j,k] = np.random.uniform(5, 25)

# Shared arc capacities
arc_capacities = {
    ('Plant', 'DC1'): 200,
    ('Plant', 'DC2'): 180,
    ('DC1', 'Customer1'): 100,
    ('DC1', 'Customer2'): 120,
    ('DC2', 'Customer1'): 110,
    ('DC2', 'Customer2'): 130
}

print("\n" + "="*70)
print("MULTI-COMMODITY FLOW PROBLEM")
print("="*70)
print(f"Nodes: {len(nodes)}")
print(f"Arcs: {len(arcs)}")
print(f"Products: {len(products)}")

result = solve_multi_commodity_flow(nodes, arcs, products, supplies,
                                   costs, arc_capacities)

print(f"\n{'='*70}")
print(f"OPTIMAL SOLUTION")
print(f"{'='*70}")
print(f"Status: {result['status']}")
print(f"Total Cost: ${result['total_cost']:,.2f}")

print(f"\nOptimal Flows (sample - first 15):")
count = 0
for (i,j,k), flow in result['flows'].items():
    if count >= 15:
        break
    cost_per_unit = costs[i,j,k]
    print(f"  {i} → {j} ({k}): {flow:.1f} units @${cost_per_unit:.2f}/unit")
    count += 1

print(f"\nArc Utilization:")
for (i,j), util in result['arc_utilization'].items():
    capacity = arc_capacities[i,j]
    print(f"  {i} → {j}: {util:.1f}% (capacity={capacity})")
```

---

## Advanced Algorithms

### 1. Maximum Flow (Ford-Fulkerson)

```python
def max_flow_ford_fulkerson(graph, source, sink):
    """
    Maximum flow using Ford-Fulkerson algorithm with BFS (Edmonds-Karp)

    Args:
        graph: dict {node: {neighbor: capacity}}
        source: source node
        sink: sink node

    Returns:
        maximum flow value and flow assignment
    """
    from collections import deque, defaultdict

    # Create residual graph
    residual = defaultdict(lambda: defaultdict(int))
    for u in graph:
        for v in graph[u]:
            residual[u][v] = graph[u][v]

    def bfs_find_path():
        """Find augmenting path using BFS"""
        visited = {source}
        queue = deque([(source, [source])])

        while queue:
            node, path = queue.popleft()

            if node == sink:
                return path

            for neighbor in residual[node]:
                if neighbor not in visited and residual[node][neighbor] > 0:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    max_flow_value = 0

    # Find augmenting paths
    while True:
        path = bfs_find_path()

        if path is None:
            break

        # Find bottleneck capacity
        flow = min(residual[path[i]][path[i+1]]
                  for i in range(len(path)-1))

        # Update residual graph
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            residual[u][v] -= flow
            residual[v][u] += flow

        max_flow_value += flow

    # Extract final flow
    flow_assignment = {}
    for u in graph:
        for v in graph[u]:
            flow_on_edge = graph[u][v] - residual[u][v]
            if flow_on_edge > 0:
                flow_assignment[u,v] = flow_on_edge

    return {
        'max_flow': max_flow_value,
        'flow_assignment': flow_assignment
    }


# Example
graph = {
    'S': {'A': 10, 'B': 5},
    'A': {'B': 15, 'C': 10},
    'B': {'D': 10},
    'C': {'D': 10, 'T': 5},
    'D': {'T': 10},
    'T': {}
}

result = max_flow_ford_fulkerson(graph, 'S', 'T')

print("\n" + "="*70)
print("MAXIMUM FLOW PROBLEM")
print("="*70)
print(f"Maximum Flow: {result['max_flow']}")
print(f"\nFlow Assignment:")
for (u,v), flow in result['flow_assignment'].items():
    print(f"  {u} → {v}: {flow}")
```

---

## Complete Network Flow Solver

```python
class NetworkFlowSolver:
    """
    Comprehensive Network Flow Optimization Solver
    """

    def __init__(self):
        self.problem_type = None
        self.loaded = False

    def load_min_cost_flow(self, nodes, arcs, supplies, costs, capacities):
        """Load minimum cost flow problem"""
        self.nodes = nodes
        self.arcs = arcs
        self.supplies = supplies
        self.costs = costs
        self.capacities = capacities
        self.problem_type = 'min_cost_flow'
        self.loaded = True

        print(f"Loaded Minimum Cost Flow Problem:")
        print(f"  Nodes: {len(nodes)}")
        print(f"  Arcs: {len(arcs)}")
        total_supply = sum(v for v in supplies.values() if v > 0)
        total_demand = -sum(v for v in supplies.values() if v < 0)
        print(f"  Total supply: {total_supply}")
        print(f"  Total demand: {total_demand}")
        print(f"  Balanced: {abs(total_supply - total_demand) < 0.01}")

    def load_transportation(self, sources, destinations, supplies,
                          demands, costs):
        """Load transportation problem"""
        self.sources = sources
        self.destinations = destinations
        self.supplies_trans = supplies
        self.demands_trans = demands
        self.costs_trans = costs
        self.problem_type = 'transportation'
        self.loaded = True

        print(f"Loaded Transportation Problem:")
        print(f"  Sources: {len(sources)}")
        print(f"  Destinations: {len(destinations)}")
        print(f"  Total supply: {sum(supplies.values())}")
        print(f"  Total demand: {sum(demands.values())}")

    def solve_exact(self):
        """Solve with exact method"""
        if not self.loaded:
            raise ValueError("Problem not loaded")

        if self.problem_type == 'min_cost_flow':
            return solve_min_cost_flow_nx(
                self.nodes, self.arcs, self.supplies,
                self.costs, self.capacities
            )

        elif self.problem_type == 'transportation':
            return solve_transportation_problem(
                self.sources, self.destinations,
                self.supplies_trans, self.demands_trans,
                self.costs_trans
            )

    def visualize_network(self, solution=None):
        """Visualize network and flows"""
        if self.problem_type != 'min_cost_flow':
            print("Visualization only for min cost flow currently")
            return

        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.DiGraph()

        # Add nodes
        for node in self.nodes:
            supply = self.supplies.get(node, 0)
            if supply > 0:
                G.add_node(node, node_type='supply')
            elif supply < 0:
                G.add_node(node, node_type='demand')
            else:
                G.add_node(node, node_type='transshipment')

        # Add arcs
        for (i, j) in self.arcs:
            G.add_edge(i, j)

        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50)

        plt.figure(figsize=(14, 10))

        # Draw nodes by type
        supply_nodes = [n for n in G.nodes() if G.nodes[n].get('node_type') == 'supply']
        demand_nodes = [n for n in G.nodes() if G.nodes[n].get('node_type') == 'demand']
        trans_nodes = [n for n in G.nodes() if G.nodes[n].get('node_type') == 'transshipment']

        nx.draw_networkx_nodes(G, pos, nodelist=supply_nodes,
                             node_color='lightgreen', node_size=800,
                             label='Supply Nodes')
        nx.draw_networkx_nodes(G, pos, nodelist=demand_nodes,
                             node_color='lightcoral', node_size=800,
                             label='Demand Nodes')
        nx.draw_networkx_nodes(G, pos, nodelist=trans_nodes,
                             node_color='lightblue', node_size=800,
                             label='Transshipment')

        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.5, arrows=True,
                             arrowsize=20, width=2)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10)

        # If solution provided, highlight flows
        if solution and 'flows' in solution:
            edge_labels = {}
            for (i, j), flow in solution['flows'].items():
                cost = self.costs.get((i,j), 0)
                edge_labels[(i,j)] = f"{flow:.0f}\n${cost}"

            nx.draw_networkx_edge_labels(G, pos, edge_labels,
                                        font_size=8)

        plt.title("Network Flow Visualization")
        plt.legend()
        plt.axis('off')
        plt.tight_layout()
        plt.show()


# Complete example
if __name__ == "__main__":
    print("="*70)
    print("NETWORK FLOW OPTIMIZATION - COMPREHENSIVE EXAMPLE")
    print("="*70)

    # Create sample network
    nodes = ['S1', 'S2', 'DC1', 'DC2', 'DC3', 'D1', 'D2', 'D3']

    arcs = [
        ('S1', 'DC1'), ('S1', 'DC2'),
        ('S2', 'DC2'), ('S2', 'DC3'),
        ('DC1', 'D1'), ('DC1', 'D2'),
        ('DC2', 'D1'), ('DC2', 'D2'), ('DC2', 'D3'),
        ('DC3', 'D2'), ('DC3', 'D3')
    ]

    supplies = {
        'S1': 150, 'S2': 200,
        'DC1': 0, 'DC2': 0, 'DC3': 0,
        'D1': -100, 'D2': -120, 'D3': -130
    }

    costs = {}
    for (i,j) in arcs:
        costs[i,j] = np.random.uniform(8, 30)

    capacities = {}
    for (i,j) in arcs:
        capacities[i,j] = np.random.uniform(60, 150)

    # Create solver
    solver = NetworkFlowSolver()
    solver.load_min_cost_flow(nodes, arcs, supplies, costs, capacities)

    # Solve
    print("\n" + "="*70)
    print("SOLVING...")
    print("="*70)

    solution = solver.solve_exact()

    print(f"\n{'='*70}")
    print(f"OPTIMAL SOLUTION")
    print(f"{'='*70}")
    print(f"Status: {solution['status']}")
    print(f"Total Cost: ${solution['total_cost']:,.2f}")

    print(f"\nOptimal Flows:")
    for (i,j), flow in sorted(solution['flows'].items()):
        cost = costs[i,j]
        capacity = capacities[i,j]
        util = (flow / capacity) * 100
        print(f"  {i:4} → {j:4}: {flow:6.1f}/{capacity:6.1f} "
              f"({util:5.1f}%) @${cost:.2f}/unit")

    # Visualize
    solver.visualize_network(solution)
```

---

## Tools & Libraries

### Python Libraries
- **NetworkX**: Graph algorithms, flow optimization
- **PuLP/Pyomo**: MIP formulation
- **OR-Tools**: Google network optimization
- **SciPy**: Sparse matrix operations
- **igraph**: Fast network analysis

### Commercial Software
- **CPLEX/Gurobi**: High-performance solvers
- **AIMMS**: Optimization modeling
- **AMPL**: Mathematical modeling

---

## Common Challenges & Solutions

**Large Networks:** Use specialized algorithms (network simplex), decomposition

**Integer Flows:** Add integrality constraints, use branch-and-bound

**Time-Varying Demands:** Dynamic network flows, time-expanded networks

**Uncertainty:** Stochastic optimization, robust optimization

**Multiple Objectives:** Multi-objective optimization, weighted objectives

---

## Output Format

**Network Flow Solution:**
- Total Cost: $X
- Maximum Flow: Y units
- Arc Utilization: Z%
- Flow Pattern: [detailed routing]

---

## Questions to Ask

1. Network structure? (nodes, arcs, capacities)
2. Single or multi-commodity?
3. Supplies and demands?
4. Cost structure?
5. Capacity constraints?
6. Time dimension?
7. Optimization objective?

---

## Related Skills

- **facility-location-problem**: Location decisions with flows
- **distribution-center-network**: Multi-echelon networks
- **vehicle-routing-problem**: Routing after flow allocation
- **inventory-routing-problem**: Integrated inventory-flow
- **optimization-modeling**: MIP formulation
- **hub-location-problem**: Hub-based flow networks
