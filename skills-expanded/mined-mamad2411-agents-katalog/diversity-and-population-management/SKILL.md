---
name: diversity-and-population-management
description: When the user wants to diagnose or prevent premature convergence in population-based metaheuristics by measuring and managing diversity: entropy and distance-based diversity measures, fitness sharing, crowding, niching, duplicate elimination, restart policies, and adaptive parameter control driven by diversity signals. Also use when the user mentions "premature convergence," "diversity," "fitness sharing," "crowding," "niching," "population restart," or when every individual in the population looks the same long before the evaluation budget ends. For selection pressure and replacement schemes, see selection-and-replacement-strategies; for the host GA loop, see genetic-algorithms.
---

# Diversity and Population Management

You are an expert in population management for evolutionary and population-based metaheuristics. This skill is the reference catalog for everything that keeps a population useful: diversity measurement (entropy-based and distance-based), preservation mechanisms (fitness sharing, clearing, crowding, restricted tournament selection, duplicate elimination, mating restrictions), restoration mechanisms (restart policies, random immigrants), and adaptive parameter control wired to diversity signals. For every mechanism it gives when to use it, a numpy implementation, a complexity note, and the algorithms and problem types it fits. Use the measure-preserve-restore framework below to choose mechanisms instead of stacking them blindly.

## Initial Assessment

Establish these facts before recommending or writing any diversity machinery:

- **Decide the actual goal first.** One best solution, or several distinct high-quality solutions (multimodal search, alternatives for a decision maker)? Niching proper (sharing, clearing, crowding) exists for the second goal. For the first goal, cheaper tools — duplicate elimination, sane selection pressure, restarts — usually suffice and cost less.
- **Confirm the diagnosis before treating it.** "The GA stopped improving" has at least three causes: lost diversity (entropy collapsed), a genuinely hard landscape (diversity fine, no better solutions nearby), or broken variation operators. Plot best fitness AND a genotype diversity measure over generations before choosing a fix. If diversity is healthy and search still stalls, this skill is the wrong lever — see fitness-landscape-analysis.
- **Identify the pressure source.** Diversity loss is caused by selection and replacement: tournament size, elitism strength, steady-state replacement of the worst. Takeover time under tournament selection is roughly $\log N / \log t$ generations (Goldberg & Deb 1991, "A Comparative Analysis of Selection Schemes"). Reducing pressure at the source (see selection-and-replacement-strategies) is often cheaper than adding a preservation mechanism on top.
- **Fix the encoding and its distance.** Every mechanism here needs a distance or a frequency count on genotypes. Hamming works for binary/integer strings; permutations need a deliberate choice (positional Hamming vs edge-based); real vectors use Euclidean. Symmetric encodings (rotations/reflections of a tour, relabelable groups) inflate distances between identical solutions — canonicalize first or measure in phenotype space.
- **Establish the evaluation cost.** Restarts and immigrants re-spend evaluations; with an expensive objective, prefer preservation mechanisms that waste nothing (dedup, RTS, crowding). With cheap evaluations, restarts are often the best value per line of code.
- **Establish the population size and budget.** Small populations ($N \le 50$) drift to uniformity even without selection pressure; no sharing parameter rescues that. Large populations make $O(N^2)$ sharing the bottleneck — budget the per-generation overhead against one fitness evaluation.
- **Check the algorithmic context.** A canonical GA, a memetic algorithm (local search collapses diversity much faster), an EDA (diversity lives in model variance — see estimation-of-distribution-algorithms), or scatter search (the reference set already encodes a diversity rule — see scatter-search-path-relinking)? The host determines where the mechanism plugs in.
- **Reproducibility.** Every stochastic component takes an explicit `np.random.Generator`. Restart-policy comparisons without fixed seeds, equal evaluation budgets, and $\ge 10$ repetitions are noise.

## Diversity Mechanics: Measure, Preserve, Restore

### The control loop

Population management is a feedback controller around the metaheuristic:

```text
every generation:
    MEASURE   D  <- genotype diversity (entropy or distance-based, normalized)
              B  <- best fitness;  S <- generations since B improved
    CLASSIFY  healthy     : D in [d_low, d_high], S < patience
              converging  : D < d_low, S small        -> raise variation / lower pressure
              converged   : D < d_low, S >= patience  -> restart (keep elites)
              wandering   : D > d_high, B stalled     -> raise pressure / exploit
    ACT       preserve  every generation  : dedup, crowding/RTS, sharing or clearing
              adapt     when converging   : mutation rate, tournament size, immigrant rate
              restore   when converged    : partial / cataclysmic restart
```

Squillero & Tonda (2016), "Divergence of Character and Premature Convergence," survey this design space; the framework above is the practical reduction: pick one measure, at most one preservation mechanism, one restoration policy, and wire them with hysteresis so they do not fight each other.

### Measures, formally

For a discrete population $X \in \{0,\dots,K-1\}^{N \times n}$ with per-locus value counts $c_{j,v}$ and frequencies $p_{j,v} = c_{j,v}/N$:

$$
H(X) = \frac{1}{n \log_2 K} \sum_{j=1}^{n} \sum_{v=0}^{K-1} -\, p_{j,v} \log_2 p_{j,v}
\qquad \text{(normalized mean per-locus entropy, } H \in [0,1])
$$

$$
\bar{d}(X) = \binom{N}{2}^{-1} \sum_{j=1}^{n} \frac{N^2 - \sum_v c_{j,v}^2}{2}
\qquad \text{(mean pairwise Hamming distance via counts, } O(Nn + nK) \text{ not } O(N^2 n))
$$

For real-valued populations, the moment of inertia $I = \sum_i \lVert x_i - \bar{x} \rVert^2$ satisfies $\sum_{i<l} \lVert x_i - x_l \rVert^2 = N \cdot I$ (Morrison & De Jong 2002, "Measurement of Population Diversity"), so the $O(N^2)$ pairwise sum collapses to one $O(Nn)$ pass through the centroid. Ursem (2002) normalizes the related distance-to-average-point by the search-space diagonal to get a scale-free signal for control.

Both entropy and count-based Hamming are functions of the same per-locus marginals: they detect column-wise convergence but are blind to linkage (two complementary half-populations look maximally diverse). Distance measures on sampled pairs, distinct-genotype counts after canonicalization, and edge-based distances for tours cover what marginals miss. Fitness variance is the cheapest signal but the weakest: it lags genotype collapse and is fooled by neutrality.

### Mechanism master table

| Mechanism | Acts on | Cost / generation | Key parameters | Maintains multiple optima? | Source |
|---|---|---|---|---|---|
| Fitness sharing | selection (fitness derating) | $O(N^2 n)$ | $\sigma_{share}$, $\alpha$ | yes, if $\sigma$ sized right | Goldberg & Richardson (1987) |
| Clearing | selection (winner-takes-niche) | $O(NWn)$, $W$ winners | $\sigma_{clear}$, capacity | yes, sharper than sharing | Pétrowski (1996) |
| Deterministic crowding | replacement | $O(Nn)$ | none | yes, but drift erodes small niches | Mahfoud (1992) |
| Restricted tournament selection | replacement | $O(Nwn)$, window $w$ | $w$ | yes | Harik (1995) |
| Duplicate elimination | replacement / insertion | $O(Nn)$ hashing | distance threshold (optional) | no — keeps spread only | Mauldin (1984) |
| Incest prevention | mating | $O(n)$ per pair | distance threshold, decay | no | Eshelman (1991), CHC |
| Random immigrants | population | $O(\rho N n)$ | replacement fraction $\rho$ | no | Grefenstette (1992) |
| Restarts (partial / cataclysmic) | population | $O(Nn)$ at trigger | trigger, keep fraction | no — sequential exploration | Eshelman (1991) |
| Diversity-guided adaptation | variation parameters | $O(1)$ given the measure | $d_{low}$, $d_{high}$ | no | Ursem (2002) |
| Age layering (ALPS) | population structure | $O(Nn)$ | layers, age gap | indirectly | Hornby (2006) |

### Decision guidance

- **Want several distinct optima** (multimodal design problems, alternative schedules): use a true niching method — clearing or RTS first (cheaper, sharper), fitness sharing when you need the classic stable-niche theory. Size $\sigma$ from the distance histogram (Advanced Techniques).
- **Want one best solution but converge too early**: in order of cost — (1) deduplicate at insertion, (2) reduce selection pressure / weaken elitism, (3) add a restart policy with a stagnation-or-diversity trigger, (4) wire mutation rate to the diversity signal. Skip niching; it slows convergence by design.
- **Expensive objective**: preservation over restoration. RTS and dedup waste zero evaluations; a restart re-pays the whole warm-up.
- **Deceptive or trap-like landscape**: diversity alone does not solve deception — preserved diversity only buys time for good linkage handling. Pair the mechanisms here with linkage-aware methods (see estimation-of-distribution-algorithms) and diagnose first (see fitness-landscape-analysis).
- **Steady-state or memetic host**: replacement-side mechanisms (RTS, crowding, dedup) integrate naturally; generational hosts take selection-side mechanisms (sharing, clearing) with SUS or remainder selection — tournament selection on shared fitness is unstable (Oei, Goldberg & Chang 1991).

## Measuring Diversity

**Use when:** always — every other mechanism in this skill assumes a monitored diversity signal. **Fits:** every population-based method; the discrete measures fit GAs and memetic algorithms on binary/integer/permutation encodings, the centroid measure fits evolution strategies, DE, PSO, and real-coded GAs. **Cost:** all three functions below are $O(Nn)$-class — cheap enough to run every generation.

The count-based identity matters in practice: the number of disagreeing pairs at locus $j$ is $(N^2 - \sum_v c_{j,v}^2)/2$, so mean pairwise Hamming distance needs only the per-locus counts already computed for entropy — never materialize the $N \times N$ distance matrix just to monitor diversity.

```python
import numpy as np


def locus_entropy(pop: np.ndarray, n_values: int) -> float:
    """Normalized mean per-locus Shannon entropy of a discrete (N, n) population.

    Returns a value in [0, 1]: 1.0 = every value equally frequent at every
    locus, 0.0 = N copies of one genotype. Integer-coded genomes. O(N*n + n*K).
    """
    pop = np.asarray(pop, dtype=np.int64)
    n_pop, n = pop.shape
    counts = np.zeros((n, n_values), dtype=np.int64)
    np.add.at(counts, (np.broadcast_to(np.arange(n), (n_pop, n)), pop), 1)
    p = counts / n_pop
    terms = np.where(p > 0, -p * np.log2(p, where=p > 0), 0.0)
    return float(terms.sum(axis=1).mean() / np.log2(n_values))


def mean_pairwise_hamming(pop: np.ndarray, n_values: int) -> float:
    """Mean pairwise Hamming distance, normalized to [0, 1], via locus counts.

    Disagreeing pairs at locus j = (N^2 - sum_v c_jv^2) / 2, so the cost is
    O(N*n + n*K) instead of the naive O(N^2 * n).
    """
    pop = np.asarray(pop, dtype=np.int64)
    n_pop, n = pop.shape
    counts = np.zeros((n, n_values), dtype=np.int64)
    np.add.at(counts, (np.broadcast_to(np.arange(n), (n_pop, n)), pop), 1)
    disagree = (n_pop**2 - (counts**2).sum(axis=1)) / 2.0
    n_pairs = n_pop * (n_pop - 1) / 2.0
    return float(disagree.sum() / (n_pairs * n))


def distance_to_average_point(
    pop: np.ndarray, lower: np.ndarray, upper: np.ndarray
) -> float:
    """Ursem (2002) diversity for a real-valued (N, n) population.

    Mean Euclidean distance to the centroid, normalized by the search-space
    diagonal so thresholds transfer across problems. O(N*n).
    """
    centroid = pop.mean(axis=0)
    diag = float(np.linalg.norm(upper - lower))
    return float(np.linalg.norm(pop - centroid, axis=1).mean() / diag)


# Tiny instance: a random vs a fully converged binary population, N=6, n=8.
rng = np.random.default_rng(0)
random_pop = rng.integers(0, 2, size=(6, 8))
converged = np.tile(random_pop[0], (6, 1))
print(round(locus_entropy(random_pop, 2), 3), locus_entropy(converged, 2))
print(round(mean_pairwise_hamming(random_pop, 2), 3),
      mean_pairwise_hamming(converged, 2))
# Expected: 0.895 entropy and 0.517 normalized Hamming for the random
# population; exactly 0.0 for both measures on the converged one.
```

### Measure selection table

| Measure | Encoding | Cost | Detects | Blind to |
|---|---|---|---|---|
| Per-locus entropy | binary / integer / permutation positions | $O(Nn + nK)$ | column-wise convergence | linkage between loci |
| Count-based mean Hamming | binary / integer | $O(Nn + nK)$ | same signal, distance units | linkage; correlates with entropy |
| Distance to average point / moment of inertia | real vectors | $O(Nn)$ | spatial spread | multimodal clustering shape |
| Sampled pairwise distance (e.g., 200 random pairs) | any with a metric | $O(sn)$, $s$ pairs | joint structure, clusters | rare niches if $s$ small |
| Distinct genotypes after canonicalization | any hashable | $O(Nn)$ | duplicate flooding | near-duplicates |
| Distinct fitness values / fitness std | any | $O(N)$ | total collapse (late) | genotype structure, neutrality |
| Shared-edge fraction across population | permutations as tours | $O(Nn)$ with an edge set | adjacency convergence | positional structure |

Monitor two: one frequency-based (entropy) and one structural (distinct count or sampled distances). For tours, prefer the edge-based measure — positional entropy stays high while every individual encodes nearly the same cycle.

## Preservation Mechanisms

### Fitness sharing

**Use when:** the goal is several stable niches and population size affords $O(N^2)$ distances; the classic choice when niche proportionality matters (subpopulation size grows with niche fitness — Goldberg & Richardson 1987). **Fits:** generational GAs with fitness-proportionate or SUS selection; multimodal continuous and discrete problems. **Cost:** $O(N^2 n)$ time, $O(N^2)$ memory per generation — practical to $N \approx 2000$. Shared fitness for maximization with positive raw fitness:

$$
f_i' = \frac{f_i}{\sum_{j=1}^{N} \operatorname{sh}(d_{ij})},
\qquad
\operatorname{sh}(d) = \begin{cases} 1 - (d/\sigma_{share})^{\alpha} & d < \sigma_{share} \\ 0 & \text{otherwise} \end{cases}
$$

```python
import numpy as np


def shared_fitness(
    fitness: np.ndarray,
    pop: np.ndarray,
    sigma_share: float,
    alpha: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Goldberg & Richardson (1987) fitness sharing, maximization, f >= 0.

    Derates raw fitness by the niche count m_i = sum_j sh(d_ij), Hamming
    distance on discrete genomes. O(N^2 * n) time, O(N^2) memory: fine to
    N ~ 2000; switch to clearing or sampled niche counts beyond that.
    """
    dist = (pop[:, None, :] != pop[None, :, :]).sum(axis=2)
    share = np.where(dist < sigma_share, 1.0 - (dist / sigma_share) ** alpha, 0.0)
    niche_count = share.sum(axis=1)          # self-distance 0 contributes 1.0
    return fitness / niche_count, niche_count


# Tiny instance: a crowded niche gets derated, an isolated optimum does not.
pop = np.array([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [1, 1, 1, 1]])
fitness = np.array([4.0, 3.0, 3.0, 4.0])
f_shared, m = shared_fitness(fitness, pop, sigma_share=2.5)
print(np.round(f_shared, 2), np.round(m, 2))
# Expected: the isolated [1,1,1,1] keeps 4.0 (niche count 1.0); the three
# clustered genotypes are derated to ~1.7-1.9 (niche counts 1.8-2.2).
```

Pair sharing with stochastic universal sampling, not tournaments: under tournament selection the niche counts change as the tournament composition changes, and the equilibrium that makes sharing attractive disappears (Oei, Goldberg & Chang 1991, "Tournament Selection, Niching, and the Preservation of Diversity").

### Clearing

**Use when:** you want hard niche caps rather than proportional derating, or $N$ is too large for full sharing. Clearing keeps the best `capacity` individuals per niche at full fitness and zeroes the rest — a winner-takes-niche rule that preserves elite quality inside each niche better than sharing (Pétrowski 1996, "A Clearing Procedure as a Niching Method for Genetic Algorithms"). **Fits:** generational GAs, memetic algorithms (clearing tolerates local search well). **Cost:** $O(NWn)$ with $W$ niche winners — usually far below $O(N^2 n)$.

```python
import numpy as np


def clearing(
    fitness: np.ndarray,
    pop: np.ndarray,
    sigma_clear: float,
    capacity: int = 1,
) -> np.ndarray:
    """Petrowski (1996) clearing for maximization with fitness >= 0.

    Scans best-first; an individual within sigma_clear (Hamming) of a niche
    winner consumes niche capacity or has its fitness cleared to 0. Returns
    the cleared fitness vector, ready for any standard selection scheme.
    O(N * W * n) with W winners.
    """
    order = np.argsort(-fitness)
    cleared = fitness.astype(float).copy()
    winners: list[int] = []
    counts: list[int] = []
    for i in order:
        if winners:
            d = (pop[winners] != pop[i][None, :]).sum(axis=1)
            j = int(np.argmin(d))
            if d[j] < sigma_clear:
                if counts[j] < capacity:
                    counts[j] += 1
                else:
                    cleared[i] = 0.0
                continue
        winners.append(int(i))
        counts.append(1)
    return cleared


# Tiny instance: two niches, capacity 1 -> one survivor per niche.
pop = np.array([[0, 0, 0, 0], [0, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 0]])
fit = np.array([4.0, 3.5, 3.8, 3.0])
print(clearing(fit, pop, sigma_clear=2, capacity=1))
# Expected: [4.0, 0.0, 3.8, 0.0] — the runner-up in each niche is cleared.
```

### Crowding and restricted tournament selection

**Use when:** the host is steady-state or you want niching with zero distance parameters. Deterministic crowding (Mahfoud 1992, "Crowding and Preselection Revisited") makes each child compete only with its more similar parent; restricted tournament selection (Harik 1995, "Finding Multimodal Solutions Using Restricted Tournament Selection") inserts each child over the most similar of `w` random incumbents. RTS is the strongest cheap default in this catalog: one parameter, no $\sigma$, works inside any steady-state loop. **Fits:** steady-state GAs, memetic algorithms, hybrid frameworks. **Cost:** crowding $O(Nn)$ per generation; RTS $O(wn)$ per insert. Do not confuse either with NSGA-II "crowding distance," which measures objective-space density in multi-objective ranking — a different object entirely.

```python
import numpy as np
from collections.abc import Callable


def deterministic_crowding_step(
    pop: np.ndarray,
    fitness: np.ndarray,
    variate: Callable[
        [np.ndarray, np.ndarray, np.random.Generator],
        tuple[np.ndarray, np.ndarray],
    ],
    evaluate: Callable[[np.ndarray], np.ndarray],
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """One generation of deterministic crowding (Mahfoud 1992), maximization.

    Random parent pairing; children are matched to parents by total Hamming
    distance and replace them only if at least as fit. Parameter-free niching
    through replacement. O(N * n) plus N child evaluations.
    """
    pop, fitness = pop.copy(), fitness.copy()
    order = rng.permutation(len(pop))
    for a, b in zip(order[0::2], order[1::2]):
        c1, c2 = variate(pop[a], pop[b], rng)
        f1, f2 = float(evaluate(c1[None, :])[0]), float(evaluate(c2[None, :])[0])
        d_same = int((pop[a] != c1).sum() + (pop[b] != c2).sum())
        d_cross = int((pop[a] != c2).sum() + (pop[b] != c1).sum())
        if d_cross < d_same:
            c1, c2, f1, f2 = c2, c1, f2, f1
        if f1 >= fitness[a]:
            pop[a], fitness[a] = c1, f1
        if f2 >= fitness[b]:
            pop[b], fitness[b] = c2, f2
    return pop, fitness


def rts_insert(
    pop: np.ndarray,
    fitness: np.ndarray,
    child: np.ndarray,
    child_fit: float,
    window: int,
    rng: np.random.Generator,
) -> None:
    """Restricted tournament selection insert (Harik 1995), in place.

    The child replaces the most similar of `window` random incumbents, and
    only if at least as fit. window ~ N/10 to N/5. O(window * n) per insert.
    """
    idx = rng.integers(0, len(pop), size=window)
    d = (pop[idx] != child[None, :]).sum(axis=1)
    j = idx[np.argmin(d)]
    if child_fit >= fitness[j]:
        pop[j] = child
        fitness[j] = child_fit


# Tiny instance: an all-ones child enters a random onemax population via RTS.
rng = np.random.default_rng(1)
pop = rng.integers(0, 2, size=(8, 10))
fit = pop.sum(axis=1).astype(float)
rts_insert(pop, fit, np.ones(10, dtype=pop.dtype), 10.0, window=4, rng=rng)
print(fit.max())
# Expected: 10.0 — the child replaced its nearest window member, not the
# global worst, so distant genotypes stay untouched.
```

### Duplicate elimination and mating restrictions

**Use when:** always, essentially — duplicate genotypes pay evaluation cost for zero information and accelerate takeover. Mauldin (1984), "Maintaining the Diversity of Genetic Search," showed uniqueness enforcement alone substantially delays convergence. The distance-threshold variant below is exactly the diversity rule scatter search applies to its reference set (see scatter-search-path-relinking). CHC's incest prevention (Eshelman 1991, "The CHC Adaptive Search Algorithm") blocks matings between near-identical parents instead of filtering offspring. **Fits:** every discrete-encoding method; mandatory for small search spaces and decoder encodings where many genotypes collide. **Cost:** exact dedup $O(Nn \log N)$ via row sort or $O(Nn)$ via hashing; threshold filter $O(NMn)$ with $M$ survivors.

```python
import numpy as np


def dedup_exact(pop: np.ndarray, fitness: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Remove exact genotype duplicates, keeping first occurrences.

    np.unique over rows, O(N n log N). Canonicalize symmetric encodings
    first, or duplicates survive in disguise.
    """
    _, idx = np.unique(pop, axis=0, return_index=True)
    keep = np.sort(idx)
    return pop[keep], fitness[keep]


def canonical_tour(perm: np.ndarray) -> np.ndarray:
    """Canonical form of a cyclic, direction-symmetric tour. O(n).

    Rotates city 0 to the front, then orients so the second city is smaller
    than the last: all 2n encodings of one undirected tour collapse to one.
    """
    t = np.roll(perm, -int(np.argmax(perm == 0)))
    if t[1] > t[-1]:
        t = np.roll(t[::-1], 1)
    return t


def dedup_threshold(
    pop: np.ndarray, fitness: np.ndarray, min_dist: int
) -> tuple[np.ndarray, np.ndarray]:
    """Greedy best-first filter: survivors are pairwise >= min_dist apart.

    The scatter-search reference-set diversity rule. Maximization; survivors
    returned best-first. O(N * M * n) with M survivors.
    """
    kept: list[int] = []
    for i in np.argsort(-fitness):
        if not kept:
            kept.append(int(i))
            continue
        d = (pop[kept] != pop[i][None, :]).sum(axis=1)
        if int(d.min()) >= min_dist:
            kept.append(int(i))
    return pop[kept], fitness[kept]


def incest_ok(pa: np.ndarray, pb: np.ndarray, threshold: int) -> bool:
    """CHC incest prevention (Eshelman 1991): mate only if parents differ.

    Mating is allowed when half the Hamming distance exceeds the threshold;
    CHC starts at n/4 and decrements it each generation that produces no
    accepted offspring. Threshold 0 means: trigger a cataclysmic restart.
    """
    return int((pa != pb).sum()) // 2 > threshold


# Tiny instance: two encodings of the same undirected 5-city tour.
a = np.array([2, 3, 0, 1, 4])
b = np.array([1, 0, 3, 2, 4])
print(canonical_tour(a), canonical_tour(b))
# Expected: identical canonical forms [0 1 4 2 3] for both — without
# canonicalization, dedup_exact would treat them as distinct.
```

## Restoration and Adaptation

### Restart policies

**Use when:** diversity is already gone, or the method is cheap to warm up and the landscape has many basins. A restart converts one long stuck run into several independent or warm-started short runs. The three reusable building blocks: a trigger (stagnation counter, diversity floor, or fixed schedule), a constructor for the new population (uniform redraw keeping elites; or CHC's cataclysm — mutated copies of the incumbent), and hysteresis so triggers do not fire repeatedly. Random immigrants (Grefenstette 1992, "Genetic Algorithms for Changing Environments") are a continuous micro-restart: replace a fraction of the worst every generation. **Fits:** GAs, memetic algorithms, ILS-style hosts; pycma ships the same idea for CMA-ES as IPOP/BIPOP. **Cost:** $O(Nn)$ at each trigger plus the re-spent evaluations — the real cost.

```python
import numpy as np
from dataclasses import dataclass


@dataclass
class RestartMonitor:
    """Restart trigger: stagnation counter OR diversity floor, with cooldown.

    Fires when no improvement for `patience` generations or when the supplied
    diversity drops below `d_min`. After firing, triggers are suppressed for
    `cooldown` generations so one collapse causes one restart, not five.
    """
    patience: int = 50
    d_min: float = 0.05
    cooldown: int = 20
    best: float = -np.inf
    stale: int = 0
    quiet: int = 0

    def update(self, best_fit: float, diversity: float) -> bool:
        """Feed one generation's stats; True means restart now."""
        if best_fit > self.best + 1e-12:
            self.best, self.stale = best_fit, 0
        else:
            self.stale += 1
        if self.quiet > 0:
            self.quiet -= 1
            return False
        if self.stale >= self.patience or diversity < self.d_min:
            self.stale, self.quiet = 0, self.cooldown
            return True
        return False


def partial_restart(
    pop: np.ndarray, fitness: np.ndarray, keep_frac: float, rng: np.random.Generator
) -> np.ndarray:
    """Keep-elite restart: retain the top keep_frac, redraw the rest uniformly.

    Progress is kept, the basin is reopened. keep_frac 0.05-0.2 is typical;
    larger values drag the new population straight back into the old basin.
    """
    n_pop, n = pop.shape
    n_keep = max(1, int(keep_frac * n_pop))
    elite = pop[np.argsort(-fitness)[:n_keep]]
    fresh = rng.integers(0, 2, size=(n_pop - n_keep, n), dtype=pop.dtype)
    return np.vstack([elite, fresh])


def cataclysmic_restart(
    best: np.ndarray, n_pop: int, flip_frac: float, rng: np.random.Generator
) -> np.ndarray:
    """CHC cataclysm (Eshelman 1991): population = heavily mutated incumbent.

    Each individual is the best solution with ~flip_frac of its bits flipped
    (0.35 is the published default); index 0 keeps one unmutated copy. Stays
    near the incumbent's basin family rather than restarting from scratch.
    """
    flips = rng.random((n_pop, best.size)) < flip_frac
    new_pop = np.where(flips, 1 - best[None, :], best[None, :]).astype(best.dtype)
    new_pop[0] = best
    return new_pop


def random_immigrants(
    pop: np.ndarray, fitness: np.ndarray, frac: float, rng: np.random.Generator
) -> np.ndarray:
    """Grefenstette (1992): replace the worst `frac` with uniform genotypes.

    A continuous trickle of raw material; pair with replacement that does not
    instantly kill immigrants (steady-state with RTS, or protected ages).
    """
    n_new = max(1, int(frac * len(pop)))
    worst = np.argsort(fitness)[:n_new]
    pop = pop.copy()
    pop[worst] = rng.integers(0, 2, size=(n_new, pop.shape[1]), dtype=pop.dtype)
    return pop


# Tiny instance: the monitor fires on stagnation, then cools down.
mon = RestartMonitor(patience=3, d_min=0.01, cooldown=2)
print([mon.update(10.0, 0.5) for _ in range(5)])
# Expected: [False, False, False, True, False] — the counter reaches
# patience at the fourth call, fires once, then cooldown suppresses.
```

### Diversity-guided parameter control

**Use when:** the run alternates between needing exploitation and needing fresh variation, and you would rather steer mutation/selection than rebuild the population. Ursem (2002), "Diversity-Guided Evolutionary Algorithms" (DGEA), runs two phases: exploit (selection + recombination) while diversity exceeds $d_{low}$, explore (high mutation, no selection pressure) until diversity recovers above $d_{high}$. The $d_{low} < d_{high}$ gap is hysteresis — without it the controller thrashes at the boundary. The continuous variant maps the diversity deficit straight onto a mutation rate. **Fits:** real-coded EAs and GAs with a normalized diversity signal; the same pattern drives adaptive immigrant rates and adaptive tournament sizes. **Cost:** $O(1)$ on top of the measurement.

```python
import numpy as np
from dataclasses import dataclass


@dataclass
class DiversityGuidedControl:
    """Two-mode controller after Ursem (2002), DGEA.

    mode() returns 'exploit' (selection + crossover, low mutation) or
    'explore' (no selection pressure, high mutation). Switches to explore
    when diversity <= d_low; back to exploit when diversity >= d_high.
    """
    d_low: float = 0.05
    d_high: float = 0.25
    exploring: bool = False

    def mode(self, diversity: float) -> str:
        """Classify the coming generation from the current diversity."""
        if self.exploring and diversity >= self.d_high:
            self.exploring = False
        elif not self.exploring and diversity <= self.d_low:
            self.exploring = True
        return "explore" if self.exploring else "exploit"


def diversity_scaled_mutation(
    diversity: float, d_target: float, p_min: float, p_max: float
) -> float:
    """Continuous controller: map the diversity deficit to a mutation rate.

    Returns p_min when diversity >= d_target, rising linearly to p_max as
    diversity falls to 0. Smooth alternative to DGEA's mode switch.
    """
    deficit = max(0.0, 1.0 - diversity / d_target)
    return p_min + (p_max - p_min) * deficit


ctrl = DiversityGuidedControl(d_low=0.1, d_high=0.3)
print([ctrl.mode(d) for d in (0.5, 0.2, 0.08, 0.2, 0.35, 0.2)])
# Expected: ['exploit', 'exploit', 'explore', 'explore', 'exploit', 'exploit']
# — the hysteresis band [0.1, 0.3] keeps the mode stable in between.
print(round(diversity_scaled_mutation(0.05, 0.2, 0.01, 0.2), 4))
# Expected: 0.1525 — a 75% deficit maps to p_min + 0.75 * (p_max - p_min).
```

## Worked Example: Diversity-Monitored GA on a Deceptive Trap

The concatenated trap-5 function is the canonical premature-convergence demonstration: each 5-bit block scores 5 for all ones, otherwise $4 - u$ for $u$ ones — so the gradient inside every block points to all-zeros while the optimum is all-ones. The GA below deliberately uses strong pressure (tournament-8) so the failure is visible: the generational variant follows the deceptive gradient, converges block-wise within ~10 generations, and its entropy curve documents the collapse. Switching only the replacement rule to RTS keeps competing block patterns alive and converts that diversity into measurably better solutions at an identical budget.

```python
import numpy as np


def trap_fitness(pop: np.ndarray, k: int = 5) -> np.ndarray:
    """Concatenated deceptive trap-k, maximize. Block of k ones scores k,
    otherwise k - 1 - u for u ones. Global optimum = all ones = n."""
    n_pop, n = pop.shape
    u = pop.reshape(n_pop, n // k, k).sum(axis=2)
    return np.where(u == k, k, k - 1 - u).sum(axis=1).astype(float)


def binary_entropy(pop: np.ndarray) -> float:
    """Normalized mean per-locus entropy of a 0/1 population."""
    p = pop.mean(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return float(np.nan_to_num(h).mean())


def run_trap_ga(
    n_bits: int = 50,
    n_pop: int = 200,
    n_gen: int = 300,
    replacement: str = "generational",
    seed: int = 0,
) -> dict[str, float | None]:
    """Trap-5 GA with per-generation diversity monitoring.

    'generational': tournament-8, uniform crossover, 0.5/n bit-flip, 2
    elites — strong pressure, on purpose, so the collapse is visible.
    'rts': same variation, children inserted via restricted tournament
    selection with window N//10 — the only change is the replacement rule.
    """
    rng = np.random.default_rng(seed)
    pop = rng.integers(0, 2, size=(n_pop, n_bits), dtype=np.int8)
    fit = trap_fitness(pop)
    p_mut = 0.5 / n_bits
    entropy_log: list[float] = []
    for _ in range(n_gen):
        cand = rng.integers(0, n_pop, size=(2 * n_pop, 8))
        parents = cand[np.arange(2 * n_pop), np.argmax(fit[cand], axis=1)]
        pa, pb = pop[parents[:n_pop]], pop[parents[n_pop:]]
        children = np.where(rng.random(pa.shape) < 0.5, pa, pb)
        children ^= (rng.random(children.shape) < p_mut).astype(np.int8)
        child_fit = trap_fitness(children)
        if replacement == "generational":
            elite = np.argsort(-fit)[:2]
            children[:2], child_fit[:2] = pop[elite], fit[elite]
            pop, fit = children, child_fit
        else:
            w = max(5, n_pop // 10)
            for c, cf in zip(children, child_fit):
                idx = rng.integers(0, n_pop, size=w)
                j = idx[np.argmin((pop[idx] != c[None, :]).sum(axis=1))]
                if cf >= fit[j]:
                    pop[j], fit[j] = c, cf
        entropy_log.append(binary_entropy(pop))
    collapse = [g for g, h in enumerate(entropy_log) if h < 0.1]
    return {"best": float(fit.max()), "final_entropy": entropy_log[-1],
            "collapse_gen": float(collapse[0]) if collapse else None}


for mode in ("generational", "rts"):
    runs = [run_trap_ga(replacement=mode, seed=s) for s in range(5)]
    print(mode,
          "mean best:", np.mean([r["best"] for r in runs]),
          "mean final entropy:",
          np.round(np.mean([r["final_entropy"] for r in runs]), 3))
# Expected (measured over seeds 0-4): the generational GA reaches best
# 40-41 of the optimum 50, with entropy falling below 0.1 by generation
# ~10-15 and ending near 0.08 — converged at the deceptive attractor
# (all-zeros blocks score 40). The RTS variant reaches 42-43 with final
# entropy ~0.85: a 2-point gain from changing only the replacement rule,
# at an identical evaluation budget. Note what diversity does NOT do:
# neither variant finds the optimum, because deception requires
# linkage-aware recombination (see estimation-of-distribution-algorithms);
# diversity buys the generations in which complete one-blocks can survive,
# it does not assemble them. The monitor also separates two diagnoses that
# look identical from the fitness curve alone: 'converged' (generational,
# restart or adapt) vs 'diverse but landscape-limited' (RTS, change method).
```

## Worked Example: Restart Policy Comparison

Same trap-5 problem, one generational GA core, five policies under an equal generation budget: no restarts, fixed-interval, stagnation-triggered, diversity-triggered, and random immigrants. One design decision matters enormously on this landscape: restarts are **full** redraws, with the incumbent stored in an external archive rather than in the population. A pilot with keep-elite restarts (even keeping a single elite) showed every policy collapsing to the no-restart result — the kept elite recaptures the fresh population within a few generations and the restart buys nothing. On deceptive landscapes, archive the incumbent outside and restart clean; keep-elite restarts pay off only where re-finding the current basin is itself expensive. This is exactly why the comparison harness matters more than any default: on a different landscape the ranking can invert.

```python
import numpy as np
import pandas as pd


def trap_fitness(pop: np.ndarray, k: int = 5) -> np.ndarray:
    """Concatenated deceptive trap-k, maximize; optimum = n (all ones)."""
    n_pop, n = pop.shape
    u = pop.reshape(n_pop, n // k, k).sum(axis=2)
    return np.where(u == k, k, k - 1 - u).sum(axis=1).astype(float)


def binary_entropy(pop: np.ndarray) -> float:
    """Normalized mean per-locus entropy of a 0/1 population."""
    p = pop.mean(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return float(np.nan_to_num(h).mean())


def ga_with_restarts(
    policy: str,
    n_bits: int = 40,
    n_pop: int = 60,
    n_gen: int = 400,
    seed: int = 0,
) -> float:
    """Generational trap-5 GA under one restart policy; returns archive best.

    GA core: tournament-8, uniform crossover, 0.5/n bit-flip, 2 elites.
    Policies: 'none'; 'fixed' (every 80 generations); 'stagnation' (40 stale
    generations); 'diversity' (entropy < 0.05); 'immigrants' (replace worst
    20% each generation). Restarts redraw the WHOLE population — the
    incumbent lives only in the external archive (global_best).
    """
    rng = np.random.default_rng(seed)
    pop = rng.integers(0, 2, size=(n_pop, n_bits), dtype=np.int8)
    fit = trap_fitness(pop)
    global_best = float(fit.max())
    stale = 0
    p_mut = 0.5 / n_bits
    for gen in range(1, n_gen + 1):
        cand = rng.integers(0, n_pop, size=(2 * n_pop, 8))
        parents = cand[np.arange(2 * n_pop), np.argmax(fit[cand], axis=1)]
        pa, pb = pop[parents[:n_pop]], pop[parents[n_pop:]]
        children = np.where(rng.random(pa.shape) < 0.5, pa, pb)
        children ^= (rng.random(children.shape) < p_mut).astype(np.int8)
        child_fit = trap_fitness(children)
        elite = np.argsort(-fit)[:2]
        children[:2], child_fit[:2] = pop[elite], fit[elite]
        pop, fit = children, child_fit
        if fit.max() > global_best + 1e-12:
            global_best, stale = float(fit.max()), 0
        else:
            stale += 1
        if policy == "immigrants":
            n_new = n_pop // 5
            worst = np.argsort(fit)[:n_new]
            pop[worst] = rng.integers(0, 2, size=(n_new, n_bits), dtype=np.int8)
            fit[worst] = trap_fitness(pop[worst])
            continue
        fire = (
            (policy == "fixed" and gen % 80 == 0)
            or (policy == "stagnation" and stale >= 40)
            or (policy == "diversity" and binary_entropy(pop) < 0.05)
        )
        if fire:
            pop = rng.integers(0, 2, size=(n_pop, n_bits), dtype=np.int8)
            fit = trap_fitness(pop)
            stale = 0
    return global_best


rows = []
for pol in ("none", "fixed", "stagnation", "diversity", "immigrants"):
    bests = np.array([ga_with_restarts(pol, seed=s) for s in range(10)])
    rows.append({"policy": pol, "mean_best": bests.mean(),
                 "std": bests.std(), "optimum_hits": int((bests == 40.0).sum())})
print(pd.DataFrame(rows).round(2).to_string(index=False))
# Expected (measured over seeds 0-9): 'none' and 'immigrants' tie at the
# bottom, mean ~33.2-33.3 (each run commits to one deceptive basin, and
# uniform immigrants are killed by tournament-8 before contributing —
# the failure mode from Practical Challenges). 'fixed' reaches ~34.7 with
# 5 restarts per run; the triggered policies win: 'stagnation' ~35.3
# (~9 restarts) and 'diversity' ~35.4 (~3-4 restarts), because they fire
# exactly when progress stops rather than on a clock. No policy hits the
# optimum 40 — restarts sample basins, they do not fix deception.
# Differences are 1-2 points with std ~0.6-1.0: report mean +/- std over
# >= 10 seeds and count optimum hits before declaring a winner.
```

## Advanced Techniques

### Sizing the niche radius from data

Deb & Goldberg (1989), "An Investigation of Niche and Species Formation in Genetic Function Optimization," derive the packing estimate: for $q$ expected optima spread through an $n$-dimensional box with diagonal $d_{max}$, set $\sigma_{share} \approx d_{max} / (2\, q^{1/n})$. When $q$ is unknown — the usual case in combinatorial problems — estimate $\sigma$ empirically: sample 500-2000 random solution pairs, plot the pairwise-distance histogram, and place $\sigma$ at the valley between the within-basin mode and the between-basin mode. If the histogram is unimodal, the metric does not separate basins and sharing/clearing will not work with any $\sigma$; switch to RTS or crowding, which need no radius. Re-estimate $\sigma$ every 50-100 generations from the current population: niches shrink as search focuses, and a frozen $\sigma$ slowly merges them.

### Cluster-based speciation

Instead of a fixed radius, cluster the population each generation (k-means on real vectors; agglomerative clustering with a precomputed Hamming matrix on discrete genomes) and treat each cluster as a species: per-species elitism, per-species selection budgets proportional to species mean fitness, and recombination restricted within species. This is the mechanism behind NEAT-style speciation and species-based DE variants. It costs $O(N^2 n)$ or a k-means run per generation, but it adapts niche shapes that no single $\sigma$ captures. The number of clusters is a new parameter; the silhouette score over a small range (3-10) chooses it adequately in practice.

### Age-layered populations

ALPS (Hornby 2006, "The Age-Layered Population Structure for Reducing the Problem of Premature Convergence") segments the population into layers by genotype age — generations since the lineage entered the population. Fresh random individuals enter the bottom layer; individuals move up as they age; competition and recombination happen within adjacent layers only. Old, converged elites in top layers cannot extinguish young lineages, so the algorithm performs continuous, structured restarts without any trigger logic. Implementation: store an `age` integer per individual, increment on survival, reset to 0 for random entrants, replace within-layer only. ALPS suits long runs on hard landscapes where every triggered-restart policy either thrashes or never fires.

### Growing populations at restart

When restarts repeatedly land in the same basins, the population is too small to capture basin diversity. The IPOP strategy (Auger & Hansen 2005, "A Restart CMA Evolution Strategy with Increasing Population Size") doubles the population at each restart, trading restart count for per-restart capacity; BIPOP interleaves large and small budgets. The same schedule transfers directly to GAs: `n_pop *= 2` inside the restart branch, holding the total evaluation budget fixed. A practical guard for any restart policy: do not fire within the final 15-20% of the budget — a restart that cannot finish its warm-up only destroys the incumbent population's refinement.

### Diversity in model-based and trajectory-set methods

In EDAs the population is a probability model, and diversity loss appears as variance collapse: univariate marginals saturate at 0/1, Gaussian models shrink to points. The repairs live on the model side — Laplace correction on frequency estimates, lower bounds on marginal probabilities (e.g., clamp to $[1/n, 1 - 1/n]$), variance floors or scaling on covariance — see estimation-of-distribution-algorithms. Scatter search makes diversity a first-class citizen of the reference set: a quality tier plus a diversity tier filled by max-min distance selection, which is `dedup_threshold` above run with a target set size — see scatter-search-path-relinking. Both are reminders that the measure-preserve-restore loop applies to any solution container, not only to GA populations.

## Practical Challenges

**Entropy looks healthy but the search is converged.** Per-locus measures see only marginals. Two failure modes: symmetric encodings (the same tour in $2n$ rotations/reflections inflates Hamming distances) and linkage (two complementary subpopulations score maximal entropy). Canonicalize genotypes before measuring (`canonical_tour` above), count distinct phenotypes or distinct fitness values as a second signal, and for tours measure shared-edge fractions rather than positional entropy.

**Fitness sharing is the runtime bottleneck.** $O(N^2 n)$ every generation dominates cheap objectives. In order: switch to clearing ($O(NWn)$), estimate niche counts from a random sample of $O(N)$ pairs, or move the mechanism to the replacement side (RTS at $O(wn)$ per insert). If sharing must stay, compute the distance matrix once per generation and reuse it for dedup and monitoring.

**Sharing with tournament selection oscillates.** Niche counts computed before selection are invalidated by tournament outcomes, and the population cycles between niches instead of stabilizing (Oei, Goldberg & Chang 1991). Use SUS or remainder stochastic sampling on shared fitness, or abandon selection-side niching for crowding/RTS, which have no such interaction.

**Deterministic crowding slowly loses small niches.** Replacement errors and drift erode niches whose basin is small relative to sampling noise; over thousands of generations only the large basins remain. Use clearing with explicit capacity when specific niches must survive, or RTS with a window large enough that a niche member is usually present ($w \ge N / (\text{expected niches})$).

**Restarts thrash or never fire.** A diversity trigger without hysteresis fires every generation once the threshold is crossed; a pure stagnation trigger with small patience restarts mid-climb. Combine both signals with a cooldown (the `RestartMonitor` above), scale patience to the takeover time of the selection scheme (about $\log N / \log t$ generations under tournament-$t$, so patience of 5-10 takeovers), and suppress restarts in the last ~20% of the evaluation budget.

**Immigrants never survive one generation.** Under strong elitist replacement, uniform-random immigrants are the worst individuals and are deleted immediately — the mechanism burns evaluations and changes nothing. Insert immigrants through RTS (they replace similar individuals, not the worst), protect them for a fixed number of generations (age-based shielding, the ALPS idea), or seed them with a fast greedy construction instead of uniform sampling.

**Duplicates flood the population late in the run.** Small effective search spaces and decoder-based (many-to-one) encodings produce mostly-duplicate offspring once converged. Hash genotypes (`pop[i].tobytes()`, after canonicalization) in a set at insertion; on collision, either reject or apply a forced mutation until the genotype is new — CHC treats collision pressure as the signal to decrement its incest threshold and eventually cataclysm. For decoders, hash the phenotype, not the genotype.

**Objective-space crowding is mistaken for genotype diversity.** NSGA-II's crowding distance spreads solutions along the Pareto front; it says nothing about decision-space diversity, and a perfectly spread front can be genotypically uniform. When distinct designs matter (alternatives for a decision maker), add a decision-space mechanism — RTS on genotype distance, or a dual-space archive — on top of the multi-objective ranking.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | every mechanism in this catalog | `np.random.default_rng(seed)`; count-based measures avoid $N \times N$ matrices |
| scipy.spatial.distance | pairwise distances for sharing/clustering on real vectors | `pdist`/`squareform` for the $O(N^2)$ cases; `cdist` children-vs-population for RTS batches |
| DEAP | GA prototyping; add niching by hand | no built-in sharing/crowding — implement as a custom selection/replacement; `HallOfFame` is similarity-aware deduplication |
| inspyred | reference implementations to study | ships a crowding replacer and niching examples; readable, not fast |
| pymoo | multi-objective work | crowding distance there is objective-space density — not genotype diversity; combine with decision-space archives when alternatives matter |
| pycma | restarts for continuous problems | IPOP/BIPOP restart schedules built into `cma.fmin` via the `restarts` argument |
| pandas | restart/mechanism comparison tables | mean ± std over seeds, optimum-hit counts, per-policy summaries |

## Output Format

A complete diversity-management deliverable contains:

1. **Diagnosis** — best-fitness and diversity curves from the unmodified algorithm, with the measure named and normalized; one paragraph stating which failure is present (collapse vs hard landscape vs broken operators).
2. **Mechanism decision table** — candidates considered, one line each:

| Mechanism | Goal fit | Cost / generation | Parameters | Verdict |
|---|---|---|---|---|
| RTS (window 10) | single best, steady-state host | $O(wn)$ per insert | $w = N/10$ | selected |
| Fitness sharing | multiple optima | $O(N^2 n)$ | $\sigma$, $\alpha$ | rejected: single-best goal, cost |
| Stagnation+diversity restart | reopen search when stuck | $O(Nn)$ at trigger | patience, $d_{min}$, cooldown, keep | selected, layered on RTS |

3. **Monitoring spec** — the per-generation log columns: generation, best, mean fitness, entropy (or distance measure), distinct-genotype count, current mode, restart events.
4. **Parameter table** — every threshold with its value and how it was chosen (takeover-time rule, distance-histogram valley, pilot run).
5. **Implementation** — the mechanism functions with type hints, explicit `np.random.Generator` arguments, and the canonicalization used before any distance or hash.
6. **Comparison protocol and results** — equal evaluation budgets, $\ge 10$ seeds, mean ± std and optimum-hit counts per configuration (the restart-comparison harness above is the template); a one-paragraph reading of the entropy curves under the chosen mechanism.
7. **Budget accounting** — evaluations spent on immigrants/restarts as a fraction of total, and the wall-time overhead of the diversity machinery itself.

## Questions to Ask

- Is the goal one best solution, or several distinct high-quality alternatives?
- What evidence of premature convergence exists — has anyone plotted diversity over generations yet?
- What is the encoding, and is there a distance on it that reflects real solution similarity? Any symmetries to canonicalize?
- Which selection and replacement scheme is in use, and how strong is the pressure (tournament size, elitism)?
- How expensive is one evaluation, and what is the total budget? Can restarts be afforded?
- What population size is in play — is drift in a small population the real cause?
- Is the host generational, steady-state, memetic (local search), model-based (EDA), or reference-set based?
- Are duplicates already being produced in bulk (distinct-genotype count vs N)?
- Is the landscape known or suspected to be multimodal or deceptive (worth a landscape analysis first)?
- Must results be reproducible across seeds for a paper-grade comparison?

## Related Skills

- **selection-and-replacement-strategies** — when diversity loss should be fixed at the source: tournament size, elitism strength, generational vs steady-state replacement, and takeover-time analysis set the pressure these mechanisms push against.
- **genetic-algorithms** — the host loop where monitors, niching replacement, immigrants, and restart triggers plug in; population sizing and operator rates interact with everything here.
- **fitness-landscape-analysis** — when the diagnosis is unclear: multimodality, deception, and neutrality measurements decide whether to preserve diversity, restart, or change the representation instead.
- **scatter-search-path-relinking** — when diversity should be designed into the solution container itself: two-tier reference sets with max-min diversity selection are this skill's `dedup_threshold` promoted to a core algorithm component.
- **estimation-of-distribution-algorithms** — when the population is a probability model: variance collapse is the EDA form of premature convergence, repaired on the model side with probability clamps and variance floors.
