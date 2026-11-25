---
name: algo-dynamic-arrays
description: "Implement resizable arrays with ctypes-backed doubling/shrinking; prove append is amortized O(1). Use when asked why list.append is O(1), to build a DynamicArray class, or to compare list vs numpy append speed."
tool_type: python
primary_tool: python
---

# Dynamic Arrays

## When to Use

- Explaining or proving why `list.append()` is O(1) amortized (accounting/aggregate method).
- Implementing a resizable array from scratch (interview-style `DynamicArray` class) with append/insert/delete/pop.
- Choosing or justifying a growth factor (1.5x vs 2x vs Python's ~1.125x) and a shrink threshold to avoid thrashing.
- Comparing `list.append` vs `np.append` vs pre-allocated `numpy.ndarray` for performance.
- Inspecting CPython's actual list over-allocation via `sys.getsizeof`.

## Version Compatibility

Python ≥ 3.9 (uses `list[int]`-style generics informally; core logic works on any CPython 3.x). NumPy ≥ 1.24 for the `ndarray` comparison. No non-stdlib dependency is required for the `DynamicArray` implementation itself (`ctypes` is stdlib).

## Prerequisites

- Comfortable with Big-O notation and worst-case vs amortized cost.
- `pip install numpy` only needed for the performance-comparison section.
- Related concept: `algo-complexity-analysis` for amortized-analysis background.

**Goal:** Implement a dynamic array supporting O(1) amortized append and O(n) insert/delete, with correct grow/shrink thresholds.

**Approach:** Store elements in a raw `ctypes.py_object` buffer sized to `_capacity`. Double capacity on a full append/insert; halve capacity only once size drops to 1/4 of capacity (not 1/2, to avoid resize thrashing when append/pop alternate near a boundary).

```python
import ctypes
from typing import Any, Iterator


class DynamicArray:
    """Resizable array with amortized O(1) append.

    Resize strategy:
      - Grow: double capacity when full (2x growth factor).
      - Shrink: halve capacity only once size <= capacity/4.
    The 2x growth factor makes n appends cost O(n) total (O(1) amortized).
    The 1/4 shrink threshold (rather than 1/2) prevents thrashing when
    append/pop alternate right at a resize boundary.
    """

    GROWTH_FACTOR: float = 2.0
    SHRINK_THRESHOLD: float = 0.25
    MIN_CAPACITY: int = 1

    def __init__(self, initial_capacity: int = 1) -> None:
        self._size: int = 0
        self._capacity: int = max(initial_capacity, self.MIN_CAPACITY)
        self._array: ctypes.Array = self._make_array(self._capacity)

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, index: int) -> Any:
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError(f"index {index} out of bounds for size {self._size}")
        return self._array[index]

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self._array[i]

    @property
    def capacity(self) -> int:
        return self._capacity

    def append(self, value: Any) -> None:
        """Add to the end. O(1) amortized, O(n) worst case (on resize)."""
        if self._size == self._capacity:
            self._resize(int(self._capacity * self.GROWTH_FACTOR))
        self._array[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """Insert at index, shifting later elements right. O(n)."""
        if index < 0:
            index += self._size
        if not 0 <= index <= self._size:
            raise IndexError(f"insert index {index} out of bounds")
        if self._size == self._capacity:
            self._resize(int(self._capacity * self.GROWTH_FACTOR))
        for i in range(self._size, index, -1):
            self._array[i] = self._array[i - 1]
        self._array[index] = value
        self._size += 1

    def delete(self, index: int) -> Any:
        """Remove and return element at index, shifting left. O(n)."""
        if self._size == 0:
            raise IndexError("delete from empty array")
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError(f"delete index {index} out of bounds")
        value = self._array[index]
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        self._size -= 1
        if self._size <= self._capacity * self.SHRINK_THRESHOLD and self._capacity > self.MIN_CAPACITY:
            self._resize(max(self._capacity // 2, self.MIN_CAPACITY))
        return value

    def pop(self) -> Any:
        """Remove and return the last element. O(1) amortized."""
        return self.delete(self._size - 1)

    def _resize(self, new_capacity: int) -> None:
        new_array = self._make_array(new_capacity)
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity

    def _make_array(self, capacity: int) -> ctypes.Array:
        return (capacity * ctypes.py_object)()
```

**Goal:** Prove append is O(1) amortized using the accounting/aggregate method.

**Approach:** Track cumulative cost of n appends with 2x growth: total resize copies are `1 + 2 + 4 + ... + n/2 ≈ n - 1`, plus `n` unit inserts, giving total cost `≤ 2n - 1`, so amortized cost per append is `O(1)`.

```python
def demonstrate_amortized_analysis(n: int = 17) -> float:
    """Trace cost of n appends under 2x growth and return amortized cost/op.

    Resize cost = size copied + 1 insert; regular append cost = 1.
    Total cost stays <= 2n - 1, so amortized cost -> O(1).
    """
    size, capacity, total_cost = 0, 1, 0
    for _ in range(1, n + 1):
        if size == capacity:
            cost = size + 1          # copy `size` elements + insert 1
            capacity *= 2
        else:
            cost = 1
        size += 1
        total_cost += cost
    return total_cost / n


amortized_cost = demonstrate_amortized_analysis(1000)
assert amortized_cost < 3.0, "amortized cost per append must stay O(1), i.e. bounded"
```

**Goal:** Understand why `np.append` is O(n^2) total and when to prefer Python `list` or pre-allocation.

**Approach:** `np.append` allocates a brand-new array and copies everything on every call (no capacity headroom), so n appends cost `0+1+2+...+(n-1) = O(n^2)`. Use a Python `list` (amortized O(1) append) and convert once, or pre-allocate a `numpy.ndarray` when the final size is known.

```python
import time
import numpy as np


def time_appends(n: int = 20_000) -> dict[str, float]:
    """Compare append strategies; returns wall-clock seconds per strategy."""
    results = {}

    start = time.perf_counter()
    py_list = []
    for i in range(n):
        py_list.append(i)          # amortized O(1) each -> O(n) total
    results["python_list"] = time.perf_counter() - start

    start = time.perf_counter()
    np_arr = np.array([], dtype=np.int64)
    for i in range(n):
        np_arr = np.append(np_arr, i)   # full copy every call -> O(n^2) total
    results["numpy_append_naive"] = time.perf_counter() - start

    start = time.perf_counter()
    np_fixed = np.empty(n, dtype=np.int64)
    for i in range(n):
        np_fixed[i] = i             # O(1) each, size known upfront
    results["numpy_preallocated"] = time.perf_counter() - start

    return results
```

## Pitfalls

- **Shrink at 1/4, not 1/2**: shrinking as soon as size drops below 1/2 capacity causes O(n) cost every time append/pop alternate right at that boundary (resize thrashing).
- **`ctypes.py_object` array raises `ValueError`/garbage on uninitialized access**: only ever read slots `< self._size`; the same applies to `numpy.empty`, which leaves memory uninitialized — never read beyond the tracked count.
- **`np.append` is not amortized O(1)**: it always allocates a new buffer and copies everything, giving O(n^2) total cost across n calls — never loop it; use `list.append` then `np.array(...)`, or pre-allocate.
- **`list.insert(0, x)` is O(n)**: every element shifts right; use `collections.deque` (O(1) append/pop from both ends) if you need frequent front operations.
- **CPython's real growth factor is ~1.125x, not 2x**: don't assume `sys.getsizeof(lst)` grows by exactly 2x per resize — verify empirically before relying on a specific over-allocation formula.

## See Also

- `algo-linked-lists` — alternative when frequent middle insertion/deletion matters more than O(1) append.
- `algo-stacks-queues` — deque-based O(1) front/back operations built on dynamic arrays or linked lists.
- `algo-complexity-analysis` — general amortized-analysis techniques (accounting, potential method).
- `algo-hash-tables-bloom` — another data structure whose resizing shares the same amortized-doubling analysis.
