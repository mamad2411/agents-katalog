---
name: crossover-operators
description: When the user wants to choose or implement a crossover operator for a genetic or evolutionary algorithm: one-point, two-point, uniform, arithmetic, blend (BLX-alpha), and SBX plus the permutation family OX, PMX, CX, ERX, AEX, and position-based, with preservation properties and operator-encoding fit tables. Also use when the user mentions "crossover operator," "order crossover," "PMX," "uniform crossover," "edge recombination," "SBX," or when offspring must inherit position, order, or adjacency from two parents. For representation choice, see solution-encodings; for unary variation, see mutation-and-perturbation-operators.
---

# Crossover Operators

You are an expert in recombination operators for evolutionary and population-based metaheuristics. This skill is the reference catalog: for every standard crossover — one-point, two-point, uniform (binary/integer); arithmetic, BLX-alpha, SBX (real-valued); OX, PMX, CX, ERX, AEX, position-based (permutation) — it gives when to use it, a numpy implementation, a complexity note, and the problems and algorithms it fits. Use the preservation-property framework below to match operator to encoding to problem, and the measurement harness to verify the match empirically instead of trusting folklore.

## Initial Assessment

Establish these facts before recommending or writing any crossover code:

- **Fix the encoding first.** Binary vector, integer vector, real vector, permutation, or something indirect (random keys, decoder)? The encoding determines which operators are even legal — k-point crossover on a permutation produces duplicates, period. If the encoding is still negotiable, settle it before the operator (see solution-encodings).
- **Identify which structural property carries fitness.** Absolute position (QAP-style slot assignment), relative order (sequencing, scheduling with precedence), adjacency (tours, routing), or set membership (knapsack, covering)? This single question selects the operator family; the anatomy section formalizes the three permutation properties.
- **Check what crossover does to feasibility.** Permutation operators preserve the permutation invariant but nothing else. Side constraints (capacities, time windows, budgets) are violated freely by every standard operator — decide up front: repair, penalty, or decoder.
- **Ask whether recombination earns its place at all.** If two good parents rarely share exploitable structure (low fitness-distance correlation, highly epistatic objective), crossover degenerates to macro-mutation. Plan the headless-chicken control experiment (Advanced Techniques) before investing in an exotic operator.
- **Establish the algorithmic context.** Which algorithm consumes the operator — a canonical GA, a memetic algorithm with local search on offspring, scatter search? With strong local search after crossover, disruption matters less and cheaper operators (OX instead of ERX) often win on time-adjusted quality.
- **Determine the per-child cost tolerance.** All operators here are O(n) per child, but constants differ by an order of magnitude: `np.where` masking vs. Python-level adjacency bookkeeping (ERX). Measure evaluations per second first; the operator should stay well under ~20% of generation wall time.
- **Determine batch shape and vectorizability.** Binary and real operators vectorize fully over an `(N, n)` population array. Permutation operators are inherently per-pair (the fill step depends on which genes are already used), so the loop runs over pairs with vectorized inner steps.
- **One child or two per pair?** Symmetric operators (k-point, uniform, SBX, arithmetic) produce two children for free; most permutation operators produce one child per parent ordering — call them twice with swapped arguments if the budget wants two.
- **Real-valued specifics.** Bounds and their enforcement (clip, reflect, resample), the spread parameter (SBX eta, BLX alpha), and whether crossover applies per gene or per vector.
- **Reproducibility.** Every stochastic operator takes an explicit `np.random.Generator`; seeds are recorded per run. An operator comparison without fixed seeds and repeated runs is noise.

## Operator Anatomy: What Crossover Must Preserve

### The contract of recombination

A crossover operator takes two parent genotypes and must produce a child that (a) is a valid genotype and (b) inherits the structure that made the parents good. Radcliffe (1991), "Forma Analysis and Random Respectful Recombination," makes this precise with two properties worth checking for any operator: **respect** (features common to both parents appear in the child) and **transmission** (every child feature comes from at least one parent). Uniform crossover respects and transmits gene values; CX respects and transmits absolute positions; ERX transmits edges with rare exceptions. An operator that transmits the *wrong* feature class — PMX transmitting positions on a problem where fitness lives in edges — is technically correct and practically useless.

### The three permutation properties, formally

For parents $P^1, P^2$ and child $C$, all permutations of $\{0,\dots,n-1\}$, with $\pi_X(v)$ the index of value $v$ in $X$ and $E(X)$ the undirected cyclic edge set $\{\{X_k, X_{k+1 \bmod n}\}\}$:

$$
\mathrm{pos}(C) = \frac{1}{n}\,\bigl|\{\, i : C_i \in \{P^1_i,\, P^2_i\} \,\}\bigr|
\qquad\text{(position preservation)}
$$

$$
\mathrm{ord}(C \mid P) = \binom{n}{2}^{-1} \,\bigl|\{\, \{a,b\} : \operatorname{sgn}(\pi_C(a)-\pi_C(b)) = \operatorname{sgn}(\pi_P(a)-\pi_P(b)) \,\}\bigr|
\qquad\text{(order agreement)}
$$

$$
\mathrm{adj}(C) = \frac{1}{n}\,\bigl|E(C) \cap \bigl(E(P^1) \cup E(P^2)\bigr)\bigr|
\qquad\text{(edge preservation)}
$$

CX achieves $\mathrm{pos}(C) = 1$ by construction. ERX typically achieves $\mathrm{adj}(C) \ge 0.95$ (Whitley, Starkweather & Fuquay 1989 report ~95-99% parental edges). OX keeps one parent's segment in place and the rest in the other parent's relative order, so it scores high on $\mathrm{ord}$ and middling on the rest. The measurement harness below computes all three for any operator on any parent pair — run it on representative parents from *your* population rather than arguing from the table alone.

### Master catalog

| Operator | Encoding | Primarily preserves | Per-child cost | Source |
|---|---|---|---|---|
| One-point | binary / integer / real | contiguous blocks; strong positional bias | O(n) | Holland (1975) |
| Two-point / k-point | binary / integer / real | blocks, weaker endpoint bias | O(n) | De Jong (1975) |
| Uniform | binary / integer | per-gene values; no positional bias | O(n) | Syswerda (1989) |
| Whole/per-gene arithmetic | real | convexity — children on the parent segment | O(n) | Michalewicz (1992) |
| BLX-alpha | real | interval schemata; allows expansion beyond parents | O(n) | Eshelman & Schaffer (1993) |
| SBX | real | parent-centric spread, tunable via eta | O(n) | Deb & Agrawal (1995) |
| OX (order) | permutation | relative order + one parent's segment | O(n) | Davis (1985) |
| POS (position-based) | permutation | a random position subset + other parent's order | O(n) | Syswerda (1991) |
| PMX (partially mapped) | permutation | absolute positions, segment-anchored | O(n) | Goldberg & Lingle (1985) |
| CX (cycle) | permutation | absolute positions, fully ($\mathrm{pos}=1$) | O(n) | Oliver, Smith & Holland (1987) |
| ERX (edge recombination) | permutation | undirected adjacency | O(n), heavy constant | Whitley et al. (1989) |
| AEX (alternating edges) | permutation | directed adjacency, alternating parents | O(n) | Grefenstette et al. (1985) |

### Operator × problem-type fit

| Problem type | Fitness lives in | First choice | Also reasonable | Avoid |
|---|---|---|---|---|
| Knapsack, subset selection, set covering | membership | uniform | two-point | one-point on long genomes |
| TSP, routing | adjacency | ERX (EAX at the high end) | OX, AEX | PMX, CX |
| Flow-shop, sequencing, priority lists | relative order | OX | POS, PMX | CX |
| QAP, slot assignment, keyboard layout | absolute position | CX | PMX | OX, ERX |
| Continuous parameters | coordinates | SBX (eta 10-20) | BLX-0.5, arithmetic | one-point on correlated genes |
| Bounded integer vectors | per-slot values | uniform | two-point; arithmetic + rounding | — |

Larrañaga et al. (1999), "Genetic Algorithms for the Travelling Salesman Problem: A Review of Representations and Operators," is the standard empirical backing for the permutation rows: edge-preserving operators dominate on the TSP, order-preserving operators on sequencing objectives, and the ranking *inverts* between those two problem classes — there is no best permutation crossover, only a best property match.

### Bias: how operators explore differently at the same fitness

Eshelman, Caruana & Schaffer (1989), "Biases in the Crossover Landscape," separate two axes. **Positional bias:** one-point crossover separates two genes with probability proportional to their distance on the string — a schema of defining length $\delta$ survives with probability about $1 - \delta/(n-1)$ — so gene ordering on the genome silently matters. **Distributional bias:** uniform crossover exchanges $\mathrm{Binomial}(n, 0.5)$ genes, never few, so it is maximally mixing; an order-$o$ schema survives intact with probability $2^{1-o}$ regardless of its span. Practical reading: tightly linked building blocks → two-point; independent genes or unknown linkage → uniform; and if you find yourself reordering the genome to protect one-point crossover, switch operators instead.

## Binary and Integer Crossovers

All three operators below are fully vectorized over an `(N, n)` parent batch: each is one mask construction plus two `np.where` calls, O(Nn) total and allocation-bound rather than compute-bound. They apply unchanged to integer and real genomes (any dtype `np.where` supports); only their bias profiles differ.

**One-point** — use when genes are ordered so that physical adjacency on the string reflects real linkage (rare in OR practice); otherwise its positional bias is a liability. **Two-point** — the default block-preserving choice; treats the genome as a ring, removing one-point's endpoint asymmetry. **Uniform** — the default when linkage is unknown or genes are independent (knapsack, feature selection); `p_swap` tunes mixing strength (0.5 = maximal, Syswerda 1989; 0.1-0.2 behaves like a multi-gene macro-mutation that preserves more parent structure).

```python
import numpy as np

Array = np.ndarray


def one_point_crossover(
    pa: Array, pb: Array, rng: np.random.Generator
) -> tuple[Array, Array]:
    """Batch one-point crossover on (N, n) parent arrays; returns two children.

    Cut position is drawn in [1, n-1] so both children mix both parents.
    """
    n_pairs, n = pa.shape
    cuts = rng.integers(1, n, size=(n_pairs, 1))
    mask = np.arange(n)[None, :] < cuts          # True -> gene taken from first parent
    return np.where(mask, pa, pb), np.where(mask, pb, pa)


def two_point_crossover(
    pa: Array, pb: Array, rng: np.random.Generator
) -> tuple[Array, Array]:
    """Batch two-point crossover: the segment [lo, hi) is swapped between parents."""
    n_pairs, n = pa.shape
    lo = rng.integers(0, n - 1, size=(n_pairs, 1))
    hi = rng.integers(lo + 1, n)                 # broadcast: hi in [lo+1, n-1] per pair
    idx = np.arange(n)[None, :]
    mid = (idx >= lo) & (idx < hi)
    return np.where(mid, pb, pa), np.where(mid, pa, pb)


def uniform_crossover(
    pa: Array, pb: Array, rng: np.random.Generator, p_swap: float = 0.5
) -> tuple[Array, Array]:
    """Batch uniform crossover: each gene swaps between parents with prob p_swap."""
    mask = rng.random(pa.shape) < p_swap
    return np.where(mask, pb, pa), np.where(mask, pa, pb)
```

The knapsack demo below shows the family's one shared weakness: none of these operators knows about the capacity constraint, so children of two feasible parents can be infeasible. That is not a bug to fix inside the operator — handle it with repair, penalty, or a decoder, chosen per problem.

```python
import numpy as np

# Uses one_point_crossover, two_point_crossover, uniform_crossover from above.


def knapsack_eval(
    pop: np.ndarray, values: np.ndarray, weights: np.ndarray, capacity: float
) -> np.ndarray:
    """Batch total value per row; infeasible rows are reported as -1."""
    v = pop @ values
    w = pop @ weights
    return np.where(w <= capacity, v, -1.0)


def knapsack_demo() -> None:
    """Recombine two feasible knapsack parents with each binary operator."""
    values = np.array([8.0, 11.0, 6.0, 4.0, 12.0, 3.0, 5.0, 7.0])
    weights = np.array([5.0, 7.0, 4.0, 3.0, 8.0, 2.0, 3.0, 5.0])
    capacity = 20.0
    pa = np.array([[1, 1, 0, 0, 0, 0, 1, 1]])   # value 31, weight 20
    pb = np.array([[0, 0, 1, 1, 1, 1, 0, 0]])   # value 25, weight 17
    for name, op in [
        ("one-point", one_point_crossover),
        ("two-point", two_point_crossover),
        ("uniform  ", uniform_crossover),
    ]:
        rng = np.random.default_rng(7)           # fresh rng per operator
        c1, c2 = op(pa, pb, rng)
        vals = knapsack_eval(np.vstack([c1, c2]), values, weights, capacity)
        print(f"{name}  child values: {vals[0]:5.1f} {vals[1]:5.1f}")


if __name__ == "__main__":
    knapsack_demo()
# Expected (seed 7): one-point -> 24.0 and -1.0; two-point -> 26.0 and 30.0;
# uniform -> -1.0 and 14.0. Recombination works (two-point built two feasible
# children mixing both parents' items), yet one-point and uniform each
# produced an infeasible child from two feasible parents: standard binary
# crossovers transmit gene values, not constraint satisfaction.
```

## Real-Valued Crossovers

Real-coded GAs and memetic continuous searches recombine coordinates, not bits. The design axis is the **spread** of children around the parents: arithmetic crossover is purely contractive (children lie on the segment between parents, so the population's bounding box can only shrink — pair it with a mutation that can expand), BLX-alpha extends the sampling interval beyond the parents by a fraction alpha per side, and SBX shapes a parent-centric distribution whose concentration is tuned by eta.

**Arithmetic** — use for convex feasible regions where any point between two feasible parents is feasible (linear constraints); also the natural operator when genes are weights or probabilities. **BLX-alpha** — use when the population must be able to expand; alpha = 0.5 makes the children's expected variance equal the parents' (Eshelman & Schaffer 1993, interval-schemata argument), the standard balanced setting. **SBX** — the default in modern real-coded evolutionary algorithms and NSGA-II; eta in [10, 20] for exploitation-leaning search, [2, 5] for exploration (Deb & Agrawal 1995).

```python
import numpy as np

Array = np.ndarray


def arithmetic_crossover(
    pa: Array, pb: Array, rng: np.random.Generator, per_gene: bool = False
) -> tuple[Array, Array]:
    """Batch arithmetic crossover: complementary convex combinations of parents.

    per_gene=False draws one lambda per pair (children on the line segment);
    per_gene=True draws one lambda per coordinate (children in the box).
    """
    n_pairs, n = pa.shape
    lam = rng.random((n_pairs, n) if per_gene else (n_pairs, 1))
    return lam * pa + (1.0 - lam) * pb, (1.0 - lam) * pa + lam * pb


def blx_alpha(
    pa: Array,
    pb: Array,
    rng: np.random.Generator,
    alpha: float = 0.5,
    lower: float = 0.0,
    upper: float = 1.0,
) -> Array:
    """Batch BLX-alpha: per gene, sample uniformly from the parent interval
    extended by alpha times its width on each side, then clip to bounds."""
    lo = np.minimum(pa, pb)
    hi = np.maximum(pa, pb)
    width = hi - lo
    child = rng.uniform(lo - alpha * width, hi + alpha * width)
    return np.clip(child, lower, upper)
```

SBX deserves its own block: it was designed so that, on unbounded reals, the child spread imitates the one-point binary crossover it replaces, with the spread factor $\beta$ drawn from a polynomial density $p(\beta) \propto \beta^{\eta}$ for $\beta \le 1$ and $\beta^{-(\eta+2)}$ for $\beta > 1$. The implementation below includes the two standard practical details that naive versions miss: per-gene application probability (typically 0.5, so children keep some coordinates exactly) and bound handling by clipping.

```python
import numpy as np

Array = np.ndarray


def sbx_crossover(
    pa: Array,
    pb: Array,
    rng: np.random.Generator,
    eta: float = 15.0,
    p_gene: float = 0.5,
    lower: float = 0.0,
    upper: float = 1.0,
) -> tuple[Array, Array]:
    """Batch simulated binary crossover (Deb & Agrawal 1995) with clipping.

    Large eta concentrates children near the parents; small eta spreads them.
    Each gene recombines with probability p_gene, else it is copied through.
    """
    u = rng.random(pa.shape)
    beta = np.where(
        u <= 0.5,
        (2.0 * u) ** (1.0 / (eta + 1.0)),
        (0.5 / (1.0 - u)) ** (1.0 / (eta + 1.0)),
    )
    c1 = 0.5 * ((1.0 + beta) * pa + (1.0 - beta) * pb)
    c2 = 0.5 * ((1.0 - beta) * pa + (1.0 + beta) * pb)
    cross = rng.random(pa.shape) < p_gene
    c1 = np.where(cross, c1, pa)
    c2 = np.where(cross, c2, pb)
    return np.clip(c1, lower, upper), np.clip(c2, lower, upper)


def spread_demo() -> None:
    """Measure child spread around the parent pair (0.3, 0.7) per gene."""
    rng = np.random.default_rng(11)
    n_samples, n = 20_000, 1
    pa = np.full((n_samples, n), 0.3)
    pb = np.full((n_samples, n), 0.7)
    c_sbx20, _ = sbx_crossover(pa, pb, rng, eta=20.0, p_gene=1.0)
    c_sbx2, _ = sbx_crossover(pa, pb, rng, eta=2.0, p_gene=1.0)
    c_blx = blx_alpha(pa, pb, rng, alpha=0.5)
    for name, c in [("SBX eta=20", c_sbx20), ("SBX eta=2 ", c_sbx2),
                    ("BLX-0.5   ", c_blx)]:
        dist = np.minimum(np.abs(c[:, 0] - 0.3), np.abs(c[:, 0] - 0.7))
        print(f"{name}  mean |child - nearest parent| = {dist.mean():.4f}")


if __name__ == "__main__":
    spread_demo()
# Expected (seed 11): SBX eta=20 -> 0.010, SBX eta=2 -> 0.067, BLX-0.5 ->
# 0.100. The ordering is the lesson: eta is a precision dial around the
# parents, while BLX-0.5 samples the whole extended interval uniformly.
```

## Permutation Crossovers

This is the family where operator choice changes results the most, because a permutation simultaneously encodes three different feature classes — positions, order, adjacencies — and each operator preserves a different one. All implementations below take two 1-D parent permutations of $\{0,\dots,n-1\}$ and return one child; call with swapped arguments for the sibling. They are per-pair functions: the fill logic depends on which genes are already placed, so the pair loop stays in Python while every inner step (membership masks, inverse-permutation lookups) is a vectorized array operation.

### OX and POS — order-preserving

**OX (order crossover, Davis 1985)** — use for sequencing problems where *relative* order drives fitness (flow-shop priority sequences, dispatching lists) and as the cheap robust default for tours when ERX is too slow. Keeps one contiguous parent-A segment in place and fills the remaining slots, starting after the segment and wrapping, with the missing genes in parent B's circular order. O(n) per child. Fits: GAs and memetic algorithms on flow-shop, single-machine sequencing, TSP-with-local-search.

**POS (position-based crossover, Syswerda 1991)** — use when a *non-contiguous* set of good gene placements should be heritable (scheduling problems where scattered jobs anchor the sequence). Identical to OX in spirit but the preserved set is a random position subset instead of one segment; with subset rate 0.5 it is the uniform-crossover analogue for permutations. O(n) per child. Fits: job sequencing, rostering priority lists.

```python
import numpy as np

Array = np.ndarray


def order_crossover(p1: Array, p2: Array, rng: np.random.Generator) -> Array:
    """OX: keep p1[i:j] in place; fill remaining slots (circularly, starting
    at j) with the missing genes in p2's circular order starting at j."""
    n = p1.size
    i, j = np.sort(rng.choice(n, size=2, replace=False))
    j += 1                                        # nonempty segment p1[i:j]
    child = np.full(n, -1, dtype=p1.dtype)
    child[i:j] = p1[i:j]
    in_segment = np.zeros(n, dtype=bool)
    in_segment[p1[i:j]] = True
    scan = np.concatenate([p2[j % n:], p2[: j % n]])      # p2 from j, wrapped
    fill = scan[~in_segment[scan]]                        # keeps p2's order
    slots = np.concatenate([np.arange(j, n), np.arange(0, i)])
    child[slots] = fill
    return child


def position_based_crossover(
    p1: Array, p2: Array, rng: np.random.Generator, p_keep: float = 0.5
) -> Array:
    """POS: copy p1's genes on a random position subset; fill the remaining
    positions left-to-right with the missing genes in p2's order."""
    n = p1.size
    keep = rng.random(n) < p_keep
    child = np.full(n, -1, dtype=p1.dtype)
    child[keep] = p1[keep]
    used = np.zeros(n, dtype=bool)
    used[p1[keep]] = True
    child[~keep] = p2[~used[p2]]
    return child
```

### PMX and CX — position-preserving

**PMX (partially mapped crossover, Goldberg & Lingle 1985)** — use when absolute slot assignments matter but you still want segment-level inheritance (QAP-flavored problems attacked with a GA, position-sensitive scheduling). Copies a parent-A segment, then places each conflicting parent-B gene at the slot freed by the mapping chain through the segment; remaining slots copy parent B. O(n) per child — chain-following work is bounded by the segment length. Fits: QAP, assignment-like permutation problems; historically popular on the TSP but adjacency-blind there.

**CX (cycle crossover, Oliver, Smith & Holland 1987)** — use when *every* gene must keep a position it had in one of the parents: CX decomposes the parent pair into cycles and alternates whole cycles between parents, achieving position preservation 1.0 by construction — the maximally respectful position operator. Deterministic: one parent pair yields exactly one child per parent ordering. O(n) per child. Fits: QAP and layout problems; selection-only diversity, so pair it with a real mutation operator.

```python
import numpy as np

Array = np.ndarray


def pmx_crossover(p1: Array, p2: Array, rng: np.random.Generator) -> Array:
    """PMX: copy p1[i:j]; map p2's conflicting segment genes through the
    chain p2-value -> slot of that value in p2 via p1; copy the rest from p2."""
    n = p1.size
    i, j = np.sort(rng.choice(n, size=2, replace=False))
    j += 1
    child = np.full(n, -1, dtype=p1.dtype)
    child[i:j] = p1[i:j]
    slot_in_p2 = np.empty(n, dtype=np.int64)
    slot_in_p2[p2] = np.arange(n)
    placed = np.zeros(n, dtype=bool)
    placed[p1[i:j]] = True
    for k in range(i, j):
        val = int(p2[k])
        if placed[val]:
            continue
        slot = k
        while i <= slot < j:                      # follow the mapping chain
            slot = int(slot_in_p2[p1[slot]])
        child[slot] = val
        placed[val] = True
    open_slots = child == -1
    child[open_slots] = p2[open_slots]
    return child


def cycle_crossover(p1: Array, p2: Array) -> Array:
    """CX: alternate the cycles of the pair (p1, p2) between the parents.
    Deterministic; every child gene keeps its position from one parent."""
    n = p1.size
    child = np.full(n, -1, dtype=p1.dtype)
    slot_in_p1 = np.empty(n, dtype=np.int64)
    slot_in_p1[p1] = np.arange(n)
    visited = np.zeros(n, dtype=bool)
    take_p1 = True
    for start in range(n):
        if visited[start]:
            continue
        slot = start
        while not visited[slot]:                  # walk one cycle
            visited[slot] = True
            child[slot] = p1[slot] if take_p1 else p2[slot]
            slot = int(slot_in_p1[p2[slot]])
        take_p1 = not take_p1
    return child
```

### ERX and AEX — adjacency-preserving

**ERX (edge recombination, Whitley, Starkweather & Fuquay 1989)** — use when fitness lives in edges: the TSP and routing orderings. Builds the union adjacency map of both parents (each gene has 2-4 neighbors), then constructs the child greedily, always moving to the unvisited neighbor that itself has the fewest remaining neighbors — the fail-first rule that keeps edge transmission near 95-99%. When the current gene has no unvisited neighbor (an "edge failure"), a random unvisited gene is inserted, creating one foreign edge. O(n) per child but with the largest constant in this catalog: Python-level set bookkeeping, roughly 10-50x the wall time of OX. Fits: TSP/routing GAs without local search; with strong 2-opt afterwards, OX usually wins on time-adjusted quality.

**AEX (alternating edges, Grefenstette, Gopal, Rosmaita & Van Gucht 1985)** — use as the cheap directed-adjacency operator: the child follows parent A's successor, then parent B's successor, alternating, repairing with a random unvisited gene whenever the inherited successor is already used. More disruptive than ERX (repairs are frequent in late generations) but nearly as cheap as OX. Fits: asymmetric TSP and problems where *directed* succession matters; also a useful diversity-leaning companion to ERX in an operator portfolio.

```python
import numpy as np

Array = np.ndarray


def edge_recombination(p1: Array, p2: Array, rng: np.random.Generator) -> Array:
    """ERX: greedy child construction over the union adjacency map, always
    moving to the unvisited neighbor with the fewest remaining neighbors."""
    n = p1.size
    neighbors: list[set[int]] = [set() for _ in range(n)]
    for p in (p1, p2):
        for k in range(n):
            a, b = int(p[k]), int(p[(k + 1) % n])
            neighbors[a].add(b)
            neighbors[b].add(a)
    child = np.empty(n, dtype=p1.dtype)
    visited = np.zeros(n, dtype=bool)
    current = int(p1[0])
    for k in range(n):
        child[k] = current
        visited[current] = True
        for v in neighbors[current]:              # current leaves the map
            neighbors[v].discard(current)
        if k == n - 1:
            break
        cand = sorted(neighbors[current])         # only unvisited remain here
        if cand:
            sizes = np.array([len(neighbors[v]) for v in cand])
            ties = np.flatnonzero(sizes == sizes.min())
            current = cand[int(rng.choice(ties))]
        else:                                     # edge failure: random restart
            current = int(rng.choice(np.flatnonzero(~visited)))
    return child


def alternating_edges_crossover(
    p1: Array, p2: Array, rng: np.random.Generator
) -> Array:
    """AEX: follow p1's successor, then p2's, alternating; on conflict
    (successor already visited) insert a random unvisited gene."""
    n = p1.size
    succ1 = np.empty(n, dtype=np.int64)
    succ2 = np.empty(n, dtype=np.int64)
    succ1[p1] = np.roll(p1, -1)
    succ2[p2] = np.roll(p2, -1)
    child = np.empty(n, dtype=p1.dtype)
    visited = np.zeros(n, dtype=bool)
    current = int(p1[0])
    child[0] = current
    visited[current] = True
    for k in range(1, n):
        nxt = int(succ1[current]) if k % 2 == 1 else int(succ2[current])
        if visited[nxt]:
            nxt = int(rng.choice(np.flatnonzero(~visited)))
        child[k] = nxt
        visited[nxt] = True
        current = nxt
    return child
```

### Worked comparison: all six on one TSP parent pair

The harness below runs the whole permutation catalog on the textbook parent pair from Eiben & Smith (2015), "Introduction to Evolutionary Computing" (shifted to 0-indexing), validates every child, and measures the three preservation properties defined in the anatomy section. This is the experiment to rerun on parents sampled from your own population whenever an operator choice is contested.

```python
import numpy as np

# Uses order_crossover, position_based_crossover, pmx_crossover,
# cycle_crossover, edge_recombination, alternating_edges_crossover from the
# blocks above (collect them in one module alongside this harness to run it).


def inverse(perm: np.ndarray) -> np.ndarray:
    """pos[v] = index of value v in perm."""
    pos = np.empty(perm.size, dtype=np.int64)
    pos[perm] = np.arange(perm.size)
    return pos


def position_preservation(child: np.ndarray, p1: np.ndarray,
                          p2: np.ndarray) -> float:
    """Fraction of slots where the child agrees with at least one parent."""
    return float(np.mean((child == p1) | (child == p2)))


def order_agreement(child: np.ndarray, parent: np.ndarray) -> float:
    """Fraction of gene pairs whose relative order matches the parent."""
    pc, pp = inverse(child), inverse(parent)
    dc = np.sign(pc[:, None] - pc[None, :])
    dp = np.sign(pp[:, None] - pp[None, :])
    iu = np.triu_indices(child.size, k=1)
    return float(np.mean(dc[iu] == dp[iu]))


def edge_preservation(child: np.ndarray, p1: np.ndarray,
                      p2: np.ndarray) -> float:
    """Fraction of the child's cyclic edges present in either parent."""
    def edges(perm: np.ndarray) -> set[frozenset[int]]:
        return {frozenset((int(perm[k]), int(perm[(k + 1) % perm.size])))
                for k in range(perm.size)}
    parental = edges(p1) | edges(p2)
    return len(edges(child) & parental) / child.size


def property_table() -> None:
    """Run every permutation crossover on one parent pair; print properties."""
    p1 = np.arange(9)
    p2 = np.array([8, 2, 6, 7, 1, 5, 4, 0, 3])
    ops = {
        "OX ": lambda r: order_crossover(p1, p2, r),
        "POS": lambda r: position_based_crossover(p1, p2, r),
        "PMX": lambda r: pmx_crossover(p1, p2, r),
        "CX ": lambda r: cycle_crossover(p1, p2),
        "ERX": lambda r: edge_recombination(p1, p2, r),
        "AEX": lambda r: alternating_edges_crossover(p1, p2, r),
    }
    print("op   child                        pos   ord1  ord2  edge")
    for name, op in ops.items():
        child = op(np.random.default_rng(7))
        assert sorted(child.tolist()) == list(range(9)), f"{name} invalid"
        print(f"{name}  {str(child.tolist()):27}"
              f"  {position_preservation(child, p1, p2):.2f}"
              f"  {order_agreement(child, p1):.2f}"
              f"  {order_agreement(child, p2):.2f}"
              f"  {edge_preservation(child, p1, p2):.2f}")


if __name__ == "__main__":
    property_table()
# Expected (seed 7 per operator): every child passes the permutation check.
# CX scores pos = 1.00 by construction but only edge = 0.56. ERX and AEX
# both score edge = 1.00 on this small pair (no edge failures) while their
# pos collapses to 0.22. OX keeps p1's slice in place yet transmits p2's
# relative order (ord2 = 0.72 vs ord1 = 0.56); PMX is the position-leaning
# middle ground (pos = 0.78). On larger random pairs the contrast sharpens:
# ERX stays near 0.95-1.0 on edges while PMX and CX drop toward the random
# baseline on that column.
```

Reading the table: no operator dominates a column it was not designed for. If the run that consumes these children evaluates tour length, the `edge` column predicts offspring quality; if it evaluates a position-dependent assignment cost, the `pos` column does. Matching the measured property to the objective — not historical habit — is the entire selection method, and Oliver, Smith & Holland (1987) already demonstrated it: on the TSP their CX lost to OX, while on position-fitness test functions the ranking reversed.

## Advanced Techniques

### Adaptive operator selection

When two or three operators are plausible, let the run decide: maintain a small portfolio and select per mating event with probabilities driven by recent offspring improvement. Probability matching with a floor (Thierens 2005, "An Adaptive Pursuit Strategy for Allocating Operator Probabilities") is the robust simple scheme; bandit-style selection (DaCosta et al. 2008, dynamic multi-armed bandits) reacts faster but needs reward-scale care. Reward = max(0, parent best − child cost), normalized by a running scale.

```python
import numpy as np


class OperatorPortfolio:
    """Probability-matching operator selection with a minimum-rate floor.

    q[k] tracks an exponentially smoothed reward per operator; selection
    probabilities mix normalized q with a floor p_min so no operator
    starves and the portfolio can recover when the search phase changes.
    """

    def __init__(self, n_ops: int, p_min: float = 0.10,
                 alpha: float = 0.30, seed: int = 0) -> None:
        self.q = np.ones(n_ops)
        self.p_min = p_min
        self.alpha = alpha
        self.rng = np.random.default_rng(seed)

    def probabilities(self) -> np.ndarray:
        """Current selection distribution over operators."""
        q = self.q / self.q.sum()
        return self.p_min + (1.0 - self.q.size * self.p_min) * q

    def pick(self) -> int:
        """Sample the operator index for the next mating event."""
        return int(self.rng.choice(self.q.size, p=self.probabilities()))

    def update(self, op: int, reward: float) -> None:
        """Smooth the picked operator's reward estimate toward `reward`."""
        self.q[op] += self.alpha * (reward - self.q[op])


if __name__ == "__main__":
    portfolio = OperatorPortfolio(n_ops=3, seed=1)
    rng = np.random.default_rng(2)
    for _ in range(300):                 # operator 1 yields double the reward
        op = portfolio.pick()
        portfolio.update(op, rng.exponential(2.0 if op == 1 else 1.0))
    print(np.round(portfolio.probabilities(), 2))
# Expected (seeds 1, 2): [0.26 0.53 0.21] -- probability mass concentrates
# on operator 1 while the 0.10 floor keeps the others alive for later phases.
```

### Heuristic and problem-aware recombination

The catalog operators are problem-blind. The high-performance end of permutation recombination injects the objective into the child-building step: sequential constructive crossover (Ahmed 2010) picks, at each step, the cheaper of the two parental successors using the distance matrix; edge assembly crossover (Nagata & Kobayashi 2013, "A Powerful Genetic Algorithm Using Edge Assembly Crossover for the Traveling Salesman Problem") merges the parents' edge sets into AB-cycles and reassembles tours from them — the operator behind state-of-the-art TSP GAs. The price is generality and code complexity; reach for these only after the property-matched catalog operator plus local search has plateaued.

### Multi-parent and gene-pool recombination

Nothing restricts recombination to two parents. Scanning crossover (Eiben, Raué & Ruttkay 1994) builds each gene by majority or fitness-weighted vote over r parents; gene-pool optimal mixing (Thierens & Bosman 2011, GOMEA) recombines against the whole selected population using learned linkage sets and accepts per-block improvements greedily. Multi-parent variants raise mixing speed and can rescue a stalling two-parent GA without touching the rest of the loop — but they amplify takeover of common alleles, so watch diversity metrics when switching.

### Crossover under constraints: repair, penalty, or decoder

Standard operators preserve the encoding's invariant, never side constraints. Three placements for the fix, in order of preference when applicable: (1) **decoder** — recombine in an unconstrained genotype (random keys, Bean 1994) and let decoding enforce feasibility, which makes every real-valued crossover, SBX included, a legal permutation operator; (2) **repair** — a greedy post-crossover pass (drop items until capacity holds, reinsert unvisited customers); (3) **penalty** — accept infeasible children and charge the objective. Repair preserves more parental signal than penalties for tight constraints; decoders shift the design burden to decoder locality.

### The headless-chicken control

Before crediting crossover, run the control of Jones (1995), "Crossover, Macromutation, and Population-based Search": replace one parent in every mating with a fresh random solution, keeping everything else identical. If search quality does not drop, recombination is acting as macro-mutation and the operator (or the encoding's linkage) is not exploiting parental structure — switch operators, fix the encoding, or drop crossover and spend the budget on mutation and local search. This experiment costs one extra run and regularly kills weeks of operator-tuning effort.

## Practical Challenges

**k-point or uniform crossover applied to a permutation yields duplicate genes.** The operator is not wrong — the encoding contract is. Either switch to a permutation operator from this catalog, or change representation: random keys recombine safely under any real-valued crossover and decode to permutations by argsort. Add a validity assert (`sorted(child) == list(range(n))`) to the operator's unit test so the violation fails loudly, not as silently corrupted fitness.

**Offspring are consistently worse than both parents.** The classic property mismatch: PMX or CX transmitting positions on an adjacency-fitness problem (TSP), or ERX transmitting edges on a position-fitness problem (QAP). Run the property harness on sampled parent pairs, check which column correlates with offspring fitness, and switch families. If no property correlates, the problem has weak parental structure — see the headless-chicken control.

**Crossover-on vs crossover-off makes no measurable difference.** Test it honestly: same seeds, same budget, mutation-only vs full GA, plus the headless-chicken variant. Frequent outcomes: selection pressure so high that one lineage dominates (crossover recombines near-identical parents — fix selection or diversity first), or a low-locality encoding where parental structure does not survive decoding.

**SBX children pile up at the variable bounds.** Clipping maps the distribution's tails onto the bounds; with many generations a visible atom forms at `lower`/`upper`. Use the bounded SBX variant that renormalizes the spread distribution to the feasible interval (as in NSGA-II reference implementations and pymoo), or reflect instead of clip. Also check eta: values above ~30 make crossover nearly a copy machine and the bound atoms grow from mutation alone.

**ERX dominates the runtime profile.** Expected: its per-child constant is 10-50x OX's because of Python-level set bookkeeping. Options in order: apply ERX only to a top fraction of matings and OX elsewhere; replace sets with a fixed-size `(n, 4)` neighbor array plus counts; or accept OX and add 2-opt to offspring — on time-adjusted tour quality, OX + local search usually beats pure ERX.

**CX returns exact copies of the parents.** When the parent pair forms a single cycle (common late in a run, when parents are similar in a specific way), CX has nothing to alternate and the children equal the parents. Detect `(child == p1).all()` and fall back to PMX or to a mutation, and read it as a diversity warning, not an operator bug.

**Uniform crossover destroys multi-gene building blocks.** With order-$o$ linked groups, uniform transmits them intact with probability $2^{1-o}$ — hopeless past o ≈ 6. If linkage is known, reorder conceptually by using a grouped two-point scheme (cut only at group boundaries); if unknown but suspected, lower `p_swap` to 0.1-0.2 or move to linkage-learning methods (GOMEA-style) rather than tuning blindly.

**Two implementations of "the same" operator give different results.** PMX and OX have published variants (segment endpoints inclusive/exclusive, fill starting at 0 vs after the segment, repair direction in PMX chains). All are legitimate operators but not interchangeable mid-experiment. Pin the variant in code you control, regression-test it against a worked textbook example — the Eiben & Smith pair above gives `[8, 2, 1, 3, 4, 5, 6, 0, 7]` for PMX with segment slots 3-6 — and never compare runs across libraries without checking variant equivalence first.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | always — every operator in this catalog | `np.random.default_rng(seed)` per run; batch binary/real operators over `(N, n)` arrays |
| DEAP | quick GA prototyping with ready-made operators | `tools.cxOrdered` (OX), `cxPartialyMatched` (PMX), `cxUniform`, `cxSimulatedBinaryBounded`; list-based, slower than numpy batches |
| pymoo | real-coded and multi-objective work | reference bounded-SBX implementation; clean operator plug-in API for NSGA-II and friends |
| jMetalPy | metaheuristic experimentation with many built-in operators | includes PMX, SBX, BLX-alpha; heavier framework, useful for comparisons |
| inspyred | teaching and small studies | readable implementations of classic variators; not performance-oriented |
| EvoTorch | GPU-scale evolutionary runs | batch tensor operators; worth it only when populations reach 10^4+ |

Verify the variant, not just the name: DEAP's `cxPartialyMatched` expects index-valued permutations, and library OX implementations differ in fill-start convention — run one known parent pair (the harness above) through any library operator before trusting cross-library comparisons.

## Output Format

A complete crossover recommendation or implementation deliverable contains:

1. **Operator decision table** — the candidates considered, one line each:

| Operator | Encoding fit | Property preserved | Per-child cost | Verdict |
|---|---|---|---|---|
| OX | permutation | relative order | O(n), small constant | selected: order-driven objective |
| ERX | permutation | adjacency | O(n), large constant | rejected: local search covers edges |
| PMX | permutation | position | O(n) | rejected: objective is order-based |

2. **Justification in one paragraph** — which structural property carries fitness for this problem, and the evidence (objective structure, property-harness measurements on sampled parents, or a pilot A/B run with seeds and budget stated).
3. **Implementation** — the operator function with type hints, an explicit `np.random.Generator` argument, and a docstring naming the published variant it implements.
4. **Validation tests** — genotype-invariant assert (permutation validity, bound containment), a regression test against a worked example with known output, and determinism under a fixed seed.
5. **Property measurements** — the pos/ord/edge table for the chosen operator on parents sampled from a real population, not only on textbook pairs.
6. **Integration parameters** — crossover rate (default 0.6-0.95 for generational GAs), one-vs-two children policy, interaction with repair/penalty, and what fraction of generation wall time the operator consumes (microbenchmark number).
7. **Control results when contested** — headless-chicken and crossover-off baselines with identical seeds and budgets, reported as mean ± std over ≥10 runs.

## Questions to Ask

- What is the encoding — and is it fixed, or can the representation still change?
- Which structure makes a good solution good here: positions, relative order, adjacencies, or membership?
- Are there side constraints that crossover will break, and is repair, penalty, or a decoder preferred?
- Will offspring receive local search afterwards (memetic), or must crossover carry quality alone?
- What is the evaluation budget, and how expensive may the operator be relative to one evaluation?
- Does the algorithm need two children per mating or one?
- How large is the population and must operators run as vectorized batches?
- Has a mutation-only or random-parent (headless-chicken) baseline been run for comparison?
- Is there a known-good published variant to match (for reproducing a paper's results)?
- For real-valued genes: what are the bounds, and how should out-of-bounds children be handled?

## Related Skills

- **genetic-algorithms** — when the user needs the full GA loop these operators plug into: selection, elitism, population sizing, convergence diagnosis.
- **solution-encodings** — when the representation itself is still open; encoding choice determines which crossovers are legal, and decoder-style encodings can replace this whole catalog with real-valued operators.
- **mutation-and-perturbation-operators** — when designing the unary variation that complements crossover; every recombination here assumes a mutation partner.
- **traveling-salesman-problem** — when the target is tours: TSP-specific construction, 2-opt/Or-opt local search, and the benchmarks on which permutation crossovers are compared.
