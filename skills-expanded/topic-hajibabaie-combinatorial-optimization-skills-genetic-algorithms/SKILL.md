---
name: genetic-algorithms
description: When the user wants to design, implement, or tune a genetic algorithm for combinatorial optimization: the canonical GA loop, encoding choice, selection, crossover, mutation, elitism, population sizing, premature convergence, and numpy-vectorized population implementations. Also use when the user mentions "genetic algorithm," "GA," "crossover," "population-based," "fitness function," "elitism," or when the problem calls for population-based search over a discrete solution space. For the full crossover catalog, see crossover-operators; for GA-plus-local-search hybrids, see memetic-algorithms.
---

# Genetic Algorithms

You are an expert in genetic algorithms (GAs) for combinatorial optimization. This skill covers the canonical generational GA loop, encoding selection, the selection/crossover/mutation operator triad, elitism, population sizing, selection-pressure analysis, and the diagnosis and prevention of premature convergence, with a reusable numpy-vectorized implementation. Use the framework below to take a user from "I want to try a GA" to a calibrated, reproducible implementation that is honest about when a GA is the right tool — and when it is not.

## Initial Assessment

Establish these facts before writing any GA code:

- **Decision variable and natural encoding.** Is a solution a binary vector, a permutation, an integer assignment, or mixed? The encoding fixes which operators are legal; choose it first (see solution-encodings). Both worked examples below — permutation TSP and binary knapsack — exist because this choice changes everything downstream.
- **Problem size and scaling.** How many genes n, and how does one evaluation scale in n? Population memory is $O(Nn)$ and vectorized operators cost $O(Nn)$ per generation, so the genome length rarely limits a GA — the evaluation usually does.
- **Exact alternative check.** Estimate whether a MIP solver or dynamic program reaches optimality within the time budget; many "GA problems" with a few hundred variables are exactly solvable. Even when they are not, solve small instances exactly anyway: a GA that cannot match brute force on 15 items is broken, not unlucky.
- **Why a GA at all.** A GA earns its complexity only when recombining two good solutions tends to produce another good solution, i.e., the problem has building blocks that crossover can exchange. If the problem rewards pure intensification, iterated local search or tabu search with a strong neighborhood usually wins. Insist on a simple baseline.
- **Constraint structure.** For each constraint, decide: satisfied by encoding (a permutation always visits each city once), restored by a repair operator, or penalized in the fitness. This decision shapes the operator set; see constraint-handling-techniques for the full menu.
- **Evaluation cost and vectorizability.** A GA spends almost all time in fitness evaluation. Can the whole population be evaluated as one `(N, n)` array operation? If a single evaluation takes seconds (simulation, solver call), the affordable population and generation counts shrink drastically and surrogate or cached evaluation becomes relevant.
- **Evaluation budget.** Total evaluations = population size × generations (plus initialization). Fix the budget from the wall-clock limit and measured evaluations per second, then split it between N and generations — do not pick both independently.
- **Local search availability.** If a cheap improvement procedure exists (2-opt for tours, greedy add/drop for subsets), plan for a memetic algorithm from the start; pure GAs are rarely competitive on classic permutation benchmarks (see memetic-algorithms).
- **Quality requirement.** A 2-5% gap from best-known is the realistic target for a plain, well-tuned GA on hard combinatorial problems. Matching best-known typically requires hybridization.
- **Multi-objective?** If yes, the replacement scheme changes fundamentally (non-dominated sorting, crowding); the single-objective loop here is the wrong skeleton.
- **Instance source and format.** Standard benchmark sets (TSPLIB, OR-Library, QAPLIB) or synthetic generators? Generated instances need their own recorded seeds so that every reported number can be regenerated bit-for-bit.
- **Reporting protocol.** Number of seeds per instance, instances, fixed budget per run, statistics to report (best/mean/std). A GA result from one seed is an anecdote.
- **Parameter-tuning budget.** Will parameters be tuned systematically (Optuna, irace) or set from the guidance table below? Reserve separate tuning instances to avoid overfitting.

## Algorithm Anatomy

### The canonical loop and its six design decisions

A generational GA maintains a population of N encoded solutions and repeats: select parents biased toward quality, recombine them, mutate the offspring, and replace the population while preserving the best individuals. Holland (1975), "Adaptation in Natural and Artificial Systems," introduced the framework; Goldberg (1989), "Genetic Algorithms in Search, Optimization and Machine Learning," fixed the canonical form used here. Every GA is fully specified by six decisions:

| Component | Decision | Robust default | Detail skill |
|---|---|---|---|
| Encoding | genotype structure | match the natural decision variable | solution-encodings |
| Fitness | objective + constraint handling | minimize cost; repair > penalty when cheap | constraint-handling-techniques |
| Selection | how parents are chosen | tournament, k = 2-4 | selection-and-replacement-strategies |
| Crossover | how parents recombine | encoding-specific (uniform / OX) at rate 0.6-0.95 | crossover-operators |
| Mutation | background variation | per-gene 1/n (binary); one move per individual (permutation) | mutation-and-perturbation-operators |
| Replacement | how generations turn over | generational + 1-5% elitism | selection-and-replacement-strategies |

### When a GA is the right tool

- **Use a GA** when solutions decompose into parts worth mixing (subsets, assignments with weak interactions, sequencing with reusable sub-orders), when no strong single-solution neighborhood with cheap delta evaluation is known, or when the objective is a black box that vectorizes well over a whole population.
- **Prefer iterated local search or tabu search** when a powerful neighborhood with $O(1)$/$O(n)$ delta evaluation exists and intensification drives quality — or keep the GA but make it memetic from the start (memetic-algorithms).
- **Prefer an estimation-of-distribution algorithm** when variables have strong, learnable dependencies that pairwise recombination scrambles; prefer BRKGA when a natural decoder exists and a problem-independent framework is wanted.
- **Prefer an exact solver outright** when instances are small or the formulation is tight; the GA then serves at most as a warm-start provider.

A GA chosen by default, without this comparison, is the most common design error in metaheuristic practice.

### Selection pressure, formally

Under fitness-proportionate (roulette) selection the expected copy count of individual $i$ is

$$
E[m_i] = N \,\frac{f_i}{\sum_{j} f_j},
$$

which collapses to near-uniform sampling once fitness values cluster — the standard failure of roulette late in a run. Tournament selection depends only on ranks: with tournament size $k$ and rank $r$ (1 = best of N),

$$
P(\text{rank } r \text{ wins a tournament}) = \frac{(N-r+1)^k - (N-r)^k}{N^k}.
$$

Goldberg & Deb (1991), "A Comparative Analysis of Selection Schemes Used in Genetic Algorithms," show the takeover time — generations until the best individual fills the population under selection alone — is approximately $\ln N / \ln k$ for tournament selection. For N = 100: about 6.6 generations at k = 2 and 4.2 at k = 3. Crossover and mutation push back against takeover; if observed convergence is much faster than these numbers suggest, selection pressure or elitism is too high.

### What crossover is supposed to do

The schema theorem (Holland 1975) bounds the growth of a pattern $H$ with order $o(H)$ (fixed positions) and defining length $\delta(H)$ (span):

$$
E[m(H, t+1)] \;\ge\; m(H,t)\,\frac{f(H)}{\bar f}\left(1 - p_c\,\frac{\delta(H)}{n-1} - o(H)\,p_m\right).
$$

The practical reading, independent of the debated building-block hypothesis: selection amplifies above-average patterns, while crossover and mutation destroy them at a rate growing with their span and order. Operators must therefore respect the structure that carries fitness — adjacency for tours (hence order/edge-preserving crossovers), subset membership for knapsacks (hence uniform crossover). An encoding-operator mismatch makes crossover a noise generator; the crossover-operators skill catalogs which operator preserves which property.

### Population sizing and budget split

Theory (Goldberg, Deb & Clark 1992, "Genetic Algorithms, Noise, and the Sizing of Populations"; Harik, Cantú-Paz, Goldberg & Miller 1999, the gambler's-ruin model) sizes N by the signal-to-noise ratio of competing building blocks — informative but not directly computable for a new problem. Practical protocol: under a fixed evaluation budget, run N ∈ {50, 100, 200, 400} with proportionally fewer generations and keep the best mean. Small N converges fast and stalls; large N explores but may not converge within budget. Per-generation work is $O(N \cdot c_{\text{eval}} + N \log N)$ with $O(N n)$ memory — almost always dominated by evaluation.

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| Population size N | 50-200 (binary), 100-400 (permutation) | Diversity, better final quality | Fewer generations per budget |
| Crossover rate $p_c$ | 0.6-0.95 | More recombination of building blocks | Disruption when operators mismatch the encoding |
| Mutation rate $p_m$ | 1/n per gene (binary); 0.1-0.4 per individual (permutation) | Diversity, escape from stalls | Random-walk behavior, destroyed offspring |
| Tournament size k | 2-5 | Faster convergence to good regions | Premature convergence, lost diversity |
| Elite count e | 1-5% of N | Monotone best-so-far, no regression | Diversity loss when overdone |
| Generations | budget / N | Deeper convergence | Nothing, if budget is truly fixed |

Tune N and k first — they control the explore/exploit balance; $p_c$ and $p_m$ are secondary once the defaults above are in place (De Jong 1975 and Grefenstette 1986 remain the classic parameter studies; Eiben & Smith 2015, "Introduction to Evolutionary Computing," is the modern reference).

## Reusable GA Framework

The engine below is problem-independent. It sees the population as one `(N, n)` numpy array and receives four callables: `init_population`, batch `evaluate` (minimization), batch `crossover`, and batch `mutate`. All problem knowledge lives in those hooks, so the TSP and knapsack examples reuse the loop unchanged. Selection is vectorized tournament; replacement is generational with elitism.

```text
GENETIC-ALGORITHM(instance, budget)
  P <- initial population of N encoded solutions   // random + a few greedy seeds
  evaluate cost of every individual in P           // one vectorized batch call
  repeat until budget exhausted:
      E <- the e best individuals of P             // elitism, e ~ 1-5% of N
      build N - e offspring:
          A, B <- tournament-select parent batches (size k)
          C <- crossover(A, B), each pair recombined with prob. pc
               (pairs that skip crossover copy parent A)
          C <- mutate(C)                           // per-gene rate ~ 1/n
      P <- E union C
      evaluate C in one batch; update best-so-far
      record best, mean, diversity                 // convergence diagnostics
  return best-so-far solution and cost
```

```python
import numpy as np
from typing import Callable

Array = np.ndarray


def tournament_selection(
    cost: Array, n_parents: int, k: int, rng: np.random.Generator
) -> Array:
    """Return indices of n_parents tournament winners (minimization).

    Draws an (n_parents, k) matrix of entrants in one call and picks the
    lowest-cost entrant per row -- no Python loop over tournaments.
    """
    entrants = rng.integers(0, cost.shape[0], size=(n_parents, k))
    return entrants[np.arange(n_parents), np.argmin(cost[entrants], axis=1)]


def run_ga(
    init_population: Callable[[np.random.Generator], Array],
    evaluate: Callable[[Array], Array],
    crossover: Callable[[Array, Array, np.random.Generator], Array],
    mutate: Callable[[Array, np.random.Generator], Array],
    *,
    n_generations: int = 200,
    tournament_k: int = 3,
    crossover_rate: float = 0.9,
    n_elites: int = 2,
    seed: int = 0,
) -> tuple[Array, float, Array]:
    """Generational GA with tournament selection and elitism.

    evaluate maps an (N, n) population to an (N,) cost vector (minimize).
    crossover maps two (M, n) parent arrays to one (M, n) child array.
    mutate maps an (M, n) child array to an (M, n) mutated array.
    Returns (best solution, best cost, best-cost-per-generation history).
    """
    rng = np.random.default_rng(seed)
    pop = init_population(rng)
    cost = evaluate(pop)
    n_pop = pop.shape[0]
    n_children = n_pop - n_elites
    history = np.empty(n_generations)
    for gen in range(n_generations):
        order = np.argsort(cost)
        elites, elite_cost = pop[order[:n_elites]], cost[order[:n_elites]]
        pa = pop[tournament_selection(cost, n_children, tournament_k, rng)]
        pb = pop[tournament_selection(cost, n_children, tournament_k, rng)]
        children = crossover(pa, pb, rng)
        skip = rng.random(n_children) > crossover_rate
        children[skip] = pa[skip]                 # pairs that skip crossover
        children = mutate(children, rng)
        pop = np.vstack([elites, children])
        cost = np.concatenate([elite_cost, evaluate(children)])
        history[gen] = cost.min()
    best = int(np.argmin(cost))
    return pop[best].copy(), float(cost[best]), history


def demo_onemax(n_bits: int = 60, pop_size: int = 80) -> None:
    """Sanity check on OneMax, stated as minimizing the count of zero bits."""

    def init(rng: np.random.Generator) -> Array:
        return rng.integers(0, 2, size=(pop_size, n_bits), dtype=np.int8)

    def evaluate(pop: Array) -> Array:
        return (pop == 0).sum(axis=1).astype(float)

    def uniform_crossover(pa: Array, pb: Array, rng: np.random.Generator) -> Array:
        mask = rng.random(pa.shape) < 0.5
        return np.where(mask, pa, pb)

    def bit_flip(children: Array, rng: np.random.Generator) -> Array:
        flip = rng.random(children.shape) < 1.0 / children.shape[1]
        return np.where(flip, 1 - children, children).astype(np.int8)

    best, best_cost, hist = run_ga(
        init, evaluate, uniform_crossover, bit_flip, n_generations=120, seed=42
    )
    solved_at = int(np.argmax(hist == 0)) if (hist == 0).any() else -1
    print(f"best cost {best_cost:.0f}, first hit generation {solved_at}")


if __name__ == "__main__":
    demo_onemax()
# Expected: best cost 0 (the all-ones string), first hit well before generation 120.
```

Design notes on the framework:

- **Minimization convention everywhere.** "Fitness function" in GA folklore means "bigger is better"; flipping signs at the boundary once avoids a whole class of bugs.
- **Elites are carried with their cached costs** — never re-evaluate unchanged individuals.
- **The crossover-skip mask copies parent A** rather than leaving slots empty, so offspring count is deterministic and array shapes never change.
- **All randomness flows through one `np.random.default_rng(seed)`**, making every run exactly reproducible from `(instance seed, algorithm seed)`.

## Worked Example: TSP with Order Crossover

A tour is a permutation of cities; tour quality lives in the *adjacencies and relative order* of cities, not their absolute positions. Order crossover (OX; Oliver, Smith & Holland 1987 compare it with PMX and CX) copies a slice from one parent and fills the remainder in the other parent's relative order — exactly the property worth inheriting. Inversion mutation reverses a segment, which is a 2-opt-style move in mutation form. For the full permutation-operator menu and its preservation properties, see crossover-operators and mutation-and-perturbation-operators.

```python
import numpy as np

Array = np.ndarray


def circle_instance(n: int, seed: int = 0) -> Array:
    """Distance matrix for n cities on the unit circle (indices sorted by angle).

    Points in convex position make the optimum known: the tour that visits
    cities in angular order, i.e., the identity permutation here.
    """
    rng = np.random.default_rng(seed)
    angles = np.sort(rng.uniform(0.0, 2.0 * np.pi, size=n))
    pts = np.column_stack([np.cos(angles), np.sin(angles)])
    return np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)


def tour_lengths(tours: Array, dist: Array) -> Array:
    """Vectorized closed-tour length of every row in an (N, n) permutation array."""
    nxt = np.roll(tours, -1, axis=1)
    return dist[tours, nxt].sum(axis=1)


def order_crossover(pa: Array, pb: Array, rng: np.random.Generator) -> Array:
    """OX: copy a random slice from parent A, fill the rest in parent-B order.

    The fill step is inherently sequential per pair (it depends on which
    cities the slice already used), so the loop runs over pairs while the
    membership test inside is vectorized over genes.
    """
    n_pairs, n = pa.shape
    cuts = np.sort(rng.integers(0, n + 1, size=(n_pairs, 2)), axis=1)
    children = np.empty_like(pa)
    for i in range(n_pairs):
        lo, hi = cuts[i]
        segment = pa[i, lo:hi]
        rest = pb[i][~np.isin(pb[i], segment)]
        children[i, lo:hi] = segment
        children[i, :lo] = rest[:lo]
        children[i, hi:] = rest[lo:]
    return children


def inversion_mutation(
    children: Array, rng: np.random.Generator, p: float = 0.3
) -> Array:
    """Reverse one random segment of each child with probability p.

    Segment reversal changes only two tour edges -- the gentlest useful
    permutation mutation for adjacency-driven objectives like the TSP.
    """
    n_children, n = children.shape
    out = children.copy()
    cuts = np.sort(rng.integers(0, n, size=(n_children, 2)), axis=1)
    for i in np.flatnonzero(rng.random(n_children) < p):
        lo, hi = cuts[i]
        out[i, lo : hi + 1] = out[i, lo : hi + 1][::-1]
    return out


def nearest_neighbor_tour(dist: Array, start: int) -> Array:
    """Greedy nearest-neighbor tour, used to seed a few individuals."""
    n = dist.shape[0]
    unvisited = np.ones(n, dtype=bool)
    tour = np.empty(n, dtype=np.int64)
    tour[0] = start
    unvisited[start] = False
    for i in range(1, n):
        row = np.where(unvisited, dist[tour[i - 1]], np.inf)
        tour[i] = int(np.argmin(row))
        unvisited[tour[i]] = False
    return tour
```

Before wiring anything into the loop, verify the operator's contract in isolation — a recombination bug that silently produces invalid permutations is the most expensive GA bug to find later, because the run "works" and merely returns garbage tours:

```python
import numpy as np

# Uses order_crossover from the operator block above.


def ox_demo() -> None:
    """Show that OX output is a valid permutation and what it inherits."""
    pa = np.array([[3, 0, 6, 2, 5, 1, 4, 7]])
    pb = np.array([[2, 7, 5, 0, 3, 4, 1, 6]])
    child = order_crossover(pa, pb, np.random.default_rng(8))[0]
    assert sorted(child.tolist()) == list(range(8)), "child must be a permutation"
    print("parent A", pa[0])
    print("parent B", pb[0])
    print("child   ", child)


if __name__ == "__main__":
    ox_demo()
# Expected: child [7 0 6 2 5 1 3 4]. Positions 2:6 carry parent A's slice
# [6 2 5 1] unchanged, and the remaining cities 7, 0, 3, 4 appear in exactly
# the relative order parent B visits them. The assert is the regression test
# worth keeping.
```

Wiring the operators into the framework takes one function. Seeding a handful of individuals with nearest-neighbor tours gives crossover good material from generation zero without collapsing diversity (keep seeded individuals below ~10% of N):

```python
import numpy as np

# Uses run_ga / tournament_selection from the framework block and the
# TSP instance, operators, and construction heuristic defined above.


def solve_tsp(
    dist: np.ndarray, pop_size: int = 100, n_generations: int = 400, seed: int = 1
) -> tuple[np.ndarray, float]:
    """Permutation GA for the TSP: OX + inversion mutation + NN seeding."""
    n = dist.shape[0]

    def init(rng: np.random.Generator) -> np.ndarray:
        pop = np.array([rng.permutation(n) for _ in range(pop_size)])
        starts = rng.choice(n, size=min(5, pop_size), replace=False)
        for j, start in enumerate(starts):
            pop[j] = nearest_neighbor_tour(dist, int(start))
        return pop

    def evaluate(pop: np.ndarray) -> np.ndarray:
        return tour_lengths(pop, dist)

    best, best_len, _history = run_ga(
        init,
        evaluate,
        order_crossover,
        inversion_mutation,
        n_generations=n_generations,
        tournament_k=4,
        crossover_rate=0.9,
        n_elites=2,
        seed=seed,
    )
    return best, best_len


if __name__ == "__main__":
    dist = circle_instance(n=15, seed=7)
    tour, length = solve_tsp(dist)
    optimum = float(tour_lengths(np.arange(15)[None, :], dist)[0])
    print(f"GA tour length {length:.4f}   angular optimum {optimum:.4f}")
# Expected: GA length equals the angular-order optimum on this 15-city circle.
```

Scaling notes: on random Euclidean instances beyond ~100 cities, this plain GA lands several percent above 2-opt local optima — the documented weakness of crossover-only search on the TSP. The fix is not more generations but a memetic design (2-opt applied to offspring; see memetic-algorithms) or an edge-preserving crossover such as ERX (see crossover-operators). Treat this example as the pattern for permutation problems, not as a competitive TSP solver.

## Worked Example: 0-1 Knapsack with Penalty and Repair

Binary encoding fits the knapsack directly: gene $j$ = item $j$ selected. The design question is constraint handling, and the knapsack is the classic head-to-head between the two standard answers (Michalewicz & Arabas 1994, "Genetic Algorithms for the 0/1 Knapsack Problem"):

- **Static penalty.** Minimize $-\sum_j v_j x_j + \rho \max(0, \sum_j w_j x_j - W)$. With $\rho$ above the best value-per-weight ratio, dropping an item from an overloaded knapsack pays whenever the excess still exceeds that item's weight, so the penalty pulls the search toward the capacity boundary. The guarantee is one-sided, though: a solution slightly *over* capacity can still out-score the true optimum — its value grows by a whole item while the penalty charges only the small excess — so the penalized optimum may be an infeasible genotype. A final repair pass is therefore mandatory, not cosmetic. With continuous weights no finite $\rho$ removes this effect; exactness needs integer weights and a near-death penalty $\rho > \sum_j v_j$, which in turn blocks the useful crossings of the infeasible region that motivated a graded penalty in the first place.
- **Greedy repair (Lamarckian).** Drop selected items in worst value/weight order until feasible, then add unselected items in best-ratio order while they fit. Writing the repaired genotype back into the population (Lamarckian writeback) keeps the gene pool feasible and effectively shrinks the search space.

```python
import numpy as np

Array = np.ndarray


def knapsack_instance(n: int, seed: int) -> tuple[Array, Array, float]:
    """Weakly correlated 0-1 knapsack; capacity is half the total weight."""
    rng = np.random.default_rng(seed)
    weights = rng.uniform(1.0, 30.0, size=n)
    values = np.maximum(weights + rng.uniform(-5.0, 15.0, size=n), 1.0)
    return values, weights, 0.5 * float(weights.sum())


def brute_force_optimum(values: Array, weights: Array, capacity: float) -> float:
    """Exact optimum by enumerating all 2^n subsets (use only for n <= ~20)."""
    n = values.shape[0]
    masks = (np.arange(2**n)[:, None] >> np.arange(n)) & 1
    total_value = masks @ values
    total_value[masks @ weights > capacity] = -np.inf
    return float(total_value.max())


def penalty_cost(
    pop: Array, values: Array, weights: Array, capacity: float, rho: float
) -> Array:
    """Static-penalty cost (minimization) for an (N, n) binary population."""
    excess = np.maximum(0.0, pop @ weights - capacity)
    return -(pop @ values) + rho * excess


def greedy_repair(
    pop: Array, values: Array, weights: Array, capacity: float
) -> Array:
    """Repair + fill: keep, then add, items in value/weight order while they fit.

    The fit test depends on the running load (a prefix dependence), so the
    loop runs over the n items in ratio order while every step is vectorized
    across the whole population. Output is always feasible.
    """
    order = np.argsort(-(values / weights))
    repaired = np.zeros_like(pop)
    load = np.zeros(pop.shape[0])
    for j in order:                                   # keep selected items that fit
        take = (pop[:, j] == 1) & (load + weights[j] <= capacity)
        repaired[:, j] = take
        load += np.where(take, weights[j], 0.0)
    for j in order:                                   # greedy fill with the rest
        add = (repaired[:, j] == 0) & (load + weights[j] <= capacity)
        repaired[:, j] += add
        load += np.where(add, weights[j], 0.0)
    return repaired
```

The GA itself reuses the framework; only the hooks differ between the two constraint-handling modes. In repair mode, repair is folded into the mutation hook and the initial population, so every evaluated genotype is feasible:

```python
import numpy as np

# Uses run_ga from the framework block and the knapsack helpers above.


def solve_knapsack(
    values: np.ndarray,
    weights: np.ndarray,
    capacity: float,
    mode: str = "repair",
    pop_size: int = 80,
    n_generations: int = 150,
    seed: int = 3,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Binary GA for the 0-1 knapsack; mode is 'penalty' or 'repair'.

    Returns (best solution, its value, best-cost-per-generation history).
    """
    n = values.shape[0]
    rho = 2.0 * float((values / weights).max())

    def raw_init(rng: np.random.Generator) -> np.ndarray:
        return (rng.random((pop_size, n)) < 0.3).astype(np.int8)

    def uniform_crossover(
        pa: np.ndarray, pb: np.ndarray, rng: np.random.Generator
    ) -> np.ndarray:
        mask = rng.random(pa.shape) < 0.5
        return np.where(mask, pa, pb)

    def bit_flip(children: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        flip = rng.random(children.shape) < 1.0 / n
        return np.where(flip, 1 - children, children).astype(np.int8)

    if mode == "repair":

        def init(rng: np.random.Generator) -> np.ndarray:
            return greedy_repair(raw_init(rng), values, weights, capacity)

        def evaluate(pop: np.ndarray) -> np.ndarray:
            return -(pop @ values)

        def mutate(children: np.ndarray, rng: np.random.Generator) -> np.ndarray:
            return greedy_repair(bit_flip(children, rng), values, weights, capacity)

    else:  # static penalty
        init, mutate = raw_init, bit_flip

        def evaluate(pop: np.ndarray) -> np.ndarray:
            return penalty_cost(pop, values, weights, capacity, rho)

    best, _cost, hist = run_ga(
        init, evaluate, uniform_crossover, mutate,
        n_generations=n_generations, seed=seed,
    )
    if best @ weights > capacity:                     # penalty mode can end infeasible
        best = greedy_repair(best[None, :], values, weights, capacity)[0]
    return best, float(best @ values), hist


if __name__ == "__main__":
    values, weights, capacity = knapsack_instance(n=15, seed=11)
    optimum = brute_force_optimum(values, weights, capacity)
    for mode in ("penalty", "repair"):
        sol, val, _hist = solve_knapsack(values, weights, capacity, mode=mode)
        feasible = bool(sol @ weights <= capacity + 1e-9)
        print(f"{mode:8s} value {val:.1f}  feasible {feasible}  optimum {optimum:.1f}")
# Expected: repair reaches the brute-force optimum (172.4 on this instance).
# Penalty converges onto an infeasible genotype just over capacity -- its
# penalized cost is below -optimum -- and the final repair pass projects it to
# 171.6, about 0.4% short: the one-sided guarantee failing exactly as described.
```

The comparison should be measured, not asserted — and each run must be judged by its *returned feasible value*, never by the cost history: a penalty run's history can dip below $-z^*$ on the back of an infeasible elite, which would silently overstate the penalty GA. Counting solved seeds at three budgets makes the difference unambiguous:

```python
import numpy as np

# Uses knapsack_instance, brute_force_optimum, and solve_knapsack from above.


def solved_count(
    mode: str,
    n_generations: int,
    values: np.ndarray,
    weights: np.ndarray,
    capacity: float,
    optimum: float,
    n_seeds: int = 10,
) -> int:
    """Seeds (out of n_seeds) whose returned feasible value hits the optimum."""
    return sum(
        solve_knapsack(
            values, weights, capacity,
            mode=mode, n_generations=n_generations, seed=s,
        )[1] >= optimum - 1e-6
        for s in range(n_seeds)
    )


def budget_comparison(n_items: int = 15) -> None:
    """Solved-seed counts at three evaluation budgets, penalty vs repair."""
    values, weights, capacity = knapsack_instance(n_items, seed=11)
    optimum = brute_force_optimum(values, weights, capacity)
    print("generations  penalty  repair   (seeds solved out of 10)")
    for budget in (10, 30, 150):
        p = solved_count("penalty", budget, values, weights, capacity, optimum)
        r = solved_count("repair", budget, values, weights, capacity, optimum)
        print(f"{budget:11d} {p:8d} {r:7d}")


if __name__ == "__main__":
    budget_comparison()
# Expected: repair solves more than half the seeds already at 10 generations
# and all 10 seeds from 30 generations on. Penalty solves almost none at any
# budget on this instance: more generations only deepen its convergence onto
# the infeasible attractor, and the final repair projection lands ~0.4% short.
```

What generalizes from this comparison: repair dominates when a cheap, deterministic repair exists and the feasible region is easy to project onto. Penalties remain necessary when no sensible repair exists (complex joint constraints) or when crossing infeasible regions genuinely helps; then prefer adaptive penalties over hand-tuned static ones, and pair them with feasibility rules in selection (feasible beats infeasible) so the population cannot settle on an infeasible attractor the way it does here. The full decision guide is in constraint-handling-techniques.

## Advanced Techniques

### Diversity monitoring, random immigrants, and restarts

Premature convergence is the canonical GA failure: selection plus elitism collapses the population onto one basin long before the budget ends. Measure diversity every generation — for binary encodings the mean per-gene heterozygosity $\overline{2p(1-p)}$ is a one-liner — and act on it instead of staring at a flat convergence curve. Cheap interventions, in increasing order of force: raise the mutation rate while diversity is low, replace the worst few percent with random immigrants (Grefenstette 1992, random immigrants for nonstationary GAs), and finally restart around the elite set, CHC-style (Eshelman 1991). The diversity-and-population-management skill covers sharing, crowding, and niching for multimodal landscapes.

```python
import numpy as np
from typing import Callable


def gene_diversity(pop: np.ndarray) -> float:
    """Mean per-gene heterozygosity 2*p*(1-p) of a binary population, in [0, 0.5]."""
    p = pop.mean(axis=0)
    return float((2.0 * p * (1.0 - p)).mean())


def adaptive_mutation_rate(
    base_rate: float, div: float, low: float = 0.02, high: float = 0.15
) -> float:
    """Scale the per-gene mutation rate up to 5x as diversity falls below `high`."""
    if div >= high:
        return base_rate
    return base_rate * (1.0 + 4.0 * min(1.0, (high - div) / (high - low)))


def inject_random_immigrants(
    pop: np.ndarray,
    cost: np.ndarray,
    evaluate: Callable[[np.ndarray], np.ndarray],
    rng: np.random.Generator,
    fraction: float = 0.1,
) -> None:
    """Replace the worst `fraction` of a binary population with random individuals."""
    n_new = max(1, int(fraction * pop.shape[0]))
    worst = np.argsort(cost)[-n_new:]
    pop[worst] = rng.integers(0, 2, size=(n_new, pop.shape[1])).astype(pop.dtype)
    cost[worst] = evaluate(pop[worst])
```

### Adaptive operator probabilities

Fixed $p_c$ and $p_m$ are rarely optimal across a whole run. Srinivas & Patnaik (1994), "Adaptive Probabilities of Crossover and Mutation in Genetic Algorithms," scale both rates per individual: low for above-average individuals (protect them), high for below-average ones (disrupt them). A simpler population-level rule that captures most of the benefit: couple $p_m$ to the diversity signal as in `adaptive_mutation_rate` above, and leave $p_c$ fixed. If many operators compete (several crossovers, several mutations), use an adaptive operator-selection scheme with credit assignment — the same machinery as adaptive large neighborhood search — rather than hand-picking one.

### Fitness scaling and rank-based selection

If fitness-proportionate selection must be used (legacy code, comparison studies), it needs scaling to survive both early dominance by one super-individual and late fitness clustering: sigma scaling $f' = \max(0, f - (\bar f - c\sigma_f))$ with $c \approx 2$, or Boltzmann scaling with a temperature schedule. Linear ranking (Baker 1985) and tournament selection sidestep the problem entirely because they are invariant to monotone fitness transformations — the practical reason tournament is the default. See selection-and-replacement-strategies for selection-intensity formulas across schemes.

### Steady-state replacement and duplicate control

The generational loop above replaces N - e individuals per step. The steady-state alternative (Whitley 1989, GENITOR) inserts one offspring at a time, replacing the worst (or a random below-median) individual — higher selection pressure, faster incorporation of good genes, and a natural fit for expensive evaluations and parallel evaluation farms. Two practical guards matter more than the generational/steady-state choice itself: reject offspring identical to an existing individual (duplicates silently destroy diversity at zero apparent cost), and cap the share of the population any single genotype may occupy.

### Hybridizing with local search

The single highest-leverage upgrade to a plain GA on classic combinatorial problems is applying local search to offspring — a memetic algorithm. The GA supplies global recombination; local search supplies the intensification crossover lacks. Budget rule of thumb: spend 50-90% of evaluations inside local search, applied either to every offspring (with a cheap neighborhood) or to a random 5-20% subset (with an expensive one). Lamarckian writeback (store the improved genotype) is the default; Baldwinian (keep the genotype, score the improved fitness) preserves diversity at the price of slower convergence. Full treatment in memetic-algorithms.

## Practical Challenges

**The population collapses to near-identical individuals in the first quarter of the run.** Classic premature convergence. Check, in order: tournament size (drop to k = 2), elite count (cap at 1-2% of N), duplicate offspring (add rejection), and mutation rate (restore the 1/n baseline if it was lowered). Add the diversity monitor from Advanced Techniques and trigger immigrants below a threshold. If the problem is genuinely multimodal and multiple distinct optima matter, move to crowding or fitness sharing (diversity-and-population-management).

**A simple iterated local search baseline beats the GA.** Common and informative. It means crossover is not assembling useful building blocks: either the encoding has poor locality (small genotype changes cause large phenotype jumps — see solution-encodings), or the problem rewards intensification that the GA lacks. First response: make it memetic (add the baseline's local search to the GA). If the memetic GA still loses at equal evaluation budget, the honest conclusion is that recombination adds nothing for this problem — report that and keep the simpler method.

**Standard one-point crossover breaks permutation solutions.** One-point or uniform crossover on permutations produces children with repeated and missing elements. Use a permutation-preserving operator (OX, PMX, CX, ERX — the choice depends on whether position, order, or adjacency carries fitness; see crossover-operators), or switch to a random-key encoding where any real-valued crossover is legal at the cost of a decoding step.

**Fitness evaluation dominates runtime and the GA crawls.** Restructure evaluation as one batch operation on the `(N, n)` population array — the framework is designed for it (see the `tour_lengths` and `penalty_cost` hooks). Then eliminate repeated work: hash genotypes and memoize scores, and never re-evaluate elites. If single evaluations are irreducibly expensive (simulation), shrink N, switch to steady-state replacement, and parallelize evaluation across cores.

**Roulette-wheel selection stops differentiating individuals late in the run.** When all costs cluster within a few percent, proportionate selection degenerates to uniform sampling and progress stalls; with negative or shifted objectives it is biased or undefined. Replace it with tournament or rank selection — both depend only on order and are invariant to objective shifts and scaling.

**Confusion between per-gene and per-individual mutation rates.** For binary strings, the baseline is per-gene: each bit flips independently with $p_m = 1/n$, so each child receives one expected flip (Mühlenbein 1992 analyzes why 1/n is a robust default). For permutations, rates are per-individual: apply one mutation operator (swap, insertion, inversion) to each child with probability 0.1-0.4. Mixing the two conventions produces mutation pressure off by a factor of n.

**The penalty GA returns an infeasible final solution, or never finds the constraint boundary.** A penalty weight too small makes infeasibility profitable; too large walls off the boundary where knapsack-like optima live; and even a correctly graded $\rho$ gives only a one-sided guarantee — the penalized optimum can sit just outside the feasible region, as the worked example demonstrates numerically. Always finish with a repair pass on the returned solution, and judge runs by repaired feasible value, never by raw penalized cost. When the population visibly settles on an infeasible attractor, switch to repair or to feasibility-rules selection (feasible beats infeasible; among infeasible, less violation wins).

**Results change wildly between runs and reviewers ask which number is real.** A GA is a randomized algorithm; report it as one. Fix the evaluation budget, run 10-30 seeds per instance, and report best/mean/std plus the seed list. Pass exactly one `np.random.default_rng(seed)` through the entire run — hidden global randomness (`np.random.*` module calls, Python's `random`) is the usual source of irreproducible results.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| Hand-rolled numpy (this skill) | Research code needing speed and full operator control | ~100 lines; vectorized population ops beat object-per-individual designs by 10-100x |
| DEAP | Rapid composition of EA variants, GP, quick studies | List-based individuals; keep fitness evaluation vectorized yourself or it dominates runtime |
| pymoo | Multi-objective (NSGA-II/III) and constrained EAs | numpy-based, well-maintained; the default once a second objective appears |
| PyGAD | Quick single-objective prototypes, ML-adjacent users | Simple API; limited operator catalog for permutation problems |
| LEAP | Teaching and pipeline-style EA experiments | Readable operator-pipeline design; smaller community |
| inspyred | Lightweight classic EC (GA, ES, PSO) | Stable but low-activity; fine for small studies |
| Optuna / irace | Tuning N, k, rates on a training instance set | Treat GA parameters as a tuning problem; never tune on the reporting instances |

## Output Format

A complete GA deliverable contains four artifacts:

1. **Configuration table** — every design decision and parameter with its value and one-line justification: encoding, selection (scheme, k), crossover (operator, $p_c$), mutation (operator, rate convention, $p_m$), replacement (elitism e), N, budget in evaluations, constraint handling, seeds used. A GA result without its configuration is unverifiable.
2. **Solution report** — best solution found per instance (decoded, human-readable), its objective value recomputed by an independent evaluator (not the GA's internal fitness), feasibility check result, and gap to optimum/best-known where available.
3. **Convergence summary** — per instance: best/mean/std of final cost over seeds, mean generation of last improvement (a budget-was-too-long indicator), and final population diversity. Plot best-so-far curves with a band over seeds when figures are wanted.
4. **Reproducibility block** — instance generator seeds, algorithm seeds, code version, and the exact command. One row per run in a tidy table:

```python
import pandas as pd


def summarize_runs(records: list[dict]) -> pd.DataFrame:
    """Aggregate one-row-per-run GA results into a per-instance summary table."""
    df = pd.DataFrame.from_records(records)
    grouped = df.groupby(["instance", "algorithm"])["best_cost"]
    return grouped.agg(best="min", mean="mean", std="std", runs="size").reset_index()


records = [
    {"instance": "kp15_a", "algorithm": "ga_penalty", "seed": s, "best_cost": c}
    for s, c in enumerate([-486.2, -486.2, -480.9, -486.2, -484.5])
] + [
    {"instance": "kp15_a", "algorithm": "ga_repair", "seed": s, "best_cost": c}
    for s, c in enumerate([-486.2] * 5)
]
print(summarize_runs(records))
# Expected: ga_repair shows best == mean == -486.2 with std 0.0 over 5 runs;
# ga_penalty shows the same best with nonzero std -- the spread is the story.
```

## Questions to Ask

- What does one solution look like — a subset, a permutation, an assignment, a schedule? What encoding follows naturally?
- Which constraints exist, and for each: enforce by encoding, repair, or penalize?
- How expensive is one fitness evaluation, and can the whole population be evaluated as one array operation?
- What is the total budget — wall-clock seconds or evaluation count — per run?
- Is there a known construction heuristic or local search for this problem that should seed or hybridize the GA?
- What baseline must the GA beat, and at what evaluation budget?
- Is the goal single-objective, or will a second objective appear (then plan for NSGA-II instead)?
- How many instances and seeds will the final report use, and is a statistical comparison against another method required?
- Are GA parameters to be tuned automatically, and on which held-out instances?

## Related Skills

- **crossover-operators** — when choosing or implementing recombination beyond OX and uniform: the full catalog with position/order/adjacency preservation properties per encoding.
- **mutation-and-perturbation-operators** — when designing mutation for a specific encoding or controlling and adapting mutation strength during the run.
- **selection-and-replacement-strategies** — when tuning selection pressure, comparing tournament/rank/roulette/SUS, or switching to steady-state or (mu+lambda) replacement.
- **solution-encodings** — when the representation itself is in question: locality, redundancy, feasibility coverage, and the encoding-operator compatibility matrix.
- **diversity-and-population-management** — when premature convergence appears: diversity measures, fitness sharing, crowding, niching, and restart policies.
- **memetic-algorithms** — when adding local search to the GA, usually the single biggest quality improvement on classic combinatorial benchmarks.
