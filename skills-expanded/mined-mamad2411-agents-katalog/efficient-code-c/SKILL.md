---
name: efficient-code-c
description: Applies when writing or reviewing C code. Extends the core efficient-code principles with C-specific stdlib helpers (memcpy/memmove/bsearch/qsort), pass-by-value copies, strict aliasing, VLA/alloca danger, restrict, signed overflow UB, and LTO/perf flag discipline.
---

# Efficient Code — C

This skill assumes you also have the core `efficient-code` skill active. This one adds C-specific rules that depend on how C is parsed and compiled.

## Stdlib primitives

- **`memcpy(dest, src, n)`** — fastest bulk copy; source and destination must NOT overlap (UB otherwise).
- **`memmove(dest, src, n)`** — safe for overlapping regions; slightly slower due to a direction check.
- **`memset(p, c, n)`** — bulk byte fill; compilers often vectorize.
- **`memcmp(a, b, n)`** — faster than a hand loop for fixed-size comparisons.
- **`calloc(n, size)`** — can be faster than `malloc + memset` for large blocks (OS lazy zero-pages).
- **`bsearch(key, base, n, size, cmp)`** — O(log n) on a sorted array.
- **`qsort(base, n, size, cmp)`** — O(n log n) but function-pointer indirection kills inlining. For hot paths, a hand-written sort is often 2-5× faster.
- **`snprintf`** — always prefer over `sprintf`. Compute needed length with `snprintf(NULL, 0, ...)`.
- **`strlen` / `strcmp` / `strcpy`** — O(n) scans for NUL. Cache length when possible; prefer `memcpy`/`memcmp` when length is known.
- **No stdlib hash table.** Write one (e.g., open-addressing) or pull in `uthash` / `klib`.
- For hot paths use arena / bump / pool allocators instead of general `malloc`/`free`.

## C-specific gotchas

1. **Passing a large struct by value copies it at every call site.** Pass `const struct T *` instead.
2. **Returning a large struct by value** usually copies (NRVO is not guaranteed in C). Use an output pointer parameter.
3. **Variable-length arrays (VLAs)** allocate on the stack — unbounded input can blow it. Use `malloc` for dynamic sizes. `alloca` is non-standard and similarly unsafe.
4. **Strict aliasing:** casting a `double*` to `int64_t*` and dereferencing is UB. Use `memcpy` for type punning — compilers optimize it to a register move.
5. **`restrict` on pointer parameters** tells the compiler they don't alias, enabling vectorization and load hoisting. Apply on math kernels and buffer routines.
6. **Integer promotion:** `uint8_t a, b; a + b` is done in `int`. Watch for implicit widening in tight inner loops; cast explicitly if you mean it.
7. **Signed overflow is UB** — compilers use this to hoist checks. Prefer signed loop counters the compiler can assume won't wrap. Unsigned wraps modulo 2^N.
8. **`volatile` prevents caching a load in a register** — do not sprinkle it "for safety". It kills optimization. Use it only for memory-mapped I/O or signal handlers.
9. **`const` on a local or parameter does not prevent aliasing.** Only `restrict` does.
10. **Uninitialized locals are UB when read.** `-Wuninitialized` and `-Og` help but are not exhaustive.
11. **`inline` is a hint.** `static inline` in a header is the idiom for header-only helpers. Link-time optimization (`-flto`) matters more than `inline` keywords.
12. **`#pragma pack` changes struct layout** and can introduce unaligned loads that are slow (or trap) on some architectures.
13. **Unions for type punning are well-defined in C** (unlike C++), but `memcpy` is portable and friendlier to the optimizer.
14. **Cache-line false sharing:** two atomic counters in the same 64-byte line cause contention between cores. Pad them.
15. **Branch prediction:** `__builtin_expect(x, 1)` (GCC/Clang) on rare-error paths can help; measure before sprinkling.

## Build flags that matter

- `-O2` or `-O3` for release. `-O2` is usually the sweet spot; `-O3` enables more aggressive vectorization and inlining but can bloat code.
- `-flto` — link-time optimization; often a bigger win than any source-level tweak.
- `-march=native` on machines where the binary runs on the same CPU family — enables SSE/AVX.
- `-fsanitize=address,undefined` during development only — slow, but `ubsan` catches strict-aliasing and signed-overflow bugs your optimizer will punish.

## Profiling

`perf record -g ./a.out && perf report` on Linux; `Instruments` on macOS; FlameGraphs via Brendan Gregg's scripts.

## Sources

- https://en.cppreference.com/w/c
- https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
- https://port70.net/~nsz/c/c11/n1570.html (C11 draft)
- https://www.agner.org/optimize/
- Jens Gustedt, *Modern C* — https://gustedt.wordpress.com/modern-c/
