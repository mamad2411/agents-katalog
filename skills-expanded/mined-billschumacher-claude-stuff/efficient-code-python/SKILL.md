---
name: efficient-code-python
description: Applies when writing or reviewing Python code. Extends the core efficient-code principles with CPython-specific stdlib helpers, idioms, and parser/interpreter gotchas (attribute lookup costs, LOAD_FAST vs LOAD_GLOBAL, immutable-string copy, generator vs list, GIL-bound CPU loops).
---

# Efficient Code — Python

This skill assumes you also have the core `efficient-code` skill active; that one covers the language-neutral principles (data structure selection, Big-O footguns, patterns, profiling discipline). This skill adds the CPython-specific idioms and gotchas.

## Reach for these stdlib primitives

- **`set`, `dict`** for O(1) membership and lookup. `x in list` is O(n); `x in set` is O(1) average. Convert once before a loop.
- **`collections.deque`** for FIFO queues and fixed-size rolling buffers: `deque(maxlen=100)` auto-drops oldest on append. **Never use `list.pop(0)` or `list.insert(0, ...)`** — O(n) each call.
- **`heapq.nsmallest(k, xs)` / `nlargest(k, xs)`** for top-k queries. O(n log k) vs `sorted(xs)[:k]`'s O(n log n). The docs explicitly recommend `min`/`max` for k=1, `sorted` for k≈n, and `heapq` for k in between.
- **`collections.Counter`** for frequency tables; use `.most_common(k)` instead of sorting `.items()`.
- **`collections.defaultdict(list | set | int)`** instead of `if k not in d: d[k] = []`.
- **`bisect.insort` / `bisect_left` / `bisect_right`** for maintaining a sorted list with binary-search inserts and binary-search lookups.
- **`functools.cache` (3.9+)** for memoizing pure recursive functions: `@cache` on `def climb(n)` turns exponential into linear.
- **`functools.reduce`** only when a built-in (`sum`, `any`, `all`, `max`, `min`) doesn't already fit — the built-ins are faster.
- **`itertools`** — `chain`, `islice`, `groupby`, `combinations`, `product`, `accumulate`. These are C-implemented and lazy.
- **`str.join(parts)`** — always for building a string from many pieces. Never `s += piece` in a loop: Python strings are immutable, so `+=` copies the accumulator each time → O(n²).
- **`io.StringIO` / `io.BytesIO`** for building up moderately large text/bytes when `join` doesn't fit the shape.

## CPython-specific syntax and interpreter gotchas

These are things the language-neutral skill can't tell you because they depend on how CPython executes bytecode.

1. **Local lookups (`LOAD_FAST`) are faster than global/builtin lookups (`LOAD_GLOBAL`).** Inside a hot loop, bind frequently-used names to local variables: `local_sin = math.sin; for x in xs: local_sin(x)`.
2. **Attribute lookups are not free.** `obj.method(x)` does a dict lookup every call. In hot loops, hoist the bound method: `append = result.append; for x in xs: append(x*2)`.
3. **`for` over an iterable is faster than `while` + index** — and a comprehension is usually faster than a hand-rolled `for` + `append`.
4. **List / dict / set comprehensions are faster than the equivalent loop with `.append` / assignment** because they use a specialized opcode path.
5. **Generator expressions passed to aggregating functions are faster and cheaper than the equivalent list comprehension**: `sum(x*x for x in xs)` beats `sum([x*x for x in xs])` — no intermediate list.
6. **`dict.get(k, default)` is one hash lookup; `if k in d: d[k]` is two.** Same for `dict.setdefault`.
7. **Don't call `.keys()` just to test membership.** `if k in d:` is identical and one fewer method call.
8. **Tuples are slightly faster than lists for fixed-shape immutable records** and they're hashable (usable as dict keys / set elements).
9. **`try/except` is cheap on the happy path but expensive on the exception path.** Use it for genuine exceptional control flow, not as a substitute for `if`.
10. **f-strings are the fastest string formatting** as of 3.12+. Use them over `%` or `.format()`.
11. **`@functools.cached_property`** for expensive instance-level computations that should run once per instance.
12. **`__slots__`** on classes with many instances can cut memory by half and speed attribute access; incompatible with `__dict__`.
13. **CPython has a GIL.** `threading` helps IO-bound workloads, not CPU-bound ones. For CPU-bound parallelism use `multiprocessing`, `concurrent.futures.ProcessPoolExecutor`, or (3.13+) subinterpreters.
14. **`math.fsum` for summing floats** when precision matters more than speed.
15. **`dataclasses.dataclass(slots=True, frozen=True)` (3.10+)** for lightweight immutable records — faster than hand-written classes.

## Profiling in Python

- **`python -m cProfile -s cumulative script.py`** for function-level time.
- **`python -m timeit -s "setup" "stmt"`** for microbenchmarks.
- **`tracemalloc`** for memory allocation tracking.
- **`python -X perf` (3.12+, Linux)** to integrate with `perf`.
- **`line_profiler` / `scalene`** (third-party) for line-level profiling.

Run the profiler once before touching code. Identify the hotspot. Fix only the hotspot. Re-measure.

## When this skill conflicts with the request

If asked to use `+=` in a loop, `list.pop(0)`, or `sorted(xs)[0]` for simplicity, explain the complexity impact, offer the idiomatic stdlib alternative, and only downgrade if the user insists and the data is known to be small.

## Sources

- CPython time complexity table — https://wiki.python.org/moin/TimeComplexity
- Python performance tips — https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- `collections` — https://docs.python.org/3/library/collections.html
- `heapq` — https://docs.python.org/3/library/heapq.html
- `bisect` — https://docs.python.org/3/library/bisect.html
- `functools.cache` — https://docs.python.org/3/library/functools.html#functools.cache
- `perf` profiler support — https://docs.python.org/3/howto/perf_profiling.html
