---
name: efficient-code-cpp
description: Applies when writing or reviewing C++ code. Extends the core efficient-code principles with C++-specific STL container choices, copy/move semantics, reserve discipline, virtual dispatch cost, string_view, RVO, lambda capture gotchas, and compiler optimization flags.
---

# Efficient Code — C++

This skill assumes you also have the core `efficient-code` skill active.

## STL container choices

- **`std::vector<T>`** — contiguous, cache-friendly. `reserve(n)` before a known-size fill to avoid reallocation. Amortized O(1) `push_back`. Almost always the right default.
- **`std::array<T, N>`** — fixed-size stack array, zero overhead over a C array, with iterators.
- **`std::unordered_map` / `std::unordered_set`** — hash table, average O(1). Call `reserve(n)` to avoid rehashing. **`absl::flat_hash_map`** is typically 2-3× faster if a dependency is acceptable.
- **`std::map` / `std::set`** — red-black tree, O(log n), ordered iteration.
- **`std::deque`** — chunked; not contiguous, slower iteration than `vector`. Use only when you need fast push/pop at both ends.
- **`std::list` / `std::forward_list`** — node-per-element, cache-hostile. Almost never the right choice.
- **`std::string`** — has small-string optimization (typically ≤15-22 chars on the stack). Use `std::string_view` for read-only parameters — zero copy.
- **`std::span<T>` (C++20)** — non-owning view over contiguous memory. Pass instead of `const vector&` when the callee doesn't need ownership.
- **`<algorithm>`** — `std::sort` is introsort (O(n log n)); `std::lower_bound` / `std::upper_bound` for binary search; `std::partition` for single-pass partitioning.
- **`std::pmr::*`** (C++17) — polymorphic allocators for arena/pool allocation.

## C++-specific gotchas

1. **`for (auto x : container)` copies each element.** Use `for (const auto& x : ...)` or the universal reference form `for (auto&& x : ...)`.
2. **Copy constructors fire more than you think** — return-by-value, container insertion, passing by value. Make your types movable and use `std::move` to hand off ownership.
3. **`emplace_back(args...)` vs `push_back(x)`** — `emplace_back` constructs in place, skipping a temporary.
4. **`vector` reallocation invalidates all iterators, pointers, and references.** `reserve()` up front is often the single biggest performance win.
5. **Virtual function calls prevent inlining and add indirection.** In hot loops, prefer CRTP (static polymorphism) or mark leaf classes `final` to enable devirtualization.
6. **`std::shared_ptr` has atomic refcount ops on every copy/destroy.** In single-threaded hot paths, prefer `unique_ptr` or raw pointers with clear ownership.
7. **`std::function` is type-erased and often heap-allocates.** Use templates or function pointers on hot paths.
8. **Exception throwing is expensive but the non-throwing path is essentially free on Itanium ABI.** Don't avoid exceptions for speed, avoid them for API clarity.
9. **RVO / NRVO:** returning a named local by value is usually elided. Returning `std::move(local)` can PREVENT NRVO — don't do it.
10. **Strict aliasing:** `reinterpret_cast` between unrelated pointer types is UB. Use `std::bit_cast` (C++20) or `memcpy`.
11. **`std::endl` flushes the stream.** Use `'\n'` in loops.
12. **`std::unordered_map` is node-based** per standard requirement. Iteration is slow compared to a flat hash map.
13. **Template instantiation bloats binaries and slows compiles.** Prefer explicit instantiation in a .cpp when a template is used with few types.
14. **Lambdas with captures may or may not allocate** depending on the callable type they're assigned to. Capturing by reference into a heap-stored callable can dangle.
15. **Initialization order of globals across translation units is unspecified.** Avoid global state that depends on other global state.

## Compiler flags

- `-O2` or `-O3` for release builds.
- `-flto` — link-time optimization, often a large win.
- `-march=native` when the binary runs on the same CPU family.
- `-fvisibility=hidden` in libraries to enable more inlining.
- `-fsanitize=address,undefined,thread` during development only.

## Profiling

`perf` + FlameGraph (Linux); Instruments (macOS); Intel VTune (cross-platform); `callgrind` for call-count accuracy; Google Benchmark for microbenchmarks.

## Sources

- https://en.cppreference.com/w/cpp
- https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
- https://abseil.io/fast/
- https://github.com/google/benchmark
- https://quick-bench.com/
