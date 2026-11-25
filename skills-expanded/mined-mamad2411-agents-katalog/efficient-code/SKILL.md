---
name: efficient-code
description: Applies whenever writing, reviewing, or refactoring code that processes collections, loops, recursion, files, or strings — in any language. Enforces data-structure selection, Big-O awareness, space complexity, and profile-before-optimize discipline. Language-neutral; pairs with a language-specific efficiency skill (e.g., efficient-code-python) when one is loaded — those cover stdlib idioms plus syntax/parser/compiler-level gotchas that the core skill cannot.
---

# Efficient Code (language-neutral)

Create a complexity analysis report of the code you are writing, reviewing, or refactoring, BEFORE making any changes. 
These are **principles**. The exact primitive name and the exact syntax cost vary by language — consult the language-specific efficiency skill for your stack if one is loaded. That skill will cover stdlib helpers, idiomatic patterns, **and** syntax/parser/compiler gotchas (e.g., a language where `for` is faster than `forEach`, or where a boxed type allocates, or where a slice grows via amortized copy).

## Choose the right data structure

Pick data structures by the operations you need to be fast, not by habit:

- **Hash set / hash map** for membership, deduplication, and grouping. Average **O(1)** lookup/insert/remove. Use when you need "is this in the collection?" or "what's associated with this key?" without needing ordering.
- **Double-ended queue (deque)** for FIFO/LIFO workloads or fixed-size rolling buffers. **O(1)** push/pop at both ends. A plain array/list/slice has **O(n)** cost to remove from the front.
- **Priority queue / binary heap** for "give me the smallest/largest so far" or top-k queries. **O(log n)** insert and extract-min. Much better than re-sorting on each update.
- **Sorted container / balanced BST / tree map** when you need ordered iteration *and* fast lookup by key or range. **O(log n)** per operation.
- **Tuple / fixed-size record / struct** for small, fixed-shape values. Often hashable and cheaper than growable containers.
- **Trie** for prefix lookups over many strings.
- **Bloom filter / HyperLogLog** for approximate membership or cardinality at large scale when a false-positive rate is acceptable.

Rule of thumb: if you are about to search a list, ask "should this be a set or map instead?"

## Complexity footguns (the patterns LLMs reliably get wrong)

These are the anti-patterns that silently turn O(n) into O(n²) or worse. Each has a name; learn to spot them.

1. **`x in list` inside a loop.** Linear-scan membership test in a loop is O(n·m). Convert the right-hand side to a hash set once before the loop.
2. **`sorted(xs)[0]` / `sorted(xs)[-1]`** just to get the min or max. Sorting is O(n log n); min/max are O(n). Use the language's min/max helper.
3. **`sorted(xs)[:k]` / `sorted(xs)[-k:]`** for top-k. Sorting is O(n log n); heap-based n-smallest / n-largest is O(n log k). When k ≪ n, prefer the heap.
4. **Removing or inserting at index 0 of an array/list** in a loop. That's O(n) per call → O(n²) total. Use a deque.
5. **String concatenation with `+` or `+=` in a loop.** In languages with immutable strings (Python, Java, JavaScript, Go `string`, C# `string`), this copies the accumulator each iteration → O(n²) in total output length. Use a string builder / array-and-join / byte buffer.
6. **Nested loop with an equality or membership test.** Two nested linear scans are O(n·m). Hash one side into a set/map (O(n+m) total).
7. **Linear scan of already-sorted data.** If the collection is sorted, use binary search (O(log n)) instead of a for-loop with comparison.
8. **Recomputing the same pure value inside a loop.** If the value doesn't depend on the loop variable, hoist it out. If it does but has overlapping subproblems, memoize the function.
9. **Materializing a collection just to iterate it once.** If you only walk it once, use a stream/iterator/generator, not a concrete list.
10. **Reading an entire file when you only need to iterate it.** Stream line by line (or chunk by chunk). Large files shouldn't live in memory.
11. **`collection.length` / `len(x)` inside a loop condition** when the collection doesn't change. Hoist it to a local.
12. **Nested `.filter().map().filter()` chains that each allocate a new collection.** Chain the transformations through a lazy iterator or fuse them into a single pass.
13. **`exists_check` followed by `get`** on a map — two lookups when one would do. Use the language's "get-or-default" / "try-get" helper.
14. **Recursive function with overlapping subproblems and no memoization.** Classic trap: naive Fibonacci is O(2ⁿ). Memoize with a cache decorator / hash map.
15. **Deep copy when a shallow copy or a reference would do.** Know your language's value/reference semantics.

## Algorithmic patterns worth reaching for

When you see these problem shapes, reach for the matching pattern instead of brute force:

- **Two-pointer** — comparing or merging two sorted sequences, reverse-in-place, remove duplicates from sorted array.
- **Sliding window** — longest/smallest subarray satisfying a condition, fixed-size rolling statistics.
- **Prefix sums / running totals** — answering many range-sum queries over the same data in O(1) each after an O(n) preprocess.
- **Binary search** — on sorted data, or on the answer itself ("binary search on the answer" for monotonic predicates).
- **Memoization / top-down DP** — pure recursive function with overlapping subproblems.
- **Bottom-up DP** — when you can order subproblems by size and fill a table.
- **Topological sort** — dependency ordering in a DAG (build systems, scheduling).
- **Union-find (disjoint set)** — connectivity, cycle detection, Kruskal's MST.
- **Monotonic stack / queue** — next-greater-element, largest rectangle, sliding-window max.

You don't need to memorize the implementations, but you should recognize when a problem fits one of these so you can look up the library routine or classic pseudocode.

## Space complexity matters too

- Prefer iterators / generators / lazy sequences over materialized collections when the caller consumes once.
- Mutate in place when the caller doesn't need the original.
- Understand your language's value vs reference semantics so you don't make surprise copies.
- Stream files — don't `readAll` unless you actually need random access.
- Watch for hidden allocations: string splits, regex captures, map-then-collect pipelines, autoboxing, closure captures.
- When building a large structure, pre-size it if the size is known so the underlying buffer doesn't grow by repeated reallocation.

## Complexity analysis report

Before writing or modifying code that processes collections, produce a complexity analysis. Scale the depth to the task.

### When writing new code

Evaluate implementation options before choosing one:

```
## Complexity Analysis

**Problem:** One-line description of the operation
**Input size:** Expected n (or unknown)

| Approach | Time | Space | Trade-off |
|----------|------|-------|-----------|
| [Naive/brute force] | O(n²) | O(1) | Simple but quadratic |
| [Recommended] | O(n) | O(n) | Linear with hash set |
| [Alternative] | O(n log n) | O(1) | Sort-based, no extra memory |

**Selected:** [Which and why — consider input size, memory constraints, code simplicity]
```

Include at least the naive approach and the recommended approach. Skip this for trivial operations (single lookups, constant-time calls).

### When reviewing or refactoring existing code

Identify current complexity and propose improvements:

```
## Complexity Analysis

| Location | Current | Issue | Suggested | Improvement |
|----------|---------|-------|-----------|-------------|
| [func:line] | O(n²) | [nested loop with linear scan] | O(n) with hash set | [n·m → n+m] |
| [func:line] | O(n log n) | [sort just to find min] | O(n) with single pass | [log n factor removed] |
| [func:line] | O(n²) | [string += in loop] | O(n) with Builder/join | [quadratic alloc → linear] |

**Priority:** Fix [highest impact] first — dominates runtime for n > [threshold]
```

Focus on operations where the complexity class is wrong (O(n²) when O(n) is possible), not micro-optimizations within the same class.

## Profile before optimizing

Follow this order, every time:

1. **Make it work.** Correctness first.
2. **Make it right.** Readable, simple, well-tested.
3. **Make it fast.** Only if measurement shows it matters.

Rules:

- **Never optimize without a measurement.** Use your language's profiler.
- **Name the bottleneck** in one sentence before touching code. "The outer loop is O(n²) because of the in-list test on line 42" beats "it feels slow."
- **Optimize the hotspot, not the code that's easy to change.** Amdahl's law: speeding up something that runs 5% of the time gets you at most a 5% improvement.
- **Re-measure after the change.** Assume nothing.
- **Document surprising optimizations** with a comment explaining why the simple version is wrong.

Premature optimization is a real antipattern: complicating code for a speedup you can't measure makes it harder to maintain and often slower in practice due to cache misses, branch mispredicts, JIT deopts, or GC pressure.

## When this skill conflicts with the request

If the user asks for something that would be accidentally quadratic ("just loop through the list and check if each item is in the other list"), explain the complexity impact, offer the hash-based alternative, and only downgrade if the user insists and the data is known to be small.

## Sources

- *Introduction to Algorithms* (CLRS), Cormen, Leiserson, Rivest, Stein — formal complexity analysis, classical algorithms, dynamic programming.
- *The Algorithm Design Manual*, Steven Skiena — problem-pattern recognition, two-pointer, sliding window, DP recipes.
- CPython time complexity table — https://wiki.python.org/moin/TimeComplexity (most Big-O facts apply identically to equivalent primitives in other languages).
- Amdahl's law — https://en.wikipedia.org/wiki/Amdahl%27s_law
