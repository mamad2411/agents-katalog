---
name: algorithms-data-structures
description: Apply algorithm design patterns, complexity analysis, and data structure selection when solving computational problems. Use when implementing search, sort, graph traversal, dynamic programming, or when choosing between data structures for performance.
---

# Algorithms & Data Structures

Drawn from: *Introduction to Algorithms* (Cormen, Leiserson, Rivest, Stein — CLRS), *Data Structures and Algorithms in Java* (Goodrich & Tamassia), *Algorithms: Design and Analysis*.

## Complexity Analysis First

Before writing code, reason about time and space:

| Notation | Meaning |
|---|---|
| O(1) | Constant — hash lookup, array index |
| O(log n) | Logarithmic — binary search, balanced BST |
| O(n) | Linear — single pass, linear search |
| O(n log n) | Linearithmic — merge sort, heap sort |
| O(n²) | Quadratic — nested loops, bubble sort |
| O(2ⁿ) | Exponential — brute-force subset enumeration |

**Rules:**
- Drop constants and lower-order terms: O(3n + 5) → O(n)
- Worst case is the default unless average case is explicitly stated
- Space complexity matters as much as time in memory-constrained environments

## Choose the Right Data Structure

```
Need fast lookup by key?              → Hash map / hash set — O(1) average
Need ordered data + fast search?      → Balanced BST / sorted array — O(log n)
Need FIFO queue?                      → Linked list or deque
Need LIFO / recursion simulation?     → Stack
Need priority ordering?               → Binary heap / priority queue — O(log n) insert/extract
Need graph traversal?                 → Adjacency list (sparse), adjacency matrix (dense)
Need prefix/autocomplete?             → Trie
Need range queries?                   → Segment tree or BIT (Fenwick tree)
```

## Algorithm Design Patterns

### Divide and Conquer
Split problem into subproblems, solve recursively, combine.

```typescript
function mergeSort(arr: number[]): number[] {
  if (arr.length <= 1) return arr;
  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));
  return merge(left, right);
}

function merge(left: number[], right: number[]): number[] {
  const result: number[] = [];
  let i = 0, j = 0;
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) result.push(left[i++]);
    else result.push(right[j++]);
  }
  return result.concat(left.slice(i), right.slice(j));
}
```

### Dynamic Programming
Break into overlapping subproblems; memoize or tabulate results.

```typescript
// Top-down (memoization)
function fib(n: number, memo: Map<number, number> = new Map()): number {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n)!;
  const result = fib(n - 1, memo) + fib(n - 2, memo);
  memo.set(n, result);
  return result;
}

// Bottom-up (tabulation) — preferred for large n
function fibTable(n: number): number {
  if (n <= 1) return n;
  const dp = [0, 1];
  for (let i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }
  return dp[n];
}
```

DP decision checklist:
- Can the problem be broken into overlapping subproblems? → DP applies
- Is there an optimal substructure? (optimal solution uses optimal subsolutions) → DP applies
- State: what variables fully describe a subproblem?
- Transition: how does dp[i] depend on dp[i-1], dp[i-2], etc.?

### Greedy
Make the locally optimal choice at each step; prove it yields a global optimum.

```typescript
// Interval scheduling — maximize non-overlapping intervals
function maxIntervals(intervals: [number, number][]): [number, number][] {
  intervals.sort((a, b) => a[1] - b[1]); // sort by end time
  const result: [number, number][] = [];
  let lastEnd = -Infinity;
  for (const [start, end] of intervals) {
    if (start >= lastEnd) {
      result.push([start, end]);
      lastEnd = end;
    }
  }
  return result;
}
```

### Backtracking
Explore all possibilities; prune branches that cannot lead to a solution.

```typescript
function permutations(nums: number[]): number[][] {
  const result: number[][] = [];
  function backtrack(current: number[], remaining: number[]) {
    if (remaining.length === 0) { result.push([...current]); return; }
    for (let i = 0; i < remaining.length; i++) {
      current.push(remaining[i]);
      backtrack(current, [...remaining.slice(0, i), ...remaining.slice(i + 1)]);
      current.pop();
    }
  }
  backtrack([], nums);
  return result;
}
```

## Graph Algorithms

```typescript
// BFS — shortest path in unweighted graph
function bfs(graph: Map<number, number[]>, start: number): Map<number, number> {
  const dist = new Map<number, number>([[start, 0]]);
  const queue = [start];
  while (queue.length > 0) {
    const node = queue.shift()!;
    for (const neighbor of graph.get(node) ?? []) {
      if (!dist.has(neighbor)) {
        dist.set(neighbor, dist.get(node)! + 1);
        queue.push(neighbor);
      }
    }
  }
  return dist;
}

// DFS — cycle detection, topological sort, connected components
function dfs(graph: Map<number, number[]>, node: number, visited: Set<number>) {
  visited.add(node);
  for (const neighbor of graph.get(node) ?? []) {
    if (!visited.has(neighbor)) dfs(graph, neighbor, visited);
  }
}
```

**When to use BFS vs DFS:**
- BFS → shortest path (unweighted), level-order traversal, finding nearest node
- DFS → cycle detection, topological sort, path existence, connected components

## Binary Search

```typescript
function binarySearch(arr: number[], target: number): number {
  let lo = 0, hi = arr.length - 1;
  while (lo <= hi) {
    const mid = lo + Math.floor((hi - lo) / 2); // avoids overflow
    if (arr[mid] === target) return mid;
    else if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1; // not found
}
```

Binary search applies beyond arrays — whenever you can answer "is the answer ≥ X?" in O(1) or O(log n), you can binary search on the answer.

## Sorting Cheat Sheet

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Tim sort (built-in) | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |

Use the built-in sort for most cases. Only implement custom sorts when performance profiling shows it matters.

## Design Checklist

When solving a computational problem:

1. **Clarify** — constraints, input size, edge cases (empty, single element, duplicates)
2. **Estimate** — what complexity can you afford? For n=10⁶, O(n log n) is fine; O(n²) is not
3. **Pattern match** — divide/conquer? DP? Greedy? Graph traversal?
4. **Prove correctness** — especially for greedy (exchange argument) and DP (optimal substructure)
5. **Handle edge cases** — empty input, single element, negative numbers, integer overflow
6. **Test** — smallest input, largest input, worst-case input

## Anti-Patterns

- Using O(n) search in a loop when a hash map gives O(1)
- Rebuilding a data structure on every iteration instead of maintaining it incrementally
- Recursive solutions without memoization on overlapping subproblems
- Sorting when a linear scan or heap suffices
- Choosing an algorithm before understanding input size constraints
