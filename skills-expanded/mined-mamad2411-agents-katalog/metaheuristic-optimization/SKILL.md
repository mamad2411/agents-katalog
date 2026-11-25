---
name: metaheuristic-optimization
description: When the user wants to solve complex optimization problems using metaheuristics, apply genetic algorithms, simulated annealing, or other nature-inspired algorithms. Also use when the user mentions "genetic algorithm," "simulated annealing," "tabu search," "ant colony," "particle swarm," "evolutionary algorithms," "nature-inspired optimization," "heuristic search," or when exact optimization methods are too slow for large-scale problems. For exact methods, see optimization-modeling. For multi-objective, see multi-objective-optimization.
---

# Metaheuristic Optimization

You are an expert in metaheuristic optimization algorithms for supply chain. Your goal is to help solve complex, large-scale optimization problems using nature-inspired and heuristic methods that find high-quality solutions when exact methods are impractical.

## Initial Assessment

Before applying metaheuristics, understand:

1. **Problem Characteristics**
   - What decisions need optimization? (routing, scheduling, allocation)
   - Problem size? (variables, constraints)
   - Why not exact methods? (too slow, too large, NP-hard)
   - Solution quality needed? (optimal vs. good-enough)

2. **Problem Structure**
   - Discrete or continuous decision variables?
   - Constraints: hard (must satisfy) vs. soft (penalties)?
   - Objective: single or multiple objectives?
   - Problem landscape: smooth, rugged, multimodal?

3. **Computational Resources**
   - Available time for optimization? (seconds, minutes, hours)
   - Parallel computing available?
   - Real-time vs. offline optimization?
   - Memory constraints?

4. **Current Approach**
   - Existing heuristics or rules in use?
   - Baseline performance to beat?
   - Known good solutions?
   - Domain-specific knowledge to leverage?

---

## Metaheuristic Algorithm Types

### Population-Based Methods

**Characteristics:**
- Maintain multiple candidate solutions
- Explore solution space broadly
- Good for multimodal problems
- Examples: Genetic Algorithms, Particle Swarm

**Advantages:**
- Less likely to get stuck in local optima
- Can leverage parallelization
- Diverse solution pool

**Disadvantages:**
- Slower convergence
- More computational overhead
- More parameters to tune

### Trajectory-Based Methods

**Characteristics:**
- Single solution improved iteratively
- Intensive local search
- Memory of past solutions
- Examples: Simulated Annealing, Tabu Search

**Advantages:**
- Faster convergence
- Less memory usage
- Simpler implementation

**Disadvantages:**
- Can get trapped in local optima
- Less exploration
- Sequential execution

---

## Genetic Algorithms (GA)

### Core Concepts

**Evolutionary Process:**
1. **Population**: Set of candidate solutions (chromosomes)
2. **Selection**: Choose parents based on fitness
3. **Crossover**: Combine parents to create offspring
4. **Mutation**: Random changes to maintain diversity
5. **Replacement**: New generation replaces old

### GA for Vehicle Routing Problem

```python
import numpy as np
import random
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

class GeneticAlgorithmVRP:
    """
    Genetic Algorithm for Vehicle Routing Problem

    Problem: Optimize routes for multiple vehicles serving customers
    Objective: Minimize total distance while respecting capacity constraints
    """

    def __init__(self,
                 customers: List[Tuple[float, float]],
                 demands: List[float],
                 depot: Tuple[float, float] = (0, 0),
                 vehicle_capacity: float = 100,
                 num_vehicles: int = 5,
                 population_size: int = 100,
                 generations: int = 500,
                 mutation_rate: float = 0.15,
                 crossover_rate: float = 0.8,
                 elite_size: int = 20):
        """
        Initialize GA for VRP

        customers: list of (x, y) coordinates
        demands: customer demands
        depot: depot location
        vehicle_capacity: max capacity per vehicle
        """

        self.customers = customers
        self.demands = demands
        self.depot = depot
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        self.n_customers = len(customers)

        # GA parameters
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size

        # Distance matrix
        self.distance_matrix = self._calculate_distance_matrix()

        # Results
        self.best_solution = None
        self.best_fitness = float('inf')
        self.fitness_history = []

    def _calculate_distance_matrix(self) -> np.ndarray:
        """Calculate distances between all locations"""

        all_locations = [self.depot] + self.customers
        n = len(all_locations)
        distances = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                if i != j:
                    x1, y1 = all_locations[i]
                    x2, y2 = all_locations[j]
                    distances[i][j] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        return distances

    def _create_chromosome(self) -> List[int]:
        """
        Create random chromosome (solution)

        Chromosome: permutation of customer indices with vehicle separators
        Example: [3, 1, -1, 5, 2, 4, -1, 6, 7]
        -1 represents return to depot (vehicle separation)
        """

        # Random permutation of customers
        customers_perm = list(range(1, self.n_customers + 1))
        random.shuffle(customers_perm)

        # Insert vehicle separators randomly
        chromosome = []
        customers_per_vehicle = self.n_customers // self.num_vehicles

        for i, customer in enumerate(customers_perm):
            chromosome.append(customer)
            # Add separator every few customers (not at end)
            if ((i + 1) % customers_per_vehicle == 0 and
                i < len(customers_perm) - 1):
                chromosome.append(-1)

        return chromosome

    def _decode_chromosome(self, chromosome: List[int]) -> List[List[int]]:
        """
        Decode chromosome into routes

        Returns: list of routes, each route is list of customer indices
        """

        routes = []
        current_route = []

        for gene in chromosome:
            if gene == -1:
                if current_route:
                    routes.append(current_route)
                    current_route = []
            else:
                current_route.append(gene)

        # Add last route
        if current_route:
            routes.append(current_route)

        return routes

    def _calculate_fitness(self, chromosome: List[int]) -> float:
        """
        Calculate fitness (total distance + penalties)

        Lower is better
        """

        routes = self._decode_chromosome(chromosome)
        total_distance = 0
        penalty = 0

        for route in routes:
            if not route:
                continue

            # Check capacity constraint
            route_demand = sum(self.demands[c - 1] for c in route)
            if route_demand > self.vehicle_capacity:
                penalty += (route_demand - self.vehicle_capacity) * 1000

            # Calculate route distance: depot -> customers -> depot
            route_distance = self.distance_matrix[0, route[0]]  # Depot to first

            for i in range(len(route) - 1):
                route_distance += self.distance_matrix[route[i], route[i + 1]]

            route_distance += self.distance_matrix[route[-1], 0]  # Last to depot

            total_distance += route_distance

        return total_distance + penalty

    def _initialize_population(self) -> List[List[int]]:
        """Create initial population"""

        population = []
        for _ in range(self.population_size):
            chromosome = self._create_chromosome()
            population.append(chromosome)

        return population

    def _selection(self, population: List[List[int]],
                   fitness_scores: List[float]) -> List[List[int]]:
        """
        Tournament selection

        Select parents for breeding using tournament selection
        """

        selected = []

        for _ in range(len(population) - self.elite_size):
            # Tournament of size 3
            tournament_idx = random.sample(range(len(population)), 3)
            tournament_fitness = [fitness_scores[i] for i in tournament_idx]
            winner_idx = tournament_idx[np.argmin(tournament_fitness)]
            selected.append(population[winner_idx])

        return selected

    def _crossover(self, parent1: List[int],
                   parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Order Crossover (OX) for permutation-based chromosomes

        Preserves order and position information from parents
        """

        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()

        # Extract customer genes (without separators)
        customers1 = [g for g in parent1 if g != -1]
        customers2 = [g for g in parent2 if g != -1]

        size = len(customers1)

        # Select crossover points
        cx_point1 = random.randint(0, size - 1)
        cx_point2 = random.randint(cx_point1 + 1, size)

        # Create offspring using order crossover
        def create_offspring(p1, p2):
            offspring = [None] * size
            # Copy segment from parent1
            offspring[cx_point1:cx_point2] = p1[cx_point1:cx_point2]

            # Fill remaining from parent2
            p2_idx = 0
            for i in range(size):
                if offspring[i] is None:
                    while p2[p2_idx] in offspring:
                        p2_idx += 1
                    offspring[i] = p2[p2_idx]

            return offspring

        child1_customers = create_offspring(customers1, customers2)
        child2_customers = create_offspring(customers2, customers1)

        # Re-insert separators
        child1 = self._insert_separators(child1_customers)
        child2 = self._insert_separators(child2_customers)

        return child1, child2

    def _insert_separators(self, customers: List[int]) -> List[int]:
        """Insert vehicle separators into customer sequence"""

        chromosome = []
        customers_per_vehicle = len(customers) // self.num_vehicles

        for i, customer in enumerate(customers):
            chromosome.append(customer)
            if ((i + 1) % customers_per_vehicle == 0 and
                i < len(customers) - 1):
                chromosome.append(-1)

        return chromosome

    def _mutation(self, chromosome: List[int]) -> List[int]:
        """
        Mutation: swap two customer positions
        """

        if random.random() > self.mutation_rate:
            return chromosome

        # Get customer positions (not separators)
        customer_positions = [i for i, g in enumerate(chromosome) if g != -1]

        if len(customer_positions) < 2:
            return chromosome

        # Swap two random customers
        pos1, pos2 = random.sample(customer_positions, 2)
        chromosome[pos1], chromosome[pos2] = chromosome[pos2], chromosome[pos1]

        return chromosome

    def _elitism(self, population: List[List[int]],
                 fitness_scores: List[float]) -> List[List[int]]:
        """Select elite individuals (best solutions)"""

        sorted_idx = np.argsort(fitness_scores)
        elite = [population[i] for i in sorted_idx[:self.elite_size]]

        return elite

    def optimize(self) -> Dict:
        """
        Run genetic algorithm

        Returns: optimization results
        """

        print(f"Initializing GA for VRP with {self.n_customers} customers...")
        print(f"Population: {self.population_size}, Generations: {self.generations}")

        # Initialize
        population = self._initialize_population()

        for generation in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self._calculate_fitness(chromo) for chromo in population]

            # Track best solution
            best_gen_fitness = min(fitness_scores)
            best_gen_idx = np.argmin(fitness_scores)

            if best_gen_fitness < self.best_fitness:
                self.best_fitness = best_gen_fitness
                self.best_solution = population[best_gen_idx].copy()

            self.fitness_history.append(self.best_fitness)

            # Progress report
            if (generation + 1) % 50 == 0:
                print(f"Generation {generation + 1}: Best Fitness = {self.best_fitness:.2f}")

            # Elitism: keep best solutions
            elite = self._elitism(population, fitness_scores)

            # Selection
            selected = self._selection(population, fitness_scores)

            # Create next generation
            offspring = []

            for i in range(0, len(selected) - 1, 2):
                parent1 = selected[i]
                parent2 = selected[i + 1]

                # Crossover
                child1, child2 = self._crossover(parent1, parent2)

                # Mutation
                child1 = self._mutation(child1)
                child2 = self._mutation(child2)

                offspring.extend([child1, child2])

            # New population: elite + offspring
            population = elite + offspring[:self.population_size - self.elite_size]

        # Decode best solution
        best_routes = self._decode_chromosome(self.best_solution)

        return {
            'best_solution': best_routes,
            'total_distance': self.best_fitness,
            'chromosome': self.best_solution,
            'fitness_history': self.fitness_history,
            'generations': self.generations
        }

    def plot_solution(self, solution: List[List[int]]):
        """Visualize the best routes"""

        plt.figure(figsize=(12, 10))

        # Plot depot
        depot_x, depot_y = self.depot
        plt.plot(depot_x, depot_y, 'rs', markersize=15, label='Depot')

        # Plot customers
        customer_x = [c[0] for c in self.customers]
        customer_y = [c[1] for c in self.customers]
        plt.plot(customer_x, customer_y, 'bo', markersize=8, label='Customers')

        # Plot routes
        colors = plt.cm.rainbow(np.linspace(0, 1, len(solution)))

        for route_idx, route in enumerate(solution):
            if not route:
                continue

            # Route coordinates: depot -> customers -> depot
            route_coords = [self.depot]
            route_coords.extend([self.customers[c - 1] for c in route])
            route_coords.append(self.depot)

            route_x = [coord[0] for coord in route_coords]
            route_y = [coord[1] for coord in route_coords]

            plt.plot(route_x, route_y, 'o-',
                    color=colors[route_idx],
                    linewidth=2,
                    markersize=4,
                    label=f'Vehicle {route_idx + 1}')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Vehicle Routing Problem - GA Solution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def plot_convergence(self):
        """Plot fitness convergence"""

        plt.figure(figsize=(10, 6))
        plt.plot(self.fitness_history, linewidth=2)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness (Total Distance)')
        plt.title('GA Convergence')
        plt.grid(True, alpha=0.3)
        plt.show()


# Example usage
if __name__ == "__main__":
    # Generate random problem instance
    np.random.seed(42)
    random.seed(42)

    # 30 customers randomly distributed
    n_customers = 30
    customers = [(random.uniform(0, 100), random.uniform(0, 100))
                 for _ in range(n_customers)]

    # Random demands
    demands = [random.uniform(5, 25) for _ in range(n_customers)]

    # Create GA optimizer
    ga_vrp = GeneticAlgorithmVRP(
        customers=customers,
        demands=demands,
        depot=(50, 50),
        vehicle_capacity=100,
        num_vehicles=5,
        population_size=100,
        generations=300,
        mutation_rate=0.15,
        crossover_rate=0.8
    )

    # Optimize
    result = ga_vrp.optimize()

    print("\nOptimization Complete!")
    print(f"Total Distance: {result['total_distance']:.2f}")
    print(f"\nRoutes:")
    for i, route in enumerate(result['best_solution']):
        route_demand = sum(demands[c - 1] for c in route)
        print(f"  Vehicle {i + 1}: {route} (Demand: {route_demand:.1f})")

    # Visualize
    ga_vrp.plot_solution(result['best_solution'])
    ga_vrp.plot_convergence()
```

---

## Simulated Annealing (SA)

### Core Concepts

**Metallurgical Analogy:**
- **Annealing**: Heating then slowly cooling metal
- **Temperature**: Control parameter for randomness
- **Cooling Schedule**: Reduces temperature over time
- **Acceptance Criterion**: Accept worse solutions probabilistically

### SA for Job Shop Scheduling

```python
import numpy as np
import random
import math
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

class SimulatedAnnealingJobShop:
    """
    Simulated Annealing for Job Shop Scheduling Problem (JSSP)

    Problem: Schedule jobs on machines to minimize makespan
    Each job has sequence of operations on different machines
    """

    def __init__(self,
                 jobs: List[List[Tuple[int, int]]],
                 initial_temp: float = 1000,
                 final_temp: float = 0.1,
                 cooling_rate: float = 0.95,
                 iterations_per_temp: int = 100):
        """
        Initialize SA for JSSP

        jobs: list of jobs, each job is list of (machine, processing_time)
              Example: [[(0, 3), (1, 2), (2, 2)],  # Job 1
                       [(0, 2), (2, 1), (1, 4)]]   # Job 2
        """

        self.jobs = jobs
        self.n_jobs = len(jobs)
        self.n_machines = max(max(op[0] for op in job) for job in jobs) + 1

        # SA parameters
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.cooling_rate = cooling_rate
        self.iterations_per_temp = iterations_per_temp

        # Results
        self.best_solution = None
        self.best_makespan = float('inf')
        self.makespan_history = []
        self.temperature_history = []

    def _create_initial_solution(self) -> List[Tuple[int, int]]:
        """
        Create initial solution using random dispatch rule

        Solution representation: list of (job_id, operation_idx) tuples
        """

        # Create list of all operations
        operations = []
        for job_id, job in enumerate(self.jobs):
            for op_idx in range(len(job)):
                operations.append((job_id, op_idx))

        # Random shuffle
        random.shuffle(operations)

        return operations

    def _calculate_makespan(self, solution: List[Tuple[int, int]]) -> float:
        """
        Calculate makespan (total completion time) for given schedule

        Returns: makespan value
        """

        # Track completion time for each job's operations
        job_completion = [0] * self.n_jobs

        # Track availability of each machine
        machine_available = [0] * self.n_machines

        for job_id, op_idx in solution:
            machine, proc_time = self.jobs[job_id][op_idx]

            # Operation can start when:
            # 1. Previous operation of same job is complete
            # 2. Machine is available
            start_time = max(job_completion[job_id], machine_available[machine])
            end_time = start_time + proc_time

            # Update times
            job_completion[job_id] = end_time
            machine_available[machine] = end_time

        # Makespan is maximum completion time
        makespan = max(job_completion)

        return makespan

    def _get_neighbor(self, solution: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Generate neighbor solution using swap move

        Swap two adjacent operations that can be swapped without violating
        precedence constraints
        """

        neighbor = solution.copy()

        # Find valid swap positions
        valid_swaps = []
        for i in range(len(solution) - 1):
            job1, op1 = solution[i]
            job2, op2 = solution[i + 1]

            # Can swap if different jobs (no precedence conflict)
            if job1 != job2:
                valid_swaps.append(i)

        if not valid_swaps:
            return neighbor

        # Perform random swap
        swap_pos = random.choice(valid_swaps)
        neighbor[swap_pos], neighbor[swap_pos + 1] = \
            neighbor[swap_pos + 1], neighbor[swap_pos]

        return neighbor

    def _acceptance_probability(self, current_cost: float,
                                neighbor_cost: float,
                                temperature: float) -> float:
        """
        Calculate acceptance probability for worse solution

        Metropolis criterion: exp(-ΔE / T)
        """

        if neighbor_cost < current_cost:
            return 1.0

        delta = neighbor_cost - current_cost
        return math.exp(-delta / temperature)

    def optimize(self) -> Dict:
        """
        Run simulated annealing

        Returns: optimization results
        """

        print(f"Initializing SA for Job Shop Scheduling...")
        print(f"Jobs: {self.n_jobs}, Machines: {self.n_machines}")
        print(f"Initial Temp: {self.initial_temp}, Final Temp: {self.final_temp}")

        # Initialize
        current_solution = self._create_initial_solution()
        current_makespan = self._calculate_makespan(current_solution)

        self.best_solution = current_solution.copy()
        self.best_makespan = current_makespan

        temperature = self.initial_temp
        iteration = 0

        # Annealing loop
        while temperature > self.final_temp:

            for _ in range(self.iterations_per_temp):
                iteration += 1

                # Generate neighbor
                neighbor_solution = self._get_neighbor(current_solution)
                neighbor_makespan = self._calculate_makespan(neighbor_solution)

                # Acceptance decision
                accept_prob = self._acceptance_probability(
                    current_makespan, neighbor_makespan, temperature
                )

                if random.random() < accept_prob:
                    current_solution = neighbor_solution
                    current_makespan = neighbor_makespan

                    # Update best
                    if current_makespan < self.best_makespan:
                        self.best_solution = current_solution.copy()
                        self.best_makespan = current_makespan

            # Record history
            self.makespan_history.append(self.best_makespan)
            self.temperature_history.append(temperature)

            # Cool down
            temperature *= self.cooling_rate

            # Progress report
            if len(self.makespan_history) % 10 == 0:
                print(f"Iteration {iteration}: "
                      f"Best Makespan = {self.best_makespan:.2f}, "
                      f"Temp = {temperature:.2f}")

        return {
            'best_solution': self.best_solution,
            'best_makespan': self.best_makespan,
            'makespan_history': self.makespan_history,
            'temperature_history': self.temperature_history,
            'iterations': iteration
        }

    def plot_gantt_chart(self, solution: List[Tuple[int, int]]):
        """
        Visualize schedule as Gantt chart
        """

        # Calculate schedule times
        job_completion = [0] * self.n_jobs
        machine_available = [0] * self.n_machines

        schedule = []

        for job_id, op_idx in solution:
            machine, proc_time = self.jobs[job_id][op_idx]

            start_time = max(job_completion[job_id], machine_available[machine])
            end_time = start_time + proc_time

            schedule.append({
                'job': job_id,
                'machine': machine,
                'start': start_time,
                'duration': proc_time
            })

            job_completion[job_id] = end_time
            machine_available[machine] = end_time

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(14, 8))

        colors = plt.cm.Set3(np.linspace(0, 1, self.n_jobs))

        for task in schedule:
            ax.barh(task['machine'],
                   task['duration'],
                   left=task['start'],
                   height=0.6,
                   color=colors[task['job']],
                   edgecolor='black',
                   linewidth=1.5)

            # Add job label
            ax.text(task['start'] + task['duration'] / 2,
                   task['machine'],
                   f"J{task['job']}",
                   ha='center',
                   va='center',
                   fontsize=10,
                   fontweight='bold')

        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Machine', fontsize=12)
        ax.set_title(f'Job Shop Schedule - Makespan: {self.best_makespan:.2f}',
                    fontsize=14)
        ax.set_yticks(range(self.n_machines))
        ax.set_yticklabels([f'M{i}' for i in range(self.n_machines)])
        ax.grid(True, axis='x', alpha=0.3)

        # Legend
        legend_elements = [plt.Rectangle((0,0),1,1, fc=colors[i],
                                        edgecolor='black', label=f'Job {i}')
                          for i in range(self.n_jobs)]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.show()

    def plot_convergence(self):
        """Plot makespan and temperature convergence"""

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Makespan convergence
        ax1.plot(self.makespan_history, linewidth=2, color='blue')
        ax1.set_xlabel('Cooling Iteration')
        ax1.set_ylabel('Best Makespan')
        ax1.set_title('SA Convergence')
        ax1.grid(True, alpha=0.3)

        # Temperature schedule
        ax2.plot(self.temperature_history, linewidth=2, color='red')
        ax2.set_xlabel('Cooling Iteration')
        ax2.set_ylabel('Temperature')
        ax2.set_title('Cooling Schedule')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)

    # Example: 5 jobs, 3 machines
    # Each job: list of (machine, processing_time)
    jobs = [
        [(0, 3), (1, 2), (2, 2)],  # Job 0
        [(0, 2), (2, 1), (1, 4)],  # Job 1
        [(1, 4), (2, 3)],          # Job 2
        [(0, 3), (1, 1), (2, 2)],  # Job 3
        [(2, 2), (0, 3), (1, 1)]   # Job 4
    ]

    # Create SA optimizer
    sa_jssp = SimulatedAnnealingJobShop(
        jobs=jobs,
        initial_temp=1000,
        final_temp=0.1,
        cooling_rate=0.95,
        iterations_per_temp=100
    )

    # Optimize
    result = sa_jssp.optimize()

    print("\nOptimization Complete!")
    print(f"Best Makespan: {result['best_makespan']:.2f}")

    # Visualize
    sa_jssp.plot_gantt_chart(result['best_solution'])
    sa_jssp.plot_convergence()
```

---

## Tabu Search

### Core Concepts

**Memory-Based Search:**
- **Tabu List**: Remember recent moves to avoid cycling
- **Aspiration Criterion**: Override tabu if solution is best found
- **Intensification**: Focus on promising regions
- **Diversification**: Explore new regions

### Tabu Search for Facility Location

```python
import numpy as np
import random
from typing import List, Set, Tuple, Dict
import matplotlib.pyplot as plt

class TabuSearchFacilityLocation:
    """
    Tabu Search for Capacitated Facility Location Problem

    Problem: Select facilities to open and assign customers to minimize
             total cost (fixed + transportation)
    """

    def __init__(self,
                 customer_locations: List[Tuple[float, float]],
                 facility_locations: List[Tuple[float, float]],
                 customer_demands: List[float],
                 facility_capacities: List[float],
                 fixed_costs: List[float],
                 tabu_tenure: int = 10,
                 max_iterations: int = 500,
                 intensification_freq: int = 50):
        """
        Initialize Tabu Search for CFLP

        customer_locations: list of (x, y) for customers
        facility_locations: list of (x, y) for facilities
        customer_demands: demand for each customer
        facility_capacities: capacity of each facility
        fixed_costs: fixed cost to open each facility
        tabu_tenure: how long moves stay tabu
        """

        self.customers = customer_locations
        self.facilities = facility_locations
        self.demands = customer_demands
        self.capacities = facility_capacities
        self.fixed_costs = fixed_costs

        self.n_customers = len(customer_locations)
        self.n_facilities = len(facility_locations)

        # Tabu Search parameters
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        self.intensification_freq = intensification_freq

        # Distance matrix
        self.distance_matrix = self._calculate_distances()

        # Results
        self.best_solution = None
        self.best_cost = float('inf')
        self.cost_history = []

    def _calculate_distances(self) -> np.ndarray:
        """Calculate distances between customers and facilities"""

        distances = np.zeros((self.n_customers, self.n_facilities))

        for i, cust in enumerate(self.customers):
            for j, fac in enumerate(self.facilities):
                dist = np.sqrt((cust[0] - fac[0])**2 + (cust[1] - fac[1])**2)
                distances[i, j] = dist

        return distances

    def _create_initial_solution(self) -> Dict:
        """
        Create initial solution

        Solution: {
            'open_facilities': set of facility indices,
            'assignments': list of facility assigned to each customer
        }
        """

        # Greedy construction: open cheapest facilities until demand met
        sorted_facilities = sorted(range(self.n_facilities),
                                  key=lambda f: self.fixed_costs[f] /
                                               self.capacities[f])

        open_facilities = set()
        total_capacity = 0
        total_demand = sum(self.demands)

        for fac in sorted_facilities:
            if total_capacity >= total_demand:
                break
            open_facilities.add(fac)
            total_capacity += self.capacities[fac]

        # Assign customers to nearest open facility
        assignments = self._assign_customers(open_facilities)

        return {
            'open_facilities': open_facilities,
            'assignments': assignments
        }

    def _assign_customers(self, open_facilities: Set[int]) -> List[int]:
        """
        Assign customers to open facilities (nearest with capacity)

        Returns: list where assignments[i] = facility for customer i
        """

        assignments = [-1] * self.n_customers
        facility_load = {f: 0 for f in open_facilities}

        # Sort customers by minimum distance to any open facility
        customer_order = sorted(range(self.n_customers),
                               key=lambda c: min(self.distance_matrix[c, f]
                                               for f in open_facilities))

        for cust in customer_order:
            # Find nearest facility with available capacity
            sorted_facs = sorted(open_facilities,
                               key=lambda f: self.distance_matrix[cust, f])

            for fac in sorted_facs:
                if facility_load[fac] + self.demands[cust] <= self.capacities[fac]:
                    assignments[cust] = fac
                    facility_load[fac] += self.demands[cust]
                    break

            # If no capacity, assign to nearest (will be penalized)
            if assignments[cust] == -1:
                assignments[cust] = sorted_facs[0]
                facility_load[sorted_facs[0]] += self.demands[cust]

        return assignments

    def _calculate_cost(self, solution: Dict) -> float:
        """
        Calculate total cost for solution

        Cost = fixed costs + transportation costs + capacity penalty
        """

        open_facilities = solution['open_facilities']
        assignments = solution['assignments']

        # Fixed costs
        fixed_cost = sum(self.fixed_costs[f] for f in open_facilities)

        # Transportation costs
        transport_cost = sum(
            self.distance_matrix[c, assignments[c]]
            for c in range(self.n_customers)
        )

        # Capacity penalty
        facility_load = {f: 0 for f in open_facilities}
        for c, f in enumerate(assignments):
            facility_load[f] = facility_load.get(f, 0) + self.demands[c]

        penalty = 0
        for f in open_facilities:
            if facility_load[f] > self.capacities[f]:
                penalty += (facility_load[f] - self.capacities[f]) * 1000

        return fixed_cost + transport_cost + penalty

    def _get_neighborhood(self, solution: Dict,
                         tabu_list: List) -> List[Dict]:
        """
        Generate neighborhood solutions

        Two types of moves:
        1. Open/close a facility
        2. Reassign a customer
        """

        neighbors = []

        open_facilities = solution['open_facilities'].copy()

        # Move 1: Open/close facility
        for fac in range(self.n_facilities):
            if fac in open_facilities:
                # Try closing
                if len(open_facilities) > 1:  # Keep at least one open
                    new_open = open_facilities - {fac}
                    if ('close', fac) not in tabu_list:
                        new_assignments = self._assign_customers(new_open)
                        neighbors.append({
                            'open_facilities': new_open,
                            'assignments': new_assignments,
                            'move': ('close', fac)
                        })
            else:
                # Try opening
                new_open = open_facilities | {fac}
                if ('open', fac) not in tabu_list:
                    new_assignments = self._assign_customers(new_open)
                    neighbors.append({
                        'open_facilities': new_open,
                        'assignments': new_assignments,
                        'move': ('open', fac)
                    })

        return neighbors

    def optimize(self) -> Dict:
        """
        Run Tabu Search

        Returns: optimization results
        """

        print(f"Initializing Tabu Search for Facility Location...")
        print(f"Customers: {self.n_customers}, Facilities: {self.n_facilities}")
        print(f"Max Iterations: {self.max_iterations}")

        # Initialize
        current_solution = self._create_initial_solution()
        current_cost = self._calculate_cost(current_solution)

        self.best_solution = current_solution.copy()
        self.best_cost = current_cost

        tabu_list = []

        for iteration in range(self.max_iterations):

            # Generate neighbors
            neighbors = self._get_neighborhood(current_solution, tabu_list)

            if not neighbors:
                print("No valid neighbors found!")
                break

            # Evaluate neighbors
            neighbor_costs = [self._calculate_cost(n) for n in neighbors]

            # Select best non-tabu neighbor (or best if aspiration met)
            best_neighbor_idx = np.argmin(neighbor_costs)
            best_neighbor = neighbors[best_neighbor_idx]
            best_neighbor_cost = neighbor_costs[best_neighbor_idx]

            # Aspiration criterion: accept if best overall
            if best_neighbor_cost < self.best_cost:
                current_solution = best_neighbor
                current_cost = best_neighbor_cost

                self.best_solution = current_solution.copy()
                self.best_cost = best_neighbor_cost

                print(f"Iteration {iteration + 1}: "
                      f"New best solution found! Cost = {self.best_cost:.2f}")
            else:
                # Accept best neighbor
                current_solution = best_neighbor
                current_cost = best_neighbor_cost

            # Update tabu list
            if 'move' in best_neighbor:
                tabu_list.append(best_neighbor['move'])
                if len(tabu_list) > self.tabu_tenure:
                    tabu_list.pop(0)

            self.cost_history.append(self.best_cost)

            # Progress report
            if (iteration + 1) % 50 == 0:
                print(f"Iteration {iteration + 1}: "
                      f"Best Cost = {self.best_cost:.2f}, "
                      f"Current Cost = {current_cost:.2f}")

        return {
            'best_solution': self.best_solution,
            'best_cost': self.best_cost,
            'cost_history': self.cost_history,
            'open_facilities': self.best_solution['open_facilities'],
            'assignments': self.best_solution['assignments']
        }

    def plot_solution(self, solution: Dict):
        """Visualize the facility location solution"""

        plt.figure(figsize=(12, 10))

        open_facilities = solution['open_facilities']
        assignments = solution['assignments']

        # Plot customers
        cust_x = [c[0] for c in self.customers]
        cust_y = [c[1] for c in self.customers]
        plt.scatter(cust_x, cust_y, c='blue', s=100,
                   marker='o', label='Customers', zorder=3)

        # Plot facilities
        colors = plt.cm.Set1(np.linspace(0, 1, len(open_facilities)))

        for i, fac_idx in enumerate(open_facilities):
            fac = self.facilities[fac_idx]
            plt.scatter(fac[0], fac[1], c=[colors[i]], s=400,
                       marker='s', edgecolors='black', linewidth=2,
                       label=f'Facility {fac_idx}', zorder=4)

            # Draw assignments
            for cust_idx, assigned_fac in enumerate(assignments):
                if assigned_fac == fac_idx:
                    cust = self.customers[cust_idx]
                    plt.plot([cust[0], fac[0]], [cust[1], fac[1]],
                            color=colors[i], alpha=0.3, linewidth=1, zorder=1)

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Facility Location - Total Cost: {self.best_cost:.2f}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def plot_convergence(self):
        """Plot cost convergence"""

        plt.figure(figsize=(10, 6))
        plt.plot(self.cost_history, linewidth=2)
        plt.xlabel('Iteration')
        plt.ylabel('Best Cost')
        plt.title('Tabu Search Convergence')
        plt.grid(True, alpha=0.3)
        plt.show()


# Example usage
if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)

    # Generate problem instance
    n_customers = 40
    n_facilities = 8

    customers = [(random.uniform(0, 100), random.uniform(0, 100))
                 for _ in range(n_customers)]
    facilities = [(random.uniform(0, 100), random.uniform(0, 100))
                  for _ in range(n_facilities)]

    demands = [random.uniform(10, 30) for _ in range(n_customers)]
    capacities = [random.uniform(150, 250) for _ in range(n_facilities)]
    fixed_costs = [random.uniform(500, 1500) for _ in range(n_facilities)]

    # Create Tabu Search optimizer
    ts_flp = TabuSearchFacilityLocation(
        customer_locations=customers,
        facility_locations=facilities,
        customer_demands=demands,
        facility_capacities=capacities,
        fixed_costs=fixed_costs,
        tabu_tenure=15,
        max_iterations=300
    )

    # Optimize
    result = ts_flp.optimize()

    print("\nOptimization Complete!")
    print(f"Total Cost: {result['best_cost']:.2f}")
    print(f"Open Facilities: {result['open_facilities']}")

    # Visualize
    ts_flp.plot_solution(result['best_solution'])
    ts_flp.plot_convergence()
```

---

## Other Metaheuristics

### Ant Colony Optimization (ACO)

**Concept**: Simulate ant foraging behavior
- Ants deposit pheromones on paths
- Future ants follow strong pheromone trails
- Good solutions reinforced over time

**Applications**: TSP, VRP, network routing

**Key Parameters**:
- α (alpha): pheromone importance
- β (beta): heuristic information importance
- ρ (rho): evaporation rate
- Q: pheromone deposit amount

### Particle Swarm Optimization (PSO)

**Concept**: Simulate bird flocking or fish schooling
- Particles move in search space
- Influenced by personal best and global best
- Velocity and position updates

**Applications**: Continuous optimization, parameter tuning

**Update Rules**:
```python
v_new = w * v + c1 * r1 * (pbest - x) + c2 * r2 * (gbest - x)
x_new = x + v_new
```

### Variable Neighborhood Search (VNS)

**Concept**: Systematically change neighborhood structure
- Local search in multiple neighborhoods
- Shake to escape local optima
- Structured exploration

**Applications**: Routing, scheduling, location

---

## Hybrid Metaheuristics

### Genetic Algorithm + Local Search

```python
def hybrid_ga_local_search(problem, ga_params, ls_params):
    """
    Hybrid GA with local search

    GA for global exploration + Local search for exploitation
    """

    # Initialize GA population
    population = initialize_population(ga_params['pop_size'])

    for generation in range(ga_params['generations']):
        # GA operations
        offspring = []
        for _ in range(ga_params['offspring_size']):
            parents = tournament_selection(population, 2)
            child = crossover(parents[0], parents[1])
            child = mutate(child, ga_params['mutation_rate'])
            offspring.append(child)

        # Apply local search to best offspring
        offspring_fitness = [evaluate(ind) for ind in offspring]
        best_idx = np.argmin(offspring_fitness)

        # Local search improves best individual
        offspring[best_idx] = local_search(offspring[best_idx], ls_params)

        # Update population
        population = elitism_replacement(population, offspring,
                                        ga_params['elite_size'])

    return best_individual(population)
```

---

## Parameter Tuning

### Critical Parameters

**Population-Based (GA, PSO):**
- Population size: 50-200 for most problems
- Mutation rate: 0.05-0.20
- Crossover rate: 0.7-0.9
- Elite size: 5-20% of population

**Trajectory-Based (SA, TS):**
- Initial temperature (SA): 10-1000x expected cost
- Cooling rate (SA): 0.90-0.99
- Tabu tenure (TS): 7-20 iterations
- Neighborhood size: problem-dependent

### Automated Tuning

```python
from scipy.optimize import differential_evolution

def tune_ga_parameters(problem_instances):
    """
    Automated parameter tuning using meta-optimization
    """

    def objective(params):
        pop_size, mutation_rate, crossover_rate = params

        # Run GA with these parameters on validation set
        avg_quality = 0
        for problem in problem_instances:
            result = run_ga(problem,
                          pop_size=int(pop_size),
                          mutation_rate=mutation_rate,
                          crossover_rate=crossover_rate)
            avg_quality += result['best_fitness']

        return avg_quality / len(problem_instances)

    # Bounds for parameters
    bounds = [
        (50, 200),    # population size
        (0.01, 0.3),  # mutation rate
        (0.6, 0.95)   # crossover rate
    ]

    # Meta-optimize
    result = differential_evolution(objective, bounds)

    optimal_params = {
        'pop_size': int(result.x[0]),
        'mutation_rate': result.x[1],
        'crossover_rate': result.x[2]
    }

    return optimal_params
```

---

## Tools & Libraries

### Python Libraries

**Metaheuristic Frameworks:**
- `pymoo`: Multi-objective optimization
- `deap`: Distributed evolutionary algorithms
- `scipy.optimize`: Differential evolution, basin hopping
- `optuna`: Hyperparameter optimization

**Problem-Specific:**
- `python-tsp`: TSP solvers
- `or-tools (Google)`: Routing, scheduling
- `jmetal`: Multi-objective metaheuristics

**Parallel Computing:**
- `joblib`: Parallel function calls
- `dask`: Distributed computing
- `ray`: Scalable computing

### Commercial Software

- **FICO Xpress Mosel**: Metaheuristic module
- **CPLEX with Heuristics**: MIP heuristics
- **LocalSolver**: Local search solver

---

## Common Challenges & Solutions

### Challenge: Premature Convergence

**Problem:**
- Population loses diversity too quickly
- Stuck in local optimum

**Solutions:**
- Increase mutation rate
- Diversity preservation mechanisms
- Restart strategies
- Adaptive parameter control
- Niching techniques

### Challenge: Slow Convergence

**Problem:**
- Takes too long to find good solutions
- Insufficient exploitation

**Solutions:**
- Hybrid with local search
- Better initialization (greedy construction)
- Stronger selection pressure
- Adaptive neighborhood sizing
- Problem-specific operators

### Challenge: Parameter Sensitivity

**Problem:**
- Performance varies widely with parameters
- Difficult to tune

**Solutions:**
- Adaptive parameter control
- Parameter-free metaheuristics
- Automated tuning (meta-optimization)
- Use established defaults from literature

### Challenge: No Improvement Plateau

**Problem:**
- Algorithm stops improving
- Exploration exhausted

**Solutions:**
- Perturbation/restart mechanisms
- Change neighborhood structure (VNS)
- Diversification strategies
- Multi-start approach
- Combine multiple algorithms

---

## Best Practices

### Algorithm Selection

**Choose Metaheuristics When:**
- Problem is NP-hard
- Exact methods too slow
- Near-optimal solutions acceptable
- Limited time available
- Problem structure unknown

**Algorithm Selection Guide:**

| Problem Type | Recommended Algorithm |
|--------------|---------------------|
| Permutation (TSP, VRP) | GA with OX crossover, ACO |
| Binary (facility location) | GA, Tabu Search |
| Continuous | PSO, Differential Evolution, SA |
| Scheduling | Tabu Search, SA, GA |
| Multi-objective | NSGA-II, MOEA/D |

### Implementation Tips

1. **Start Simple**: Implement basic version first
2. **Use Problem Knowledge**: Design custom operators
3. **Benchmark**: Compare against simple heuristics
4. **Track Progress**: Log best solutions over time
5. **Multiple Runs**: Run 10-30 times with different seeds
6. **Validate Solutions**: Check constraint satisfaction

---

## Output Format

### Metaheuristic Report Template

**Executive Summary:**
- Problem description
- Algorithm selected and why
- Best solution quality
- Computational time

**Problem Formulation:**
- Decision variables
- Objective function
- Constraints
- Problem size

**Algorithm Configuration:**

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Algorithm | Genetic Algorithm | Good for permutation problems |
| Population Size | 100 | Balance between diversity and speed |
| Generations | 500 | Convergence observed by gen 400 |
| Mutation Rate | 0.15 | Standard for this problem type |
| Crossover | Order Crossover (OX) | Preserves permutation validity |

**Results:**

| Metric | Value |
|--------|-------|
| Best Objective | $125,456 |
| Average (10 runs) | $128,234 |
| Std Dev | $1,823 |
| Best Run Time | 45 seconds |
| Gap from Lower Bound | 5.2% |

**Solution Quality:**
- Convergence plot
- Solution visualization
- Comparison with baseline
- Statistical analysis (multiple runs)

**Recommendations:**
- Deploy best solution
- Expected improvement
- Further optimization opportunities

---

## Questions to Ask

If you need more context:
1. What problem are you trying to solve?
2. What makes exact optimization impractical?
3. What's the problem size? (variables, constraints)
4. How much time is available for optimization?
5. Is solution quality critical or is "good enough" acceptable?
6. Are there constraints? Hard or soft?
7. Any domain-specific knowledge to leverage?
8. Is this one-time or repeated optimization?

---

## Related Skills

- **optimization-modeling**: For exact optimization methods
- **multi-objective-optimization**: For Pareto optimization
- **constraint-programming**: For constraint-based search
- **route-optimization**: For VRP applications
- **production-scheduling**: For scheduling problems
- **network-design**: For network optimization
- **prescriptive-analytics**: For decision optimization
- **supply-chain-automation**: For automated optimization
