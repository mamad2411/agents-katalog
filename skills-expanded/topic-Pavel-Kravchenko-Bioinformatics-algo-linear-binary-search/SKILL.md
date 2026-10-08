---
name: algo-linear-binary-search
description: "Implement Python linear/binary search: first/last occurrence, lower_bound/upper_bound (bisect), rotated-sorted-array search. Use when finding an index, searching sorted data, counting duplicates, or finding an insertion point."
tool_type: python
primary_tool: Python
---

# Linear and Binary Search

## When to Use

- Finding the index of a value in a list/array (`find X in arr`, "search for element").
- Data is unsorted, small (< ~20 elements), a linked list, or searched only once → linear search.
- Data is sorted and searched repeatedly, or large → binary search, O(log n).
- Need the first/last position of a duplicated value, a count of occurrences, or an insertion point (`bisect_left`/`bisect_right` equivalents).
- Searching a sorted array that has been rotated (e.g., a circular buffer or a sorted log that wrapped around).

## Version Compatibility

Pure Python stdlib — no external dependencies. Verified on Python ≥3.8 (uses `typing.List`/`Optional`; on 3.9+ you can use built-in `list`/`None` union syntax instead). `bisect` module used for cross-checking is stdlib in every Python 3 version.

## Prerequisites

- No packages to install. Optional: `bisect` (stdlib) to validate `lower_bound`/`upper_bound` against `bisect_left`/`bisect_right`.
- Concepts: array indexing, `O(n)`/`O(log n)` complexity basics.

## Complexity

| | Linear | Binary |
|---|---|---|
| Best | O(1) | O(1) |
| Average/Worst | O(n) | O(log n) |
| Space (iterative) | O(1) | O(1) |
| Space (recursive) | O(1) | O(log n) — call stack |
| Prerequisite | None | Sorted array |

**Goal:** find the index of `target` in an unsorted or small collection.
**Approach:** scan left to right, return on first match, `-1` if exhausted.

```python
from typing import List


def linear_search(arr: List[int], target: int) -> int:
    """Search for target in arr using linear search.

    Time: O(n), Space: O(1). Works on unsorted data.
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

**Goal:** find `target` in a **sorted** array in O(log n).
**Approach:** repeatedly halve the search window `[left, right]`; compare `arr[mid]` to `target` to decide which half to keep.

```python
from typing import List, Optional


def binary_search_iterative(arr: List[int], target: int) -> int:
    """Iterative binary search on a sorted array.

    Time: O(log n), Space: O(1).
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # overflow-safe form
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binary_search_recursive(
    arr: List[int], target: int, left: Optional[int] = None, right: Optional[int] = None
) -> int:
    """Recursive binary search. O(log n) time, O(log n) stack space."""
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = left + (right - left) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

**Goal:** with duplicates present, find the first/last occurrence, count them, or find an insertion point (`bisect_left`/`bisect_right` equivalents).
**Approach:** on a match, don't stop — keep narrowing toward the boundary you want (left for "first", right for "last"); for bounds, use a half-open `[left, right)` window.

```python
from typing import List


def find_first_occurrence(arr: List[int], target: int) -> int:
    """Leftmost index of target in a sorted array with duplicates, or -1."""
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # keep searching left for an earlier match
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result


def find_last_occurrence(arr: List[int], target: int) -> int:
    """Rightmost index of target in a sorted array with duplicates, or -1."""
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1  # keep searching right for a later match
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result


def count_occurrences(arr: List[int], target: int) -> int:
    """Count occurrences of target via two O(log n) binary searches."""
    first = find_first_occurrence(arr, target)
    if first == -1:
        return 0
    return find_last_occurrence(arr, target) - first + 1


def lower_bound(arr: List[int], target: int) -> int:
    """First index with arr[i] >= target (equivalent to bisect.bisect_left)."""
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(arr: List[int], target: int) -> int:
    """First index with arr[i] > target (equivalent to bisect.bisect_right)."""
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:  # <= instead of < is the only diff from lower_bound
            left = mid + 1
        else:
            right = mid
    return left
```

**Goal:** search a sorted array that was rotated at an unknown pivot (e.g. `[4,5,6,7,0,1,2]`, originally `[0,1,2,4,5,6,7]`).
**Approach:** one half of `[left, mid, right]` is always properly sorted; check which half is sorted, then check if `target` falls in that half's range to decide where to recurse.

```python
from typing import List


def search_rotated_array(arr: List[int], target: int) -> int:
    """Search a rotated sorted array (no duplicates) in O(log n)."""
    if not arr:
        return -1
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        if arr[left] <= arr[mid]:  # left half [left..mid] is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # right half [mid..right] is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


def _demo() -> None:
    """Self-check: run against Python's bisect and known test cases."""
    import bisect

    sorted_dups = [1, 3, 5, 5, 5, 7, 9]
    assert find_first_occurrence(sorted_dups, 5) == 2
    assert find_last_occurrence(sorted_dups, 5) == 4
    assert count_occurrences(sorted_dups, 5) == 3
    assert count_occurrences(sorted_dups, 4) == 0
    for target in [0, 1, 4, 5, 6, 9, 10]:
        assert lower_bound(sorted_dups, target) == bisect.bisect_left(sorted_dups, target)
        assert upper_bound(sorted_dups, target) == bisect.bisect_right(sorted_dups, target)

    assert binary_search_iterative(list(range(1, 10)), 7) == 6
    assert binary_search_iterative([], 5) == -1
    assert binary_search_recursive(list(range(1, 10)), 7) == 6

    rotated = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated_array(rotated, 0) == 4
    assert search_rotated_array(rotated, 6) == 2
    assert search_rotated_array(rotated, 3) == -1
    assert search_rotated_array([1], 1) == 0
    assert search_rotated_array([2, 1], 1) == 1

    print("all checks passed")


if __name__ == "__main__":
    _demo()
```

## Pitfalls

- Integer overflow in `(left + right) // 2` — safe in Python (arbitrary precision), but use `left + (right - left) // 2` if porting to C/Java.
- Off-by-one errors: `left <= right` (inclusive bounds, classic search) vs `left < right` (half-open bounds, used for `lower_bound`/`upper_bound`) require different loop conditions and updates — mixing them causes infinite loops or missed elements.
- Binary search on unsorted data silently returns a wrong index — no exception is raised.
- `find_first_occurrence`/`find_last_occurrence` must *not* return immediately on a match — stopping early only finds *a* match, not the boundary one.
- Rotated-array search: don't assume the *left* half is unsorted just because `arr[left] > arr[mid]` — that only tells you the *right* half is the sorted one; check both cases explicitly.
- For real code, prefer stdlib `bisect.bisect_left`/`bisect.bisect_right` over hand-rolled `lower_bound`/`upper_bound` — they're implemented in C and battle-tested.

## See Also

- algo-sorting-fundamentals (data usually needs sorting before binary search applies)
- algo-complexity-analysis
- algo-tree-structures (binary search trees generalize binary search to dynamic data)
