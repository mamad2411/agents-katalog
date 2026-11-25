---
name: algo-intro-memoization
description: "Speed up exponential recursion (Fibonacci, alignment counting, coin change) to linear time via dict cache or lru_cache. Use when recursion is slow, or asked to memoize, add @lru_cache, or explain overlapping subproblems."
tool_type: python
primary_tool: functools.lru_cache
---

# Memoization (Top-Down Dynamic Programming)

## When to Use

- A recursive function is exponentially slow (e.g. naive Fibonacci, naive alignment-path counting) and you need to speed it up without rewriting the algorithm.
- You need to count/enumerate combinatorial possibilities (alignments, RNA foldings, coin combinations, climbing-stairs style paths) that have a recurrence relation.
- You're prototyping before writing an explicit O(nm) DP table (see `algo-tabulation`) and want to reason about the recurrence first.
- Someone asks to "add caching to this recursive function" or "why is my recursive solution slow."
- You're building toward alignment/HMM/RNA-folding algorithms and want to understand the DP mindset those algorithms rely on.

## Version Compatibility

Pure Python standard library — `functools.lru_cache` / `functools.cache` (Python ≥ 3.9). No third-party dependencies. Works identically on Python 3.10–3.13.

## Prerequisites

- Comfort writing recursive functions and base cases.
- `algo-complexity-analysis` (recognizing O(2^n) vs O(n)) is a useful prior skill.
- No packages to install — everything here is stdlib.

## DP Applicability Checklist

Ask these three questions; if all are "yes," memoization applies:

1. **Recursive substructure** — the answer to the big problem is built from answers to smaller instances (a recurrence relation exists).
2. **Overlapping subproblems** — the same smaller instance is solved more than once during naive recursion.
3. **Base cases** — the smallest instances have known, directly-returnable answers.

**Goal:** turn an exponential-time naive recursion into linear/polynomial time.
**Approach:** cache each `(arguments) -> result` mapping the first time it's computed, and return the cached value on every subsequent call with the same arguments — either manually with a dict, or automatically with `@lru_cache`.

```python
import time
from functools import lru_cache


def fib_naive(n):
    """Pure recursive Fibonacci - O(2^n) time. Recomputes fib(k) exponentially many times."""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memoized(n, memo=None):
    """Top-down Fibonacci with a manual dict cache - O(n) time, O(n) space."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_memoized(n - 1, memo) + fib_memoized(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fib_cached(n):
    """Same recurrence, cached automatically by functools - the preferred idiom."""
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


if __name__ == "__main__":
    # naive is fine up to ~30, then blows up; memoized handles n=200+ instantly
    # (n much above ~950 needs sys.setrecursionlimit() or tabulation - see Pitfalls)
    start = time.perf_counter()
    assert fib_memoized(200) == fib_cached(200)
    fib_cached.cache_clear()
    fib_cached(200)
    print(f"fib(200) via lru_cache: {fib_cached(200)} in {time.perf_counter() - start:.4f}s")
    print(fib_cached.cache_info())  # CacheInfo(hits, misses, maxsize, currsize)
```

**Goal:** count the number of possible pairwise-alignment paths between two sequences (the same recurrence structure underlying Needleman-Wunsch/Smith-Waterman, but counting paths instead of scoring them).
**Approach:** at each position, either consume one base from each sequence (match/mismatch), or a gap in one sequence; recurse and cache on `(m, n)`.

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def count_alignments(m, n):
    """Count possible alignments between sequences of length m and n.

    Same recurrence as the Needleman-Wunsch alignment matrix, but summing
    path counts instead of scores. Grows combinatorially with m, n.
    """
    if m == 0 or n == 0:
        return 1  # only gap insertions remain
    return (
        count_alignments(m - 1, n - 1)  # match/mismatch: consume both
        + count_alignments(m - 1, n)    # gap in sequence 2
        + count_alignments(m, n - 1)    # gap in sequence 1
    )


for m, n in [(3, 3), (5, 5), (10, 10)]:
    count_alignments.cache_clear()  # clear so timing/counts aren't skewed across cache-shared calls
    print(f"lengths {m},{n}: {count_alignments(m, n):,} possible alignments")
```

**Goal:** find the minimum number of coins (or, biologically, minimum edit operations / minimum resource units) to reach a target amount.
**Approach:** try every coin as the "last one used," recurse on the remainder, cache on the remaining amount.

```python
def min_coins(coins, amount, memo=None):
    """Minimum coins needed to make `amount`; returns float('inf') if impossible."""
    if memo is None:
        memo = {}
    if amount == 0:
        return 0
    if amount < 0:
        return float("inf")
    if amount in memo:
        return memo[amount]

    best = float("inf")
    for coin in coins:
        result = min_coins(coins, amount - coin, memo)
        if result != float("inf"):
            best = min(best, result + 1)

    memo[amount] = best
    return best


coins = [1, 5, 10, 25]
for amount in [11, 30, 41, 63]:
    print(f"{amount} cents: {min_coins(coins, amount)} coins minimum")
```

## Pitfalls

- Python's default recursion limit is ~1000 — deep memoized recursion (e.g. `fib_cached(5000)`) raises `RecursionError`; raise the limit with `sys.setrecursionlimit()` or switch to bottom-up tabulation (`algo-tabulation`) for large `n`.
- Mutable default arguments (`memo={}` in the function signature) persist across separate top-level calls and silently leak stale entries — use `memo=None` and initialize inside the function body, as shown above.
- `@lru_cache` requires all arguments to be hashable — it fails on `list`/`dict`/`set` arguments; convert to `tuple`/`frozenset` first, or pass a manual dict cache instead.
- Forgetting `.cache_clear()` between benchmarking runs on `@lru_cache`-decorated functions makes timings meaningless (later calls hit the cache from earlier ones).
- Memoization only saves time if subproblems actually overlap — if every call has unique arguments (no repeated subproblems), caching adds overhead with no benefit.

## See Also

- `algo-tabulation` — bottom-up DP with explicit tables, avoids recursion-depth limits.
- `algo-knapsack` — classic 2D memoization/tabulation problem (weight/value trade-off).
- `algo-sequence-alignment` — the real Needleman-Wunsch/Smith-Waterman scoring DP that `count_alignments` mirrors.
- `algo-complexity-analysis` — reasoning about why naive recursion is O(2^n) and memoized is O(n).
