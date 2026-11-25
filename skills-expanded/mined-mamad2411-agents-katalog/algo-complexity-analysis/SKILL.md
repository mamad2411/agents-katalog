---
name: algo-complexity-analysis
description: Derive Big O time/space complexity of loops and recursion via recurrence relations; simplify expressions, compare growth at scale. Use when asked the complexity of code, hunting O(n^2) loops, or worst-case cost.
tool_type: python
primary_tool: Python
---

# Algorithmic Complexity Analysis (Big O)

## When to Use
- Asked to state or derive the time/space complexity ("what's the Big O of this function") of a code snippet or algorithm
- Reviewing code for hidden quadratic behavior: `in` on a list inside a loop, `+=` string concatenation, `sorted()` inside a loop
- Choosing between data structures/algorithms for scale (list vs set membership, sort vs heap)
- Deriving recursive complexity via a recurrence relation, e.g. `T(n) = 2T(n/2) + n` (Master theorem)
- Explaining best/average/worst-case or amortized cost (`list.append`, hash table lookup, quicksort pivot choice)

## Version Compatibility
- Language-agnostic technique; example code uses Python ≥3.8 stdlib only (`math`, no third-party dependencies)

## Prerequisites
- Comfortable reading Python loops, function calls, and recursion
- No packages to install

## Complexity Classes (fastest to slowest)

| Class | Name | Example |
|-------|------|---------|
| O(1) | Constant | Dict lookup, array index |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear scan, single pass |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci, subset enumeration |
| O(n!) | Factorial | Permutation enumeration, brute-force TSP |

## Simplification Rules

```text
O(2n + 5)    →  O(n)      # drop constants
O(n² + n)    →  O(n²)     # drop lower-order terms
O(500)       →  O(1)
O(n² + n³)   →  O(n³)
O(A) then O(B)  →  O(A + B)   # sequential loops add
O(A) inside O(B) →  O(A × B)  # nested loops multiply
```

**Goal:** classify the complexity of straight-line and loop-based code.
**Approach:** identify the loop structure (single / nested / sequential / halving), express operation count as a function of `n`, then apply the simplification rules above.

```python
def get_first_element(arr):
    """Return the first element. O(1) time, O(1) space.

    Direct index access: base_address + index * element_size,
    independent of array length.
    """
    return arr[0] if arr else None


def binary_search(arr, target):
    """Find target in a sorted array. O(log n) time, O(1) space.

    Each iteration halves the search space: after k steps the
    remaining size is n / 2**k, so it terminates in ~log2(n) steps.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2       # O(1)
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1               # discard left half
        else:
            right = mid - 1              # discard right half
    return -1


def has_duplicate_naive(arr):
    """O(n²) time, O(1) space: compares every pair of elements."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return True
    return False


def has_duplicate_fast(arr):
    """O(n) time, O(n) space: trades memory for speed via a set."""
    seen = set()
    for x in arr:
        if x in seen:        # O(1) average membership test
            return True
        seen.add(x)
    return False
```

**Goal:** derive complexity of recursive functions.
**Approach:** write the recurrence relation `T(n) = a*T(n/b) + f(n)` (Master theorem form), then match it to a known pattern.

```python
def merge_sort(arr):
    """Sort via divide-and-conquer. O(n log n) time, O(n) space.

    Recurrence: T(n) = 2*T(n/2) + O(n)  ->  O(n log n)
    (log n levels of recursion, O(n) merge work per level)
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists. O(n) time, O(n) space."""
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def fibonacci_naive(n):
    """Naive recursive Fibonacci. O(2^n) time, O(n) space (call stack).

    Recurrence: T(n) = T(n-1) + T(n-2) + O(1)  ->  O(2^n)
    Each call branches into two more calls, forming a binary call tree.
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
```

| Pattern | Recurrence | Solution |
|---------|------------|----------|
| Linear recursion | T(n) = T(n-1) + 1 | O(n) |
| Binary recursion (no reuse) | T(n) = 2T(n-1) + 1 | O(2ⁿ) |
| Divide & conquer (merge sort) | T(n) = 2T(n/2) + n | O(n log n) |
| Binary search | T(n) = T(n/2) + 1 | O(log n) |

## At Scale (n = 1,000,000)

| Complexity | Operations | Feasible? |
|------------|-----------|-----------|
| O(1) | 1 | Yes |
| O(log n) | ~20 | Yes |
| O(n) | 1,000,000 | Yes |
| O(n log n) | ~20,000,000 | Yes |
| O(n²) | 10¹² | No |
| O(2ⁿ) | ∞ | Never |

## Best / Average / Worst

| Algorithm | Best | Average | Worst |
|-----------|------|---------|-------|
| Binary search | O(1) | O(log n) | O(log n) |
| Quicksort | O(n log n) | O(n log n) | O(n²) |
| Merge sort | O(n log n) | O(n log n) | O(n log n) |
| Hash table lookup | O(1) | O(1) | O(n) |
| BFS/DFS | O(V+E) | O(V+E) | O(V+E) |

## Amortized Complexity

- Python `list.append()`: O(1) amortized (occasional O(n) resize when capacity doubles, but rare)
- Python `dict`/`set` lookup: O(1) average; O(n) worst case (pathological hash collisions — rare with good hashing)

## Pitfalls

- **Hidden O(n) inside a loop**: `x in some_list` is O(n); inside an O(n) loop that's O(n²). Use a `set` for O(1) membership (see `has_duplicate_fast` above).
- **String concatenation**: `s += x` in a loop reallocates and copies each time → O(n²) total. Use `''.join(parts)`.
- **`sorted()` is O(n log n)**: calling it inside a loop makes the loop O(n² log n) — sort once outside the loop.
- **Recursion depth**: unbounded recursion on large `n` hits Python's default ~1000-frame limit. Prefer an iterative rewrite over raising `sys.setrecursionlimit`.
- **Space vs time trade-off**: memoization/hash sets trade O(n) space for O(n²) → O(n) or O(1) repeated lookups.
- **Worst-case vs average-case**: quicksort degrades to O(n²) on already-sorted input with a naive pivot; use random/median-of-three pivot selection or Python's built-in Timsort (`sorted()`/`list.sort()`), which is O(n log n) worst case.

## See Also
- `algo-basic-algorithms` — foundational search/sort algorithms referenced above
- `algo-linear-binary-search` — linear vs binary search trade-offs in depth
- `algo-comparison-sorts` — merge sort, quicksort, heapsort implementations
- `algo-intro-memoization` — turning exponential recursion into polynomial time
