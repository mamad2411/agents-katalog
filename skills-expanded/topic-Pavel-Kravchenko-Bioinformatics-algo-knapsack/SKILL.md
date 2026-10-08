---
name: algo-knapsack
description: Solve 0/1, unbounded, subset-sum, and bitmask set-cover knapsack DP in Python with traceback and O(capacity)-space optimization. Use when picking an optimal subset under a budget/capacity constraint — gene panel or assay selection under a sequencing budget, primer/reagent allocation, experiment portfolio selection, or any "maximize value subject to a cost limit" or "does a subset sum to X" problem.
tool_type: python
primary_tool: python
---

# Knapsack Problems

## When to Use
- Choosing which items to include under a hard budget/capacity while maximizing total value (e.g. selecting genes for a targeted panel within a sequencing-cost budget).
- Deciding if reusable resources (primers, reagents) can be repeatedly drawn to maximize yield within a budget — unbounded knapsack.
- Checking whether a subset of costs/weights can hit an exact target (subset sum), e.g. "can these samples' costs sum to exactly the remaining budget?".
- Picking the minimum-cost combination of assays/library preps that jointly covers a required set of genomic regions/features — bitmask set cover.
- You need not just the optimal value but *which items* were chosen (traceback) or need to fit large capacities in limited memory (space optimization).

## Version Compatibility
Pure Python ≥3.8, no dependencies (stdlib only). Logic is unchanged across Python versions.

## Prerequisites
- Comfortable with basic dynamic programming / tabulation (see `algo-tabulation`, `algo-intro-memoization`).
- No external packages required — `pip install` nothing.

**Goal:** maximize total value of selected items without exceeding a weight/cost capacity, each item usable at most once (0/1 knapsack).

**Approach:** build `dp[i][w]` = best value using the first `i` items with capacity `w`; each cell either skips item `i-1` or takes it if it fits.

```python
def knapsack_01(weights, values, capacity):
    """0/1 knapsack: each item used at most once. O(n*capacity) time/space."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # don't take item i-1
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp[n][capacity]


# Example: pick genes for a targeted panel within a sequencing-cost budget
genes = ['BRCA1', 'TP53', 'EGFR', 'KRAS', 'MYC', 'PTEN']
costs = [50, 30, 40, 35, 45, 25]        # sequencing cost units
relevance = [90, 85, 70, 75, 60, 65]    # clinical relevance score
budget = 100
print(knapsack_01(costs, relevance, budget))  # -> 175 (TP53 + PTEN + ... )
```

## Traceback: which items were chosen

```python
def knapsack_01_with_items(weights, values, names, capacity):
    """0/1 knapsack that also returns the selected item names."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # value changed => item i-1 was taken
            selected.append(names[i - 1])
            w -= weights[i - 1]
    return dp[n][capacity], selected[::-1]


value, chosen = knapsack_01_with_items(costs, relevance, genes, budget)
print(value, chosen)
```

## Space-optimized 0/1 — O(capacity) space

Traverse capacity **backwards** so each item is only ever applied once per row (prevents reusing the same item twice, which would make it unbounded). Loses traceback — use the 2D table above if you need the selected items.

```python
def knapsack_01_space_optimized(weights, values, capacity):
    """O(capacity) space 0/1 knapsack. Inner loop MUST go backwards."""
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

## Unbounded knapsack — items can be reused

**Goal:** maximize value when each item can be picked any number of times (e.g. a reagent/primer mix drawn repeatedly against a budget).

**Approach:** iterate capacity **forward** so an item's own update earlier in the same pass is visible to later capacities — that's what allows reuse.

```python
def knapsack_unbounded(weights, values, capacity):
    """Unbounded knapsack: each item reusable any number of times."""
    dp = [0] * (capacity + 1)
    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]


# Example: PCR primer pairs, synthesis cost vs. amplification efficiency
primer_costs = [2, 3, 4]
primer_efficiency = [3, 4, 5]
reagent_budget = 10
print(knapsack_unbounded(primer_costs, primer_efficiency, reagent_budget))
```

## Subset sum — decision problem, not optimization

**Goal:** determine if any subset of costs sums to an exact target (boolean DP, not a max-value DP).

```python
def subset_sum(nums, target):
    """True if some subset of nums sums exactly to target."""
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num]
    return dp[target]


print(subset_sum(costs, 80))  # can genes be selected costing exactly 80 units?
```

## Bitmask DP — minimum-cost coverage of required regions/features

**Goal:** pick the cheapest combination of assays/library-prep methods whose combined coverage (a bitmask of regions/features each one covers) includes every required region.

**Approach:** `dp[mask]` = min cost to reach coverage exactly `mask`; since `mask | coverage[i] >= mask` always, scanning masks in increasing numeric order and relaxing forward correctly propagates costs (no need to revisit).

```python
def min_cost_coverage(costs, coverage, required):
    """
    Bitmask set-cover DP. `coverage[i]` is a bitmask of regions method i covers;
    `required` is the bitmask of all regions that must be covered.
    Returns minimum total cost, or -1 if `required` is unreachable.
    """
    INF = float('inf')
    dp = [INF] * (required + 1)
    dp[0] = 0
    for mask in range(required + 1):
        if dp[mask] == INF:
            continue
        for i, cov in enumerate(coverage):
            new_mask = mask | cov
            if new_mask <= required:
                dp[new_mask] = min(dp[new_mask], dp[mask] + costs[i])
    return dp[required] if dp[required] != INF else -1


# Regions: 0=Exome, 1=Promoters, 2=Enhancers, 3=Introns
method_costs = [300, 90, 80, 120, 150]
method_coverage = [0b1111, 0b0110, 0b0100, 0b1001, 0b1011]
print(min_cost_coverage(method_costs, method_coverage, required=0b1111))
```

## Pitfalls
- 0/1 vs. unbounded: the *direction* of the inner capacity loop (backward vs. forward) is the entire difference — get it backward in unbounded or forward in 0/1 and results silently become wrong (not a crash).
- Space-optimized 0/1 loses traceback; keep the full 2D `dp` table if you need to report *which* items were selected.
- Subset sum is a boolean/decision DP — don't conflate it with the value-maximizing knapsack DPs.
- Bitmask DP array size is `required + 1` (mask values are integers up to the target bitmask, not "number of items") — sizing it by item count is a common off-by-magnitude bug.
- All variants assume non-negative integer weights/costs; capacity must fit in memory as `O(capacity)` or `O(n * capacity)` array — reject/rescale fractional or huge real-valued costs first.

## See Also
- `algo-tabulation` — general bottom-up DP tabulation patterns these knapsack variants build on.
- `algo-intro-memoization` — top-down/recursive DP alternative before converting to tabulation.
- `algo-sequence-alignment` — another 2D DP (edit distance) using the same table-fill technique.
- `bio-experimental-design-sample-size` — real budget-constrained experiment selection this DP can drive.
