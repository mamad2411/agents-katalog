---
name: multi-objective-optimization
description: When the user wants to optimize multiple conflicting objectives, find Pareto-optimal solutions, or balance trade-offs between cost, service, quality, and sustainability. Also use when the user mentions "multi-objective," "Pareto optimization," "NSGA-II," "trade-off analysis," "scalarization," "weighted objectives," "goal programming," or "multiple criteria optimization." For single objective, see optimization-modeling.
---

# Multi-Objective Optimization

You are an expert in multi-objective optimization for supply chain. Your goal is to help find and analyze Pareto-optimal solutions that balance conflicting objectives like cost vs service, profit vs sustainability, or efficiency vs resilience.

## Initial Assessment

1. **Objectives**: What are competing goals? (minimize cost, maximize service, minimize carbon)
2. **Preferences**: Known trade-offs or discover Pareto frontier?
3. **Decision Maker**: Interactive or automated selection?
4. **Problem Size**: Solvable with exact methods or need heuristics?

---

## Core Concepts

**Pareto Dominance:** Solution x dominates y if x is better in all objectives

**Pareto Front:** Set of non-dominated solutions

**Trade-off:** Improving one objective worsens another

---

## Methods

### 1. Weighted Sum (Scalarization)

```python
# Combine objectives with weights
objective = w1 * cost + w2 * (-service_level) + w3 * carbon

# Vary weights to get different Pareto points
for w1 in [0.2, 0.5, 0.8]:
    w2, w3 = (1-w1)/2, (1-w1)/2
    solve_with_weights(w1, w2, w3)
```

### 2. ε-Constraint Method

```python
# Optimize one objective, constrain others
minimize cost
subject to:
    service_level ≥ 0.95
    carbon ≤ 1000
```

### 3. NSGA-II (Genetic Algorithm)

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.problems import get_problem

# Multi-objective problem
problem = SupplyChainMO()

algorithm = NSGA2(pop_size=100)

res = minimize(problem,
               algorithm,
               ('n_gen', 200),
               verbose=True)

# Get Pareto front
pareto_front = res.F
```

### 4. Goal Programming

```python
# Set target for each objective, minimize deviations
targets = {'cost': 100000, 'service': 0.98, 'carbon': 500}

minimize sum(d_minus[obj] + d_plus[obj] for obj in objectives)
subject to:
    actual[obj] + d_plus[obj] - d_minus[obj] = targets[obj]
```

---

## Supply Chain Network Design: Cost vs Service

```python
from pulp import *
import numpy as np
import matplotlib.pyplot as plt

def multi_objective_network_design(customers, facilities, weights):
    """
    Network design with cost and service objectives
    
    Objective 1: Minimize total cost
    Objective 2: Minimize average distance (maximize service)
    """
    
    model = LpProblem("MultiObj_Network", LpMinimize)
    
    # Variables
    open_facility = LpVariable.dicts("Open", facilities, cat='Binary')
    flow = LpVariable.dicts("Flow",
                           [(i,j) for i in customers for j in facilities],
                           lowBound=0)
    
    # Objective: weighted combination
    w_cost, w_service = weights
    
    cost_obj = lpSum([fixed_cost[j] * open_facility[j] for j in facilities]) + \
               lpSum([transport_cost[i,j] * flow[i,j]
                     for i in customers for j in facilities])
    
    service_obj = lpSum([distance[i,j] * flow[i,j]
                        for i in customers for j in facilities])
    
    # Normalize objectives
    max_cost = estimate_max_cost()
    max_distance = estimate_max_distance()
    
    model += w_cost * (cost_obj / max_cost) + \
             w_service * (service_obj / max_distance), "Weighted_Objective"
    
    # Constraints
    for i in customers:
        model += lpSum([flow[i,j] for j in facilities]) >= demand[i]
    
    for j in facilities:
        model += lpSum([flow[i,j] for i in customers]) <= \
                 capacity[j] * open_facility[j]
    
    model.solve()
    
    return {
        'cost': value(cost_obj),
        'service': value(service_obj),
        'open_facilities': [j for j in facilities if open_facility[j].varValue > 0.5]
    }

# Generate Pareto frontier
pareto_solutions = []
for w_cost in np.linspace(0, 1, 20):
    w_service = 1 - w_cost
    sol = multi_objective_network_design(customers, facilities, (w_cost, w_service))
    pareto_solutions.append(sol)

# Plot Pareto front
costs = [s['cost'] for s in pareto_solutions]
services = [s['service'] for s in pareto_solutions]

plt.figure(figsize=(10, 6))
plt.plot(costs, services, 'o-', linewidth=2, markersize=8)
plt.xlabel('Total Cost ($)')
plt.ylabel('Average Distance (Service)')
plt.title('Pareto Frontier: Cost vs Service Trade-off')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## Sustainable Supply Chain: Economic-Environmental-Social

```python
class TripleBottomLineOptimization:
    """
    Optimize Economic, Environmental, and Social objectives
    """
    
    def __init__(self, network_data):
        self.data = network_data
    
    def optimize_pareto(self, method='weighted_sum'):
        """
        Find Pareto-optimal solutions for triple bottom line
        
        Objectives:
        1. Economic: Minimize cost
        2. Environmental: Minimize carbon emissions
        3. Social: Maximize local employment
        """
        
        if method == 'weighted_sum':
            solutions = []
            
            # Systematically vary weights
            for w1 in [0.2, 0.4, 0.6, 0.8]:
                for w2 in [0.2, 0.4, 0.6, 0.8]:
                    w3 = max(0, 1 - w1 - w2)
                    if w1 + w2 + w3 > 0.99:  # Valid weight combination
                        sol = self.solve_weighted(w1, w2, w3)
                        solutions.append(sol)
            
            # Filter non-dominated solutions
            pareto_front = self.extract_pareto_front(solutions)
            return pareto_front
        
        elif method == 'epsilon_constraint':
            # Fix two objectives, optimize third
            pareto_front = []
            
            for carbon_limit in np.linspace(min_carbon, max_carbon, 10):
                for employment_target in np.linspace(min_emp, max_emp, 10):
                    sol = self.solve_epsilon_constraint(
                        carbon_limit=carbon_limit,
                        employment_target=employment_target
                    )
                    if sol['feasible']:
                        pareto_front.append(sol)
            
            return pareto_front
    
    def solve_weighted(self, w_economic, w_environmental, w_social):
        """Solve with weighted objectives"""
        
        model = LpProblem("Triple_Bottom_Line", LpMinimize)
        
        # Variables and constraints
        # ...
        
        # Weighted objective
        model += (
            w_economic * economic_cost +
            w_environmental * carbon_emissions +
            w_social * (-local_employment)  # Maximize employment
        )
        
        model.solve()
        
        return {
            'economic': value(economic_cost),
            'environmental': value(carbon_emissions),
            'social': value(local_employment),
            'weights': (w_economic, w_environmental, w_social)
        }
    
    def extract_pareto_front(self, solutions):
        """Filter non-dominated solutions"""
        
        pareto = []
        
        for sol in solutions:
            dominated = False
            
            for other in solutions:
                if self.dominates(other, sol):
                    dominated = True
                    break
            
            if not dominated:
                pareto.append(sol)
        
        return pareto
    
    def dominates(self, sol1, sol2):
        """Check if sol1 Pareto-dominates sol2"""
        
        # sol1 dominates if better in all objectives
        better_economic = sol1['economic'] <= sol2['economic']
        better_environmental = sol1['environmental'] <= sol2['environmental']
        better_social = sol1['social'] >= sol2['social']  # Maximize
        
        at_least_one_strictly_better = (
            sol1['economic'] < sol2['economic'] or
            sol1['environmental'] < sol2['environmental'] or
            sol1['social'] > sol2['social']
        )
        
        return (better_economic and better_environmental and better_social and
                at_least_one_strictly_better)
```

---

## Interactive Decision-Making

```python
def interactive_pareto_exploration(problem, decision_maker):
    """
    Interactive method: present solutions, get feedback, refine
    """
    
    # Generate initial Pareto front
    pareto_front = problem.generate_initial_pareto_front()
    
    iteration = 0
    max_iterations = 10
    
    while iteration < max_iterations:
        # Present solutions to decision maker
        print(f"\nIteration {iteration + 1}")
        print("Current Pareto Solutions:")
        for i, sol in enumerate(pareto_front):
            print(f"  {i}: Cost=${sol['cost']}, Service={sol['service']:.2%}, Carbon={sol['carbon']}")
        
        # Get feedback
        preferred_region = decision_maker.get_preference(pareto_front)
        
        if decision_maker.is_satisfied():
            break
        
        # Generate more solutions in preferred region
        new_solutions = problem.explore_region(preferred_region, n_solutions=10)
        pareto_front.extend(new_solutions)
        
        # Update Pareto front
        pareto_front = filter_non_dominated(pareto_front)
        
        iteration += 1
    
    # Final selection
    best_solution = decision_maker.select_final_solution(pareto_front)
    return best_solution
```

---

## Visualization

```python
def visualize_3d_pareto_front(solutions):
    """
    Visualize 3-objective Pareto front
    """
    
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    costs = [s['cost'] for s in solutions]
    services = [s['service'] for s in solutions]
    carbons = [s['carbon'] for s in solutions]
    
    scatter = ax.scatter(costs, services, carbons,
                        c=carbons, cmap='RdYlGn_r',
                        s=100, alpha=0.6, edgecolors='black')
    
    ax.set_xlabel('Cost ($)', fontsize=12)
    ax.set_ylabel('Service Level', fontsize=12)
    ax.set_zlabel('Carbon Emissions (tons)', fontsize=12)
    ax.set_title('3D Pareto Frontier', fontsize=14, fontweight='bold')
    
    plt.colorbar(scatter, label='Carbon Emissions')
    plt.show()

def visualize_parallel_coordinates(pareto_front):
    """
    Parallel coordinates plot for many objectives
    """
    
    from pandas.plotting import parallel_coordinates
    import pandas as pd
    
    df = pd.DataFrame(pareto_front)
    df['Solution'] = range(len(df))
    
    plt.figure(figsize=(12, 6))
    parallel_coordinates(df, 'Solution', colormap='viridis')
    plt.title('Pareto Solutions - Parallel Coordinates')
    plt.ylabel('Normalized Objective Value')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.show()
```

---

## Tools & Libraries

**Python:**
- `pymoo`: Multi-objective optimization
- `platypus`: Evolutionary multi-objective
- `jmetal`: Multi-objective metaheuristics

**Commercial:**
- `modeFRONTIER`: Multi-objective design
- `CPLEX Multi-Objective`

---

## Related Skills

- **optimization-modeling**: single-objective optimization
- **metaheuristic-optimization**: NSGA-II, MOEA
- **sustainable-sourcing**: environmental objectives
- **network-design**: multi-objective network design
