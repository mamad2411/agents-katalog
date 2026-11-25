---
name: pandas-performance
description: Speeds up slow pandas code by measuring first, then vectorizing, shrinking dtypes and chunking reads. Use it when a script is slow or runs out of memory.
---

# Pandas performance

Measure, change one thing, measure again, and prove the output did not change.

## Steps

1. Build a representative sample and keep the current output as the reference. Time the slow path with `time.perf_counter()` or `%timeit`, and record memory with `df.memory_usage(deep=True).sum()`.
2. Profile to find the hot line (`python -m cProfile -s cumtime script.py`). Do not optimize lines that are not hot.
3. Replace row loops. `iterrows`, `itertuples` and `apply(axis=1)` become column arithmetic, `np.where`, `np.select`, `.map` with a dict, or `merge` for lookups.
4. Shrink dtypes: `category` for low-cardinality strings, `int32` or `float32` where range allows (check with `pd.to_numeric(downcast=...)`), nullable ints only when nulls exist, and `datetime64` instead of strings.
5. Read less: pass `usecols=`, set `dtype=` at load, and read big files with `chunksize=` or switch to Parquet. Aggregate per chunk, then combine.
6. Avoid repeated `concat` in a loop; collect pieces in a list and concat once. Filter before merging, not after.
7. Compare the new result with the reference using `pd.testing.assert_frame_equal`.

## Rules

- No optimization without a measurement showing it helps.
- If the data is beyond one machine, say so and name polars or DuckDB rather than forcing pandas.

## Report

A table of step, time and memory before and after, the one change that mattered most, and the equality check result.
