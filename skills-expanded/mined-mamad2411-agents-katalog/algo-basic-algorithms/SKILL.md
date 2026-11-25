---
name: algo-basic-algorithms
description: Compute GCD/LCM via Euclid's algorithm, find roots with Newton's method, and count k-mers using dict/Counter vs O(n^2) list-scan. Use for GCD/LCM math, root-finding, k-mer counting, or Big-O complexity questions.
tool_type: python
primary_tool: Python
---

# Basic Algorithms

## When to Use

- Computing GCD/LCM for fraction simplification, modular arithmetic, or RSA key generation.
- Finding cube roots (or other roots) numerically via Newton-Raphson iteration.
- Counting k-mers in a DNA/RNA sequence and need to justify why a hash map beats a list scan.
- Explaining/verifying Big-O complexity of a nested-loop bioinformatics routine (e.g., all-vs-all pairwise distance) before it is run at genome scale.
- Teaching or reviewing foundational CS algorithms (sorting, ciphers) as building blocks for larger pipelines.

## Version Compatibility

Pure Python stdlib — no third-party dependencies. Works on Python ≥3.9 (uses `list[str]` / `dict[str, int]` builtin generics).

## Prerequisites

- Python ≥3.9. No packages to install.
- Familiarity with Big-O notation (see `## Complexity Table` below for concrete numbers).

## Complexity Table

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Euclidean GCD | O(1) | O(log min(a,b)) | O(log min(a,b)) | O(1) |
| Newton's cube root | O(1) | O(log 1/ε) | O(max_iter) | O(1) |
| k-mer counting (dict) | O(n·k) | O(n·k) | O(n·k) | O(n) |
| k-mer counting (list scan) | O(n·k) | O(n²·k) | O(n²·k) | O(n) |

## Euclidean GCD / LCM

**Goal:** compute the greatest common divisor and least common multiple of two integers.

**Approach:** repeatedly replace `(a, b)` with `(b, a % b)` until `b == 0`; the key identity is `gcd(a, b) == gcd(b, a % b)`.

```python
def gcd(a: int, b: int) -> int:
    """Greatest common divisor via the Euclidean algorithm.

    Complexity: O(log min(a, b)) time, O(1) space.

    >>> gcd(48, 18)
    6
    >>> gcd(-48, 18)
    6
    """
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple, computed from gcd to avoid overflow in
    other languages: (a // gcd(a, b)) * b, not (a * b) // gcd(a, b).
    """
    if a == 0 or b == 0:
        return 0
    g = gcd(a, b)
    return abs(a // g * b)
```

Worst case is consecutive Fibonacci numbers (e.g., `gcd(89, 55)`) — each step still reduces the problem by at least half, so it stays O(log min(a, b)).

## Newton's Method — Root Finding

**Goal:** find `x` such that `x**3 == a` (cube root), without `**(1/3)` (which mishandles negative `a`).

**Approach:** iterate `x_new = (2*x + a/x**2) / 3`, derived from `x - f(x)/f'(x)` for `f(x) = x**3 - a`. Convergence is quadratic — correct digits roughly double each iteration.

```python
def cube_root(a: float, epsilon: float = 1e-10, max_iterations: int = 1000) -> float:
    """Cube root of a via Newton-Raphson iteration.

    Complexity: O(log(1/epsilon)) iterations due to quadratic convergence.

    >>> round(cube_root(27), 6)
    3.0
    >>> round(cube_root(-8), 6)
    -2.0
    """
    if a == 0:
        return 0.0
    sign = 1 if a > 0 else -1
    a_abs = abs(a)
    x = a_abs / 2 if a_abs > 1 else a_abs  # initial guess
    for _ in range(max_iterations):
        x_new = (2 * x + a_abs / (x * x)) / 3
        if abs(x_new - x) < epsilon:
            return sign * x_new
        x = x_new
    return sign * x
```

## k-mer Counting: Hash Map vs List Scan

**Goal:** count occurrences of every k-mer in a sequence — the core operation behind genome-size estimation (Jellyfish), error correction, and de Bruijn graph assembly.

**Approach:** a list-scan implementation looks for an existing `(kmer, count)` entry by scanning the whole list on every insert — O(n) per lookup, O(n²·k) overall. A `dict` gives O(1) average lookup, so the same task is O(n·k). This gap is why every real k-mer counter (Jellyfish, KMC, `Counter`) uses a hash map, not a list.

```python
from collections import Counter


def count_kmers_list(sequence: str, k: int) -> list[tuple[str, int]]:
    """Count k-mers by linear-scanning a list on every insert.

    Complexity: O(n^2 * k) time — n-k+1 k-mers, each insert scans up to
    n-k+1 existing entries and compares k characters.
    """
    counts: list[list] = []  # [kmer, count] pairs
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        for entry in counts:
            if entry[0] == kmer:
                entry[1] += 1
                break
        else:
            counts.append([kmer, 1])
    return [(kmer, n) for kmer, n in counts]


def count_kmers_dict(sequence: str, k: int) -> dict[str, int]:
    """Count k-mers with a dict (equivalent to collections.Counter).

    Complexity: O(n * k) time — n-k+1 k-mers, O(k) average hash/compare
    per lookup, O(1) amortized dict insert/update.
    """
    counts: dict[str, int] = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts


def count_kmers_fast(sequence: str, k: int) -> Counter:
    """Same result as count_kmers_dict, using the stdlib Counter."""
    return Counter(sequence[i:i + k] for i in range(len(sequence) - k + 1))
```

## Pitfalls

- **Euclidean GCD with negatives**: always take `abs()` first; `gcd(-48, 18)` must return 6, not -6.
- **LCM overflow**: Python ints are arbitrary precision, but in other languages `a * b` overflows before dividing — compute `(a // gcd(a, b)) * b`.
- **Newton's method diverges from a bad initial guess**: `a/2` works well for `a > 1`; use `a` itself for `0 < a <= 1`; special-case `a == 0` since the update divides by `x**2`.
- **Using float epsilon for exact integer algorithms**: GCD needs no tolerance — epsilon-based convergence only applies to numerical methods like Newton's.
- **List-scan k-mer counting silently works on toy data, then falls over at genome scale**: O(n²·k) is fine for a 100 bp read, catastrophic for a chromosome. Default to `dict`/`Counter`; only justify a list if k-mer cardinality is tiny and fixed.
- **k-mer window off-by-one**: valid start indices are `range(len(sequence) - k + 1)`; using `range(len(sequence))` reads past the end and raises/truncates silently via slicing.

## See Also

- `bio-database-access-blast-searches` — when O(n²) all-vs-all sequence comparison must be replaced with heuristic search at scale.
- `bio-sequence-io-sequence-statistics` — sequence-level statistics that often reuse k-mer counting.
- `bio-population-genetics-scikit-allel-analysis` — downstream use of counting/complexity tradeoffs on large variant matrices.
