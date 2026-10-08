---
name: algo-comparison-sorts
description: Implement bubble/merge/shell/quicksort in Python; compare Big-O time/space/stability. Use when asked to sort an array, code a sort from scratch, explain quicksort complexity, or fix O(n^2) worst case on sorted input.
tool_type: python
primary_tool: Python
---

# Comparison-Based Sorting Algorithms

## When to Use

- Implementing a sort algorithm from scratch (coursework, interview prep, teaching complexity analysis).
- Choosing between sorting strategies for a given constraint: stability required, memory-bound, guaranteed worst-case, or nearly-sorted input.
- Explaining why quicksort degrades to O(n²) on sorted input, or why merge sort is preferred for stable multi-key sorts.
- Benchmarking custom sort implementations against Python's built-in TimSort.

## Version Compatibility

Pure Python standard library only — no third-party dependencies. Verified on Python ≥3.9 (uses `list[int]` generic syntax; use `List[int]` from `typing` on Python <3.9).

## Prerequisites

- No packages to install (stdlib only: `random`, `time` for benchmarking).
- Prior concepts: Big-O notation (see `algo-complexity-analysis`), recursion, in-place vs. auxiliary-space tradeoffs.

## Complexity Table

| Algorithm | Best | Average | Worst | Space | Stable? |
|-----------|------|---------|-------|-------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Shell Sort | O(n log n) | O(n^1.3) | O(n²) | O(1) | No |
| QuickSort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |

## Decision Table

| Scenario | Use |
|----------|-----|
| Small array (< 50 elements) | Bubble or Insertion |
| Need guaranteed O(n log n) | Merge Sort |
| General purpose, in-place | QuickSort |
| Memory constrained, medium n | Shell Sort |
| Need stability (multi-key sort) | Merge Sort |
| External / disk sorting | Merge Sort |
| Nearly sorted data | Insertion / Bubble (with early termination) |
| Production code, any of the above | `list.sort()` / `sorted()` (TimSort) |

**Goal:** sort a list of comparable elements in place with the simplest correct algorithm, detecting already-sorted input early.
**Approach:** repeatedly bubble the largest unsorted element to the end; track whether any swap happened this pass to bail out in O(n) on sorted input.

```python
def bubble_sort(arr: list[int]) -> list[int]:
    """Sort arr in place using bubble sort. O(n) best case, O(n^2) worst case, stable."""
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # already sorted — early exit gives O(n) best case
    return arr
```

**Goal:** guarantee O(n log n) sorting regardless of input order, preserving the relative order of equal elements (stability).
**Approach:** divide-and-conquer — split the array in half, recursively sort each half, then merge the two sorted halves using `<=` (not `<`) to keep ties in original order.

```python
def merge_sort(arr: list[int]) -> list[int]:
    """Sort arr and return a new list. O(n log n) all cases, O(n) space, stable."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list, preserving stability."""
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # <= preserves stability
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Goal:** sort in place with O(1) extra space, faster than bubble/insertion sort on medium-sized arrays.
**Approach:** run insertion sort on interleaved subsequences separated by a shrinking gap (n/2, n/4, ..., 1); the final gap=1 pass is a plain insertion sort on an almost-sorted array.

```python
def shell_sort(arr: list[int]) -> list[int]:
    """Sort arr in place using shell sort with the n//2 gap sequence. O(1) space, unstable."""
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
```

**Goal:** sort in place, fastest in practice on random data, average O(n log n) with low constant factors.
**Approach:** Lomuto partition around a pivot (elements < pivot move left, ≥ pivot stay right), then recurse on each side. Use a randomized pivot for production code to avoid the O(n²) worst case on sorted input.

```python
import random


def quicksort(arr: list[int], lo: int = 0, hi: int | None = None) -> list[int]:
    """Sort arr in place using quicksort with random pivot selection. O(n log n) average."""
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        p = _partition(arr, lo, hi)
        quicksort(arr, lo, p - 1)
        quicksort(arr, p + 1, hi)
    return arr


def _partition(arr: list[int], lo: int, hi: int) -> int:
    """Lomuto partition: randomize the pivot first to avoid O(n^2) on sorted input."""
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def demo() -> None:
    """Self-check: all four sorts agree with Python's built-in sorted() on random data."""
    random.seed(0)
    data = [random.randint(-100, 100) for _ in range(200)]
    expected = sorted(data)
    assert bubble_sort(data.copy()) == expected
    assert merge_sort(data.copy()) == expected
    assert shell_sort(data.copy()) == expected
    assert quicksort(data.copy()) == expected
    print("All sorts match sorted(): OK")


if __name__ == "__main__":
    demo()
```

## Pitfalls

- **QuickSort worst case on sorted input**: last-element pivot gives O(n²) on already-sorted or reverse-sorted data; use a random or median-of-three pivot (shown above) for real data.
- **Merge Sort space cost**: O(n) auxiliary is unavoidable for the standard top-down version; use Python's built-in `list.sort()` (TimSort) for production instead of rolling your own.
- **Stability matters for multi-key sorts**: sorting by key A then key B with an unstable sort can destroy the A ordering. Bubble and Merge are safe; Quick and Shell are not.
- **Python's `list.sort()`/`sorted()` is TimSort**: O(n log n) worst case, stable, O(n) best case on already-sorted data. Prefer it over a hand-rolled sort unless the point is learning or the comparator is unusual (e.g., external merge).
- **Shell sort gap sequence affects performance**: the naive `n // 2` sequence (used above) can degrade toward O(n²); Knuth's `(3^k - 1) / 2` sequence (1, 4, 13, 40, …) gives O(n^1.3) average case.

## See Also

- `algo-linear-sorts` — counting sort, radix sort, bucket sort (non-comparison, O(n) sorts).
- `algo-complexity-analysis` — Big-O fundamentals referenced by the tables above.
- `algo-linear-binary-search` — searching a sorted array once it's produced.
