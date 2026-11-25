---
name: traveling-salesman-problem
description: When the user wants to solve the Traveling Salesman Problem (TSP), find the shortest route visiting all cities, or optimize tour sequences. Also use when the user mentions "TSP," "shortest tour," "Hamiltonian cycle," "tour optimization," "route sequencing," "optimal visit order," "traveling salesperson," or "minimum distance tour." For vehicle routing with capacities, see vehicle-routing-problem.
---

# Traveling Salesman Problem (TSP)

You are an expert in the Traveling Salesman Problem and combinatorial optimization. Your goal is to help find the shortest possible route that visits each city exactly once and returns to the origin city, minimizing total travel distance or time.

## Initial Assessment

Before solving TSP instances, understand:

1. **Problem Characteristics**
   - How many cities/locations need to be visited?
   - Symmetric TSP (distance i→j = distance j→i) or asymmetric?
   - What metric? (Euclidean distance, travel time, cost)
   - Any special constraints? (time windows → see vrp-time-windows)

2. **Problem Scale**
   - Small (< 20 cities): Exact methods feasible
   - Medium (20-100 cities): Advanced exact or good heuristics
   - Large (100-1000 cities): Metaheuristics required
   - Very large (> 1000 cities): Specialized algorithms

3. **Solution Requirements**
   - Need proven optimal solution?
   - Acceptable optimality gap? (e.g., within 5% of optimal)
   - Time constraint for solution?
   - Single tour or multiple tours needed?

4. **Data Format**
   - Coordinates (lat/lon, x/y)?
   - Distance matrix provided?
   - Need to calculate distances?
   - Real road network or Euclidean?

---

## Mathematical Formulation

### Classic TSP Formulation (MTZ)

**Decision Variables:**
- x_{ij} ∈ {0,1}: 1 if arc (i,j) is in tour, 0 otherwise
- u_i ∈ ℝ: Position of city i in tour (subtour elimination)

**Parameters:**
- c_{ij}: Cost/distance from city i to city j
- n: Number of cities

**Objective Function:**
```
Minimize: Σ_{i=1}^n Σ_{j=1}^n c_{ij} * x_{ij}
```

**Constraints:**
```
1. Each city has exactly one outgoing arc:
   Σ_{j=1}^n x_{ij} = 1,  ∀i

2. Each city has exactly one incoming arc:
   Σ_{i=1}^n x_{ij} = 1,  ∀j

3. Subtour elimination (Miller-Tucker-Zemlin):
   u_i - u_j + n*x_{ij} ≤ n-1,  ∀i,j ∈ {2,...,n}, i≠j

4. Variable bounds:
   x_{ij} ∈ {0,1}
   2 ≤ u_i ≤ n,  ∀i ∈ {2,...,n}
```

### Alternative: DFJ (Dantzig-Fulkerson-Johnson) Formulation

**Subtour Elimination Constraints:**
```
Σ_{i∈S} Σ_{j∈S} x_{ij} ≤ |S| - 1,  ∀S ⊂ V, 2 ≤ |S| ≤ n-1
```

This formulation has exponentially many constraints but produces tighter LP relaxations.

---

## Exact Algorithms

### 1. Branch-and-Bound with Dynamic Programming

```python
import numpy as np
from itertools import combinations

def tsp_dynamic_programming(dist_matrix):
    """
    Held-Karp algorithm for TSP using dynamic programming

    Time complexity: O(n^2 * 2^n)
    Space complexity: O(n * 2^n)

    Optimal for small instances (n ≤ 20)

    Args:
        dist_matrix: n x n distance matrix

    Returns:
        tuple: (optimal_cost, optimal_tour)
    """
    n = len(dist_matrix)

    # C[S][i] = minimum cost path visiting all nodes in S ending at i
    C = {}

    # Initialize: paths of length 1
    for i in range(1, n):
        C[(1 << i, i)] = (dist_matrix[0][i], 0)

    # Iterate over subset sizes
    for subset_size in range(2, n):
        # Generate all subsets of size subset_size
        for subset in combinations(range(1, n), subset_size):
            # Convert to bitmask
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find minimum cost to reach each node in subset
            for i in subset:
                # Previous subset without node i
                prev_bits = bits & ~(1 << i)

                min_cost = float('inf')
                min_prev = None

                # Try all possible previous nodes
                for j in subset:
                    if j == i:
                        continue

                    if (prev_bits, j) in C:
                        cost = C[(prev_bits, j)][0] + dist_matrix[j][i]
                        if cost < min_cost:
                            min_cost = cost
                            min_prev = j

                if min_prev is not None:
                    C[(bits, i)] = (min_cost, min_prev)

    # Find optimal tour
    bits = (1 << n) - 2  # All nodes except 0
    min_cost = float('inf')
    last_node = None

    for i in range(1, n):
        if (bits, i) in C:
            cost = C[(bits, i)][0] + dist_matrix[i][0]
            if cost < min_cost:
                min_cost = cost
                last_node = i

    # Reconstruct tour
    tour = [0]
    bits = (1 << n) - 2

    while last_node is not None:
        tour.append(last_node)
        prev_bits = bits & ~(1 << last_node)

        if (bits, last_node) in C:
            last_node = C[(bits, last_node)][1]
            bits = prev_bits
        else:
            break

    tour.append(0)

    return min_cost, tour


# Example usage
if __name__ == "__main__":
    # Small 5-city example
    dist_matrix = np.array([
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 30],
        [15, 35, 0, 30, 20],
        [20, 25, 30, 0, 15],
        [25, 30, 20, 15, 0]
    ])

    optimal_cost, optimal_tour = tsp_dynamic_programming(dist_matrix)
    print(f"Optimal Cost: {optimal_cost}")
    print(f"Optimal Tour: {optimal_tour}")
```

### 2. MIP Formulation with PuLP

```python
from pulp import *
import numpy as np

def tsp_mip_mtz(dist_matrix, city_names=None):
    """
    TSP using Miller-Tucker-Zemlin formulation

    Suitable for medium-sized instances (up to 50-100 cities)

    Args:
        dist_matrix: n x n distance matrix
        city_names: optional list of city names

    Returns:
        dict with optimal_cost, tour, and solve_time
    """
    n = len(dist_matrix)

    if city_names is None:
        city_names = [f"City_{i}" for i in range(n)]

    # Create problem
    prob = LpProblem("TSP_MTZ", LpMinimize)

    # Decision variables
    # x[i,j] = 1 if arc from city i to city j is in tour
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i,j] = LpVariable(f"x_{i}_{j}", cat='Binary')

    # u[i] = position of city i in tour (for subtour elimination)
    u = {}
    for i in range(1, n):
        u[i] = LpVariable(f"u_{i}", lowBound=1, upBound=n-1, cat='Continuous')

    # Objective: Minimize total distance
    prob += lpSum([dist_matrix[i][j] * x[i,j]
                   for i in range(n) for j in range(n) if i != j]), \
            "Total_Distance"

    # Constraints

    # 1. Each city has exactly one outgoing arc
    for i in range(n):
        prob += lpSum([x[i,j] for j in range(n) if j != i]) == 1, \
                f"Out_{i}"

    # 2. Each city has exactly one incoming arc
    for j in range(n):
        prob += lpSum([x[i,j] for i in range(n) if i != j]) == 1, \
                f"In_{j}"

    # 3. Miller-Tucker-Zemlin subtour elimination
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                prob += u[i] - u[j] + n*x[i,j] <= n-1, \
                        f"MTZ_{i}_{j}"

    # Solve
    import time
    start_time = time.time()
    prob.solve(PULP_CBC_CMD(msg=1, timeLimit=300))
    solve_time = time.time() - start_time

    # Extract solution
    if LpStatus[prob.status] == 'Optimal':
        tour = [0]
        current_city = 0

        for _ in range(n-1):
            for j in range(n):
                if j != current_city and x[current_city,j].varValue > 0.5:
                    tour.append(j)
                    current_city = j
                    break

        tour.append(0)  # Return to start

        return {
            'status': 'Optimal',
            'optimal_cost': value(prob.objective),
            'tour': tour,
            'tour_names': [city_names[i] for i in tour],
            'solve_time': solve_time
        }
    else:
        return {
            'status': LpStatus[prob.status],
            'optimal_cost': None,
            'tour': None,
            'solve_time': solve_time
        }


# Example usage
dist_matrix = np.array([
    [0, 29, 20, 21, 16, 31],
    [29, 0, 15, 29, 28, 40],
    [20, 15, 0, 15, 14, 25],
    [21, 29, 15, 0, 4, 12],
    [16, 28, 14, 4, 0, 16],
    [31, 40, 25, 12, 16, 0]
])

city_names = ['Depot', 'Customer_A', 'Customer_B',
              'Customer_C', 'Customer_D', 'Customer_E']

result = tsp_mip_mtz(dist_matrix, city_names)
print(f"\nStatus: {result['status']}")
print(f"Optimal Cost: {result['optimal_cost']:.2f}")
print(f"Optimal Tour: {result['tour_names']}")
print(f"Solve Time: {result['solve_time']:.2f} seconds")
```

---

## Constructive Heuristics

### 1. Nearest Neighbor

```python
import numpy as np

def nearest_neighbor_tsp(dist_matrix, start_city=0):
    """
    Nearest Neighbor heuristic for TSP

    Time complexity: O(n^2)
    Quality: Typically within 25% of optimal

    Args:
        dist_matrix: n x n distance matrix
        start_city: starting city (default 0)

    Returns:
        tuple: (total_cost, tour)
    """
    n = len(dist_matrix)
    unvisited = set(range(n))
    tour = [start_city]
    unvisited.remove(start_city)

    current_city = start_city
    total_cost = 0

    while unvisited:
        # Find nearest unvisited city
        nearest_city = min(unvisited,
                          key=lambda city: dist_matrix[current_city][city])

        total_cost += dist_matrix[current_city][nearest_city]
        tour.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city

    # Return to start
    total_cost += dist_matrix[current_city][start_city]
    tour.append(start_city)

    return total_cost, tour


def multi_start_nearest_neighbor(dist_matrix, num_starts=None):
    """
    Run Nearest Neighbor from multiple starting cities
    and return best solution

    Args:
        dist_matrix: n x n distance matrix
        num_starts: number of different starts (default: all cities)

    Returns:
        tuple: (best_cost, best_tour)
    """
    n = len(dist_matrix)

    if num_starts is None:
        num_starts = n

    best_cost = float('inf')
    best_tour = None

    for start in range(min(num_starts, n)):
        cost, tour = nearest_neighbor_tsp(dist_matrix, start)

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_cost, best_tour
```

### 2. Cheapest Insertion

```python
def cheapest_insertion_tsp(dist_matrix):
    """
    Cheapest Insertion heuristic for TSP

    Time complexity: O(n^3)
    Quality: Generally better than Nearest Neighbor

    Args:
        dist_matrix: n x n distance matrix

    Returns:
        tuple: (total_cost, tour)
    """
    n = len(dist_matrix)

    # Start with smallest edge
    min_dist = float('inf')
    best_pair = (0, 1)

    for i in range(n):
        for j in range(i+1, n):
            if dist_matrix[i][j] < min_dist:
                min_dist = dist_matrix[i][j]
                best_pair = (i, j)

    # Initial tour
    tour = list(best_pair)
    unvisited = set(range(n)) - set(tour)

    # Insert remaining cities
    while unvisited:
        best_insertion = None
        best_cost_increase = float('inf')
        best_position = None

        # Try inserting each unvisited city
        for city in unvisited:
            # Try inserting between each pair of adjacent cities
            for i in range(len(tour)):
                j = (i + 1) % len(tour)

                # Cost increase of inserting city between tour[i] and tour[j]
                cost_increase = (dist_matrix[tour[i]][city] +
                               dist_matrix[city][tour[j]] -
                               dist_matrix[tour[i]][tour[j]])

                if cost_increase < best_cost_increase:
                    best_cost_increase = cost_increase
                    best_insertion = city
                    best_position = j

        # Insert best city
        tour.insert(best_position, best_insertion)
        unvisited.remove(best_insertion)

    # Calculate total cost
    total_cost = sum(dist_matrix[tour[i]][tour[(i+1)%len(tour)]]
                    for i in range(len(tour)))

    tour.append(tour[0])  # Close tour

    return total_cost, tour


def farthest_insertion_tsp(dist_matrix):
    """
    Farthest Insertion heuristic (variant)

    Similar to cheapest insertion but selects farthest city
    from tour at each step
    """
    n = len(dist_matrix)

    # Start with two farthest cities
    max_dist = 0
    best_pair = (0, 1)

    for i in range(n):
        for j in range(i+1, n):
            if dist_matrix[i][j] > max_dist:
                max_dist = dist_matrix[i][j]
                best_pair = (i, j)

    tour = list(best_pair)
    unvisited = set(range(n)) - set(tour)

    while unvisited:
        # Find farthest city from current tour
        farthest_city = None
        max_min_dist = 0

        for city in unvisited:
            min_dist_to_tour = min(dist_matrix[city][tour_city]
                                  for tour_city in tour)
            if min_dist_to_tour > max_min_dist:
                max_min_dist = min_dist_to_tour
                farthest_city = city

        # Find best insertion position
        best_position = 0
        best_cost_increase = float('inf')

        for i in range(len(tour)):
            j = (i + 1) % len(tour)
            cost_increase = (dist_matrix[tour[i]][farthest_city] +
                           dist_matrix[farthest_city][tour[j]] -
                           dist_matrix[tour[i]][tour[j]])

            if cost_increase < best_cost_increase:
                best_cost_increase = cost_increase
                best_position = j

        tour.insert(best_position, farthest_city)
        unvisited.remove(farthest_city)

    total_cost = sum(dist_matrix[tour[i]][tour[(i+1)%len(tour)]]
                    for i in range(len(tour)))
    tour.append(tour[0])

    return total_cost, tour
```

---

## Improvement Heuristics

### 1. 2-Opt Local Search

```python
def two_opt(tour, dist_matrix):
    """
    2-opt improvement heuristic

    Iteratively removes two edges and reconnects the tour
    in a different way if it improves the solution

    Args:
        tour: initial tour (list of city indices)
        dist_matrix: n x n distance matrix

    Returns:
        tuple: (improved_cost, improved_tour)
    """
    n = len(tour) - 1  # Exclude duplicate last city
    improved = True
    best_tour = tour[:-1]  # Remove last city (duplicate of first)

    while improved:
        improved = False

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # Current edges: (tour[i-1], tour[i]) and (tour[j], tour[j+1])
                # New edges: (tour[i-1], tour[j]) and (tour[i], tour[j+1])

                current_cost = (dist_matrix[best_tour[i-1]][best_tour[i]] +
                               dist_matrix[best_tour[j]][best_tour[(j+1)%n]])

                new_cost = (dist_matrix[best_tour[i-1]][best_tour[j]] +
                           dist_matrix[best_tour[i]][best_tour[(j+1)%n]])

                if new_cost < current_cost:
                    # Reverse the segment between i and j
                    best_tour[i:j+1] = reversed(best_tour[i:j+1])
                    improved = True
                    break

            if improved:
                break

    # Calculate total cost
    total_cost = sum(dist_matrix[best_tour[i]][best_tour[(i+1)%n]]
                    for i in range(n))
    total_cost += dist_matrix[best_tour[n-1]][best_tour[0]]

    best_tour.append(best_tour[0])  # Close tour

    return total_cost, best_tour


def two_opt_optimized(tour, dist_matrix, max_iterations=1000):
    """
    Optimized 2-opt with early stopping
    """
    n = len(tour) - 1
    best_tour = tour[:-1]

    def calculate_tour_cost(t):
        return sum(dist_matrix[t[i]][t[(i+1)%len(t)]] for i in range(len(t)))

    best_cost = calculate_tour_cost(best_tour)
    iterations = 0
    no_improvement_count = 0

    while iterations < max_iterations and no_improvement_count < 50:
        iterations += 1
        improved = False

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # Calculate delta (change in cost)
                delta = (dist_matrix[best_tour[i-1]][best_tour[j]] +
                        dist_matrix[best_tour[i]][best_tour[(j+1)%n]] -
                        dist_matrix[best_tour[i-1]][best_tour[i]] -
                        dist_matrix[best_tour[j]][best_tour[(j+1)%n]])

                if delta < -1e-10:  # Improvement found
                    best_tour[i:j+1] = reversed(best_tour[i:j+1])
                    best_cost += delta
                    improved = True
                    no_improvement_count = 0
                    break

            if improved:
                break

        if not improved:
            no_improvement_count += 1

    best_tour.append(best_tour[0])
    return best_cost, best_tour
```

### 2. 3-Opt Local Search

```python
def three_opt(tour, dist_matrix, max_iterations=100):
    """
    3-opt improvement heuristic

    More powerful than 2-opt but slower
    Considers removing 3 edges and reconnecting

    Args:
        tour: initial tour
        dist_matrix: n x n distance matrix
        max_iterations: maximum iterations

    Returns:
        tuple: (improved_cost, improved_tour)
    """
    n = len(tour) - 1
    best_tour = tour[:-1]

    def calculate_cost(t):
        return sum(dist_matrix[t[i]][t[(i+1)%len(t)]] for i in range(len(t)))

    best_cost = calculate_cost(best_tour)

    for iteration in range(max_iterations):
        improved = False

        for i in range(n - 2):
            for j in range(i + 2, n - 1):
                for k in range(j + 2, n):
                    # Try all possible 3-opt reconnections
                    # There are 8 ways to reconnect 3 segments

                    # Current tour segments: A-B-C where
                    # A = tour[0:i+1]
                    # B = tour[i+1:j+1]
                    # C = tour[j+1:k+1]
                    # D = tour[k+1:]

                    # Try different reconnections
                    segments = [
                        best_tour[:i+1],
                        best_tour[i+1:j+1],
                        best_tour[j+1:k+1],
                        best_tour[k+1:]
                    ]

                    # Case 1: A + reverse(B) + C + D
                    new_tour = segments[0] + segments[1][::-1] + segments[2] + segments[3]
                    new_cost = calculate_cost(new_tour)

                    if new_cost < best_cost:
                        best_tour = new_tour
                        best_cost = new_cost
                        improved = True
                        break

                if improved:
                    break

            if improved:
                break

        if not improved:
            break

    best_tour.append(best_tour[0])
    return best_cost, best_tour
```

### 3. Or-Opt

```python
def or_opt(tour, dist_matrix):
    """
    Or-opt improvement heuristic

    Relocates sequences of 1, 2, or 3 consecutive cities

    Args:
        tour: initial tour
        dist_matrix: n x n distance matrix

    Returns:
        tuple: (improved_cost, improved_tour)
    """
    n = len(tour) - 1
    best_tour = tour[:-1]
    improved = True

    def calculate_cost(t):
        return sum(dist_matrix[t[i]][t[(i+1)%len(t)]] for i in range(len(t)))

    best_cost = calculate_cost(best_tour)

    while improved:
        improved = False

        # Try relocating sequences of length 1, 2, and 3
        for seq_length in [1, 2, 3]:
            if seq_length >= n:
                continue

            for i in range(n):
                if i + seq_length > n:
                    continue

                # Extract sequence
                sequence = best_tour[i:i+seq_length]

                # Try inserting at all other positions
                for j in range(n):
                    if j >= i and j < i + seq_length:
                        continue

                    # Create new tour with sequence relocated
                    new_tour = best_tour[:i] + best_tour[i+seq_length:]
                    new_tour = new_tour[:j] + sequence + new_tour[j:]

                    new_cost = calculate_cost(new_tour)

                    if new_cost < best_cost - 1e-10:
                        best_tour = new_tour
                        best_cost = new_cost
                        improved = True
                        break

                if improved:
                    break

            if improved:
                break

    best_tour.append(best_tour[0])
    return best_cost, best_tour
```

---

## Metaheuristics

### 1. Simulated Annealing

```python
import random
import math

def simulated_annealing_tsp(dist_matrix, initial_temp=1000,
                           cooling_rate=0.995, max_iterations=10000):
    """
    Simulated Annealing for TSP

    Probabilistically accepts worse solutions to escape local optima

    Args:
        dist_matrix: n x n distance matrix
        initial_temp: starting temperature
        cooling_rate: temperature reduction factor
        max_iterations: maximum iterations

    Returns:
        tuple: (best_cost, best_tour)
    """
    n = len(dist_matrix)

    # Generate initial solution
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_tour.append(current_tour[0])

    def calculate_cost(tour):
        return sum(dist_matrix[tour[i]][tour[i+1]]
                  for i in range(len(tour)-1))

    current_cost = calculate_cost(current_tour)
    best_tour = current_tour.copy()
    best_cost = current_cost

    temperature = initial_temp

    for iteration in range(max_iterations):
        # Generate neighbor solution (2-opt move)
        i = random.randint(1, n - 2)
        j = random.randint(i + 1, n - 1)

        new_tour = current_tour.copy()
        new_tour[i:j+1] = reversed(new_tour[i:j+1])

        new_cost = calculate_cost(new_tour)
        delta = new_cost - current_cost

        # Accept or reject new solution
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_tour = new_tour
            current_cost = new_cost

            # Update best solution
            if current_cost < best_cost:
                best_tour = current_tour.copy()
                best_cost = current_cost

        # Cool down
        temperature *= cooling_rate

        if temperature < 0.01:
            break

    return best_cost, best_tour
```

### 2. Genetic Algorithm

```python
def genetic_algorithm_tsp(dist_matrix, population_size=100,
                         generations=500, mutation_rate=0.01):
    """
    Genetic Algorithm for TSP

    Uses order crossover (OX) and swap mutation

    Args:
        dist_matrix: n x n distance matrix
        population_size: number of individuals
        generations: number of generations
        mutation_rate: probability of mutation

    Returns:
        tuple: (best_cost, best_tour)
    """
    n = len(dist_matrix)

    def calculate_fitness(tour):
        cost = sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))
        return 1.0 / (1.0 + cost)  # Higher fitness = better tour

    def create_individual():
        tour = list(range(n))
        random.shuffle(tour)
        return tour

    def order_crossover(parent1, parent2):
        """Order crossover (OX)"""
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))

        child = [-1] * size
        child[start:end] = parent1[start:end]

        # Fill remaining positions from parent2
        pos = end
        for city in parent2[end:] + parent2[:end]:
            if city not in child:
                if pos >= size:
                    pos = 0
                child[pos] = city
                pos += 1

        return child

    def mutate(tour):
        """Swap mutation"""
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(tour)), 2)
            tour[i], tour[j] = tour[j], tour[i]
        return tour

    def tournament_selection(population, fitnesses, k=3):
        """Tournament selection"""
        selected = random.sample(list(zip(population, fitnesses)), k)
        return max(selected, key=lambda x: x[1])[0]

    # Initialize population
    population = [create_individual() for _ in range(population_size)]

    best_tour = None
    best_cost = float('inf')

    for generation in range(generations):
        # Calculate fitness
        fitnesses = [calculate_fitness(ind) for ind in population]

        # Track best
        for tour, fitness in zip(population, fitnesses):
            cost = sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))
            if cost < best_cost:
                best_cost = cost
                best_tour = tour.copy()

        # Create next generation
        new_population = []

        # Elitism: keep best individuals
        elite_count = int(0.1 * population_size)
        elite_indices = sorted(range(len(fitnesses)),
                              key=lambda i: fitnesses[i],
                              reverse=True)[:elite_count]
        new_population = [population[i].copy() for i in elite_indices]

        # Crossover and mutation
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            child = order_crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    best_tour.append(best_tour[0])
    return best_cost, best_tour
```

### 3. Ant Colony Optimization

```python
def ant_colony_optimization_tsp(dist_matrix, n_ants=20, n_iterations=100,
                                alpha=1.0, beta=2.0, evaporation=0.5, Q=100):
    """
    Ant Colony Optimization for TSP

    Args:
        dist_matrix: n x n distance matrix
        n_ants: number of ants
        n_iterations: number of iterations
        alpha: pheromone importance
        beta: distance importance
        evaporation: pheromone evaporation rate
        Q: pheromone deposit factor

    Returns:
        tuple: (best_cost, best_tour)
    """
    n = len(dist_matrix)

    # Initialize pheromone matrix
    pheromone = np.ones((n, n)) / n

    best_tour = None
    best_cost = float('inf')

    for iteration in range(n_iterations):
        all_tours = []
        all_costs = []

        # Each ant constructs a tour
        for ant in range(n_ants):
            tour = [0]  # Start from city 0
            unvisited = set(range(1, n))

            current_city = 0

            while unvisited:
                # Calculate probabilities for next city
                probabilities = []

                for city in unvisited:
                    tau = pheromone[current_city][city] ** alpha
                    eta = (1.0 / dist_matrix[current_city][city]) ** beta
                    probabilities.append(tau * eta)

                # Normalize probabilities
                total = sum(probabilities)
                probabilities = [p / total for p in probabilities]

                # Select next city
                next_city = np.random.choice(list(unvisited), p=probabilities)

                tour.append(next_city)
                unvisited.remove(next_city)
                current_city = next_city

            tour.append(0)  # Return to start

            # Calculate tour cost
            cost = sum(dist_matrix[tour[i]][tour[i+1]]
                      for i in range(len(tour)-1))

            all_tours.append(tour)
            all_costs.append(cost)

            # Update best solution
            if cost < best_cost:
                best_cost = cost
                best_tour = tour.copy()

        # Evaporate pheromone
        pheromone *= (1 - evaporation)

        # Deposit pheromone
        for tour, cost in zip(all_tours, all_costs):
            deposit = Q / cost

            for i in range(len(tour) - 1):
                city1, city2 = tour[i], tour[i+1]
                pheromone[city1][city2] += deposit
                pheromone[city2][city1] += deposit

    return best_cost, best_tour
```

---

## Using OR-Tools (Google Optimization)

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_tsp_ortools(dist_matrix, time_limit_seconds=30):
    """
    Solve TSP using Google OR-Tools

    Very efficient for practical instances

    Args:
        dist_matrix: n x n distance matrix
        time_limit_seconds: time limit for solver

    Returns:
        dict with solution details
    """
    n = len(dist_matrix)

    # Create routing index manager
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)

    # Create routing model
    routing = pywrapcp.RoutingModel(manager)

    # Create distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(dist_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = time_limit_seconds

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        tour = []
        index = routing.Start(0)

        while not routing.IsEnd(index):
            tour.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))

        tour.append(manager.IndexToNode(index))

        return {
            'status': 'Optimal' if solution.status == 1 else 'Feasible',
            'optimal_cost': solution.ObjectiveValue(),
            'tour': tour,
            'computation_time': routing.solver().WallTime() / 1000.0
        }
    else:
        return {
            'status': 'No solution found',
            'optimal_cost': None,
            'tour': None
        }


# Example: Solve TSP with coordinates
def solve_tsp_from_coordinates(coordinates, time_limit=30):
    """
    Solve TSP given (x, y) coordinates

    Args:
        coordinates: list of (x, y) tuples
        time_limit: time limit in seconds

    Returns:
        solution dictionary
    """
    import math

    n = len(coordinates)

    # Calculate Euclidean distance matrix
    dist_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                dx = coordinates[i][0] - coordinates[j][0]
                dy = coordinates[i][1] - coordinates[j][1]
                dist_matrix[i][j] = math.sqrt(dx*dx + dy*dy)

    return solve_tsp_ortools(dist_matrix, time_limit)


# Example usage
coordinates = [
    (0, 0),    # Depot
    (2, 4),    # City 1
    (5, 1),    # City 2
    (8, 3),    # City 3
    (6, 7),    # City 4
    (3, 6),    # City 5
    (7, 9),    # City 6
    (1, 8)     # City 7
]

result = solve_tsp_from_coordinates(coordinates)
print(f"Status: {result['status']}")
print(f"Optimal Cost: {result['optimal_cost']:.2f}")
print(f"Optimal Tour: {result['tour']}")
print(f"Computation Time: {result['computation_time']:.2f} seconds")
```

---

## Complete Solution Framework

```python
class TSPSolver:
    """
    Complete TSP solver with multiple algorithms
    """

    def __init__(self, dist_matrix, city_names=None):
        self.dist_matrix = np.array(dist_matrix)
        self.n = len(dist_matrix)

        if city_names is None:
            self.city_names = [f"City_{i}" for i in range(self.n)]
        else:
            self.city_names = city_names

    def solve(self, method='ortools', **kwargs):
        """
        Solve TSP using specified method

        Methods:
        - 'ortools': Google OR-Tools (recommended)
        - 'dynamic_programming': Exact (small instances only)
        - 'nearest_neighbor': Fast heuristic
        - 'cheapest_insertion': Good heuristic
        - '2opt': Local search improvement
        - 'simulated_annealing': Metaheuristic
        - 'genetic': Genetic algorithm
        - 'aco': Ant colony optimization
        """

        if method == 'ortools':
            result = solve_tsp_ortools(self.dist_matrix,
                                      kwargs.get('time_limit', 30))

        elif method == 'dynamic_programming':
            if self.n > 20:
                raise ValueError("Dynamic programming only for n ≤ 20")
            cost, tour = tsp_dynamic_programming(self.dist_matrix)
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Optimal'}

        elif method == 'nearest_neighbor':
            cost, tour = multi_start_nearest_neighbor(
                self.dist_matrix,
                kwargs.get('num_starts', self.n))
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Heuristic'}

        elif method == 'cheapest_insertion':
            cost, tour = cheapest_insertion_tsp(self.dist_matrix)
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Heuristic'}

        elif method == '2opt':
            # Need initial solution
            _, initial_tour = nearest_neighbor_tsp(self.dist_matrix)
            cost, tour = two_opt_optimized(initial_tour, self.dist_matrix)
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Local Search'}

        elif method == 'simulated_annealing':
            cost, tour = simulated_annealing_tsp(
                self.dist_matrix,
                kwargs.get('initial_temp', 1000),
                kwargs.get('cooling_rate', 0.995),
                kwargs.get('max_iterations', 10000))
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Metaheuristic'}

        elif method == 'genetic':
            cost, tour = genetic_algorithm_tsp(
                self.dist_matrix,
                kwargs.get('population_size', 100),
                kwargs.get('generations', 500),
                kwargs.get('mutation_rate', 0.01))
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Metaheuristic'}

        elif method == 'aco':
            cost, tour = ant_colony_optimization_tsp(
                self.dist_matrix,
                kwargs.get('n_ants', 20),
                kwargs.get('n_iterations', 100))
            result = {'optimal_cost': cost, 'tour': tour, 'status': 'Metaheuristic'}

        else:
            raise ValueError(f"Unknown method: {method}")

        # Add city names to result
        if result['tour']:
            result['tour_names'] = [self.city_names[i] for i in result['tour']]

        return result

    def compare_methods(self, methods=['nearest_neighbor', 'cheapest_insertion',
                                      '2opt', 'ortools']):
        """
        Compare multiple solution methods
        """
        import time

        results = []

        for method in methods:
            print(f"Solving with {method}...")
            start_time = time.time()

            try:
                result = self.solve(method)
                solve_time = time.time() - start_time

                results.append({
                    'method': method,
                    'cost': result['optimal_cost'],
                    'tour': result['tour'],
                    'status': result['status'],
                    'time': solve_time
                })
            except Exception as e:
                print(f"  Error: {e}")

        # Create comparison dataframe
        import pandas as pd
        df = pd.DataFrame([{
            'Method': r['method'],
            'Cost': r['cost'],
            'Status': r['status'],
            'Time (s)': f"{r['time']:.3f}"
        } for r in results])

        # Add % from best
        best_cost = df['Cost'].min()
        df['Gap %'] = ((df['Cost'] - best_cost) / best_cost * 100).round(2)

        return df


# Example usage
if __name__ == "__main__":
    # Example distance matrix
    dist_matrix = [
        [0, 29, 20, 21, 16, 31, 100],
        [29, 0, 15, 29, 28, 40, 72],
        [20, 15, 0, 15, 14, 25, 81],
        [21, 29, 15, 0, 4, 12, 92],
        [16, 28, 14, 4, 0, 16, 94],
        [31, 40, 25, 12, 16, 0, 95],
        [100, 72, 81, 92, 94, 95, 0]
    ]

    city_names = ['Depot', 'Customer A', 'Customer B', 'Customer C',
                  'Customer D', 'Customer E', 'Customer F']

    solver = TSPSolver(dist_matrix, city_names)

    # Solve with OR-Tools
    result = solver.solve('ortools', time_limit=10)
    print(f"\nOR-Tools Solution:")
    print(f"Cost: {result['optimal_cost']:.2f}")
    print(f"Tour: {' → '.join(result['tour_names'])}")

    # Compare methods
    print("\n" + "="*60)
    print("Comparing Methods:")
    print("="*60)
    comparison = solver.compare_methods()
    print(comparison.to_string(index=False))
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- **OR-Tools (Google)**: Industrial-strength routing solver
- **PuLP**: MIP modeling
- **Pyomo**: Advanced optimization modeling
- **NetworkX**: Graph algorithms
- **python-tsp**: Specialized TSP library

**Heuristics:**
- **scikit-opt**: Genetic algorithms, simulated annealing
- **pymoo**: Multi-objective optimization

**Visualization:**
- **matplotlib**: Basic plotting
- **plotly**: Interactive visualizations
- **folium**: Map-based visualization

### Commercial Solvers

- **Gurobi**: State-of-art MIP solver
- **CPLEX**: IBM optimization solver
- **Concorde**: Best exact TSP solver (specialized)

### Online Tools

- **TSPLIB**: Standard benchmark instances
- **Concorde TSP Solver**: Free online solver
- **NEOS Server**: Remote optimization server

---

## Common Challenges & Solutions

### Challenge: Problem Too Large for Exact Methods

**Problem:**
- 100+ cities makes exact methods impractical
- Need good solutions quickly

**Solutions:**
- Use OR-Tools with time limits
- Multi-start nearest neighbor + 2-opt
- Metaheuristics (SA, GA, ACO)
- Problem decomposition (cluster first, route second)

### Challenge: Asymmetric TSP

**Problem:**
- Distance i→j ≠ distance j→i (e.g., one-way streets)
- Different formulation needed

**Solutions:**
- Modify MTZ formulation for asymmetric case
- OR-Tools handles asymmetric naturally
- Heuristics adapt easily

### Challenge: Real-World Constraints

**Problem:**
- Time windows, capacities, multiple vehicles
- Pure TSP insufficient

**Solutions:**
- See **vrp-time-windows** for time constraints
- See **vehicle-routing-problem** for capacities
- See **multi-depot-vrp** for multiple depots

### Challenge: Dynamic TSP

**Problem:**
- New customers arrive during execution
- Need to reoptimize

**Solutions:**
- Use fast heuristics (nearest neighbor, insertion)
- Implement re-optimization triggers
- Keep partial tours feasible

---

## Output Format

### TSP Solution Report

**Problem Summary:**
- Number of cities: 25
- Distance metric: Euclidean
- Solution method: OR-Tools with Guided Local Search
- Computation time: 2.3 seconds

**Solution Quality:**

| Metric | Value |
|--------|-------|
| Total Distance | 427.85 km |
| Number of Cities | 25 |
| Solution Status | Optimal |
| Optimality Gap | 0% |

**Optimal Tour:**
```
Depot → City_A → City_F → City_C → ... → City_Z → Depot
```

**Tour Visualization:**
[Map or graph showing tour]

**Statistics:**
- Average distance between consecutive cities: 17.1 km
- Longest leg: City_A → City_B (45.2 km)
- Shortest leg: City_F → City_G (3.8 km)

---

## Questions to Ask

If you need more context:
1. How many cities/locations need to be visited?
2. Do you have coordinates or a distance matrix?
3. Is distance symmetric (i→j = j→i)?
4. Do you need the proven optimal solution or is a good solution acceptable?
5. What's the acceptable computation time?
6. Are there any additional constraints (time windows, capacities)?
7. Is this a one-time solve or recurring problem?
8. Do you have access to commercial solvers (Gurobi, CPLEX)?

---

## Related Skills

- **vehicle-routing-problem**: For multiple vehicles with capacities
- **vrp-time-windows**: For TSP with time constraints
- **pickup-delivery-problem**: For pickup and delivery pairs
- **route-optimization**: For practical routing applications
- **network-flow-optimization**: For underlying graph theory
- **metaheuristic-optimization**: For advanced solution methods
- **optimization-modeling**: For general MIP formulation
