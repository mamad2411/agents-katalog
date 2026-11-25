---
name: algo-linear-sorts
description: "Implement counting sort, radix sort, and bucket sort in Python for O(n) non-comparison sorting of integers, fixed-length strings, and DNA k-mers. Use when sorting integers with a small known range, sorting fixed-length keys/k-mers for de Bruijn graph construction or k-mer analysis, or explaining why non-comparison sorts beat the Omega(n log n) lower bound."
tool_type: python
primary_tool: Python
---

# Linear Time Sorting Algorithms

## When to Use

- Sorting integers with a small, known range (ages 0-120, Phred quality scores 0-93, read counts)
- Sorting fixed-length keys where comparison sorts are the bottleneck: k-mers, barcodes, UMIs, SSNs, dates
- Building a de Bruijn graph or k-mer index and needing to sort millions of fixed-length k-mers fast
- A user asks "why is this O(n)?" or "how do I sort without comparisons?" for integer/string data
- Explaining the Omega(n log n) comparison-sort lower bound and how counting/radix/bucket sort escape it

## Version Compatibility

Pure Python standard library only — no external packages. Verified on Python >=3.8 (uses `list`, `typing.Optional`; on Python >=3.10 you can use `int | None` instead).

## Prerequisites

- Comfortable with Big-O notation and stability in sorting (see `algo-complexity-analysis`, `algo-comparison-sorts`)
- Basic Python: lists, `for`/`while` loops, slicing

## Why O(n) Is Possible

Any comparison-based sort needs Omega(n log n) comparisons in the worst case (a decision tree distinguishing n! permutations needs log2(n!) ~ n log2(n) levels). Counting, radix, and bucket sort escape this bound by never comparing elements — they use direct addressing, digit decomposition, or distribution into buckets instead.

**Trade-off:** O(n) time in exchange for assumptions about the input (integers, bounded range, fixed-length keys, or a known-uniform distribution) plus O(n+k) extra space.

## Counting Sort — O(n + k)

**Goal:** stably sort non-negative integers in a small, known range `[0, k]`.
**Approach:** count occurrences of each value, turn counts into a prefix sum (so `count[v]` = number of elements `<= v`), then place each element from right to left using that count as its output index (right-to-left preserves stability).

```python
from typing import List, Optional


def counting_sort(arr: List[int], max_val: Optional[int] = None) -> List[int]:
    """Stably sort non-negative integers in O(n + k), k = max value.

    >>> counting_sort([4, 2, 2, 8, 3, 3, 1])
    [1, 2, 2, 3, 3, 4, 8]
    """
    if not arr:
        return []
    k = max_val if max_val is not None else max(arr)
    count = [0] * (k + 1)
    for num in arr:
        count[num] += 1
    for i in range(1, k + 1):
        count[i] += count[i - 1]  # prefix sum: count[v] = #elements <= v
    output = [0] * len(arr)
    for num in reversed(arr):  # right-to-left is required for stability
        count[num] -= 1
        output[count[num]] = num
    return output
```

**When to use:** `k` close to O(n) (ages, grades, quality scores). If `k >> n`, space blows up to O(k) and it becomes slower than `sorted()`.

## Radix Sort — O(d(n + k))

**Goal:** sort integers (or fixed-length strings) with many digits without ever comparing whole keys.
**Approach:** apply a stable digit-wise counting sort from the least-significant digit (LSD) to the most-significant. `d` = number of digits, `k` = base (10 for decimal, 4 for DNA alphabet).

```python
def counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """Stably sort arr by the digit at position `exp` (1=units, 10=tens, ...)."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for num in reversed(arr):
        digit = (num // exp) % 10
        count[digit] -= 1
        output[count[digit]] = num
    return output


def radix_sort(arr: List[int]) -> List[int]:
    """LSD radix sort for non-negative integers, O(d(n + k)).

    >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
    [2, 24, 45, 66, 75, 90, 170, 802]
    """
    if not arr:
        return []
    max_num = max(arr)
    result = arr.copy()
    exp = 1
    while max_num // exp > 0:
        result = counting_sort_by_digit(result, exp)
        exp *= 10
    return result
```

**When to use:** large numbers with many digits, or fixed-length strings, whenever `d * (n + k) < n log n`.

## Bioinformatics application: sorting DNA k-mers and nucleotides

**Goal:** sort a DNA string by nucleotide, and sort a list of fixed-length k-mers lexicographically — both O(n) instead of O(n log n), because the alphabet is fixed size 4 (A, C, G, T).
**Approach:** counting sort over the 4-symbol alphabet for single nucleotides; LSD radix sort (counting sort per character position, right to left) for k-mers, since all k-mers have the same fixed length. This is the same pattern used to bucket/sort k-mers before building a de Bruijn graph in assemblers like Velvet/SPAdes.

```python
ALPHABET = "ACGT"
RANK = {base: i for i, base in enumerate(ALPHABET)}


def counting_sort_dna(sequence: str) -> str:
    """Sort a DNA string into A's, then C's, then G's, then T's. O(n), n = len(sequence)."""
    counts = [0] * len(ALPHABET)
    for base in sequence:
        counts[RANK[base]] += 1
    return "".join(base * n for base, n in zip(ALPHABET, counts))


def radix_sort_kmers(kmers: List[str]) -> List[str]:
    """Lexicographically sort fixed-length DNA k-mers via LSD radix sort.

    All k-mers must have the same length k. Stable counting sort per
    character position, processed right to left.
    """
    if not kmers:
        return []
    k = len(kmers[0])
    result = list(kmers)
    for pos in range(k - 1, -1, -1):  # rightmost character first
        buckets: List[List[str]] = [[] for _ in ALPHABET]
        for kmer in result:
            buckets[RANK[kmer[pos]]].append(kmer)
        result = [kmer for bucket in buckets for kmer in bucket]
    return result


def extract_kmers(sequence: str, k: int) -> List[str]:
    """All k-mers (substrings of length k) from sequence, in order of occurrence."""
    return [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
```

## Bucket Sort — O(n) average

**Goal:** sort uniformly distributed floats (e.g. normalized values in `[0, 1)`).
**Approach:** distribute elements into `n` buckets by value, sort each small bucket with insertion sort, concatenate.

```python
def bucket_sort(arr: List[float], num_buckets: Optional[int] = None) -> List[float]:
    """Sort floats in [0, 1) assuming a roughly uniform distribution."""
    if not arr:
        return []
    num_buckets = num_buckets or len(arr)
    buckets: List[List[float]] = [[] for _ in range(num_buckets)]
    for num in arr:
        idx = min(int(num * num_buckets), num_buckets - 1)
        buckets[idx].append(num)
    result: List[float] = []
    for bucket in buckets:
        bucket.sort()  # small bucket -> comparison sort is cheap here
        result.extend(bucket)
    return result
```

## When to Choose Which

| Algorithm | Time | Space | Stable | Input Requirement |
|---|---|---|---|---|
| Counting Sort | O(n + k) | O(n + k) | Yes | Non-negative integers, small range |
| Radix Sort | O(d(n + k)) | O(n + k) | Yes | Integers or fixed-length strings/k-mers |
| Bucket Sort | O(n) avg, O(n^2) worst | O(n + k) | Yes* | Uniformly distributed values |

## Pitfalls

- Counting sort with negative integers requires an offset: shift all values by `abs(min(arr))` before sorting, then shift back.
- Radix sort on negative numbers: sort absolute values, then separate and reverse the negatives before prepending them.
- Right-to-left iteration in counting sort is essential for stability — left-to-right breaks stable ordering.
- `radix_sort_kmers` assumes every k-mer has the same length; filter or pad first if extracting k-mers near the end of a sequence produces short trailing substrings.
- Bucket sort degrades to O(n^2) if the distribution is skewed and most elements land in one bucket — check the distribution before using it, or fall back to `sorted()`.
- Counting sort's O(k) space can dominate: sorting a single value of 10^9 allocates a 10^9-length array — use radix sort instead when `k >> n`.

## See Also

- `algo-comparison-sorts` — O(n log n) quicksort/mergesort/heapsort for when linear-sort assumptions don't hold
- `algo-complexity-analysis` — Big-O fundamentals and the comparison-sort lower bound proof
- `algo-suffix-arrays` — k-mer/suffix ranking structures that build on radix-sort-style bucketing
- `bio-genome-assembly-short-read-assembly` — de Bruijn graph assembly, where k-mer sorting is a preprocessing step
