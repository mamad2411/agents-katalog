---
name: efficient-code-csharp
description: Applies when writing or reviewing C# / .NET code. Extends the core efficient-code principles with C#-specific primitives (Span/Memory/ArrayPool, StringBuilder), struct-vs-class allocation, boxing pitfalls, LINQ materialization, ValueTask, ref structs, JIT tiering, and BenchmarkDotNet discipline.
---

# Efficient Code — C#

This skill assumes you also have the core `efficient-code` skill active.

## Stdlib primitives

- **`List<T>`** — contiguous array-backed, amortized O(1) `Add`. Preallocate via `new List<T>(capacity)`.
- **`Dictionary<K,V>` / `HashSet<T>`** — hash tables, average O(1). Preallocate via `new Dictionary<K,V>(capacity)`.
- **`SortedDictionary<K,V>`** — red-black tree, O(log n). **`SortedList<K,V>`** uses a sorted array (faster reads, slower inserts).
- **`StringBuilder`** — mutable string buffer for building strings in loops. For known-count cases, `string.Concat` / `string.Join` are fine.
- **`Span<T>` / `ReadOnlySpan<T>`** — stack-only slice, zero allocation. Works over arrays, `stackalloc`, strings, and unmanaged memory.
- **`Memory<T>` / `ReadOnlyMemory<T>`** — heap-storable analogue for async code (ref structs can't cross `await`).
- **`ArrayPool<T>.Shared.Rent(n)`** — pooled buffer rental; always `Return` in `finally`.
- **`System.IO.Pipelines`** — zero-copy streaming parse pattern for network and IO.

## C#-specific gotchas

1. **`foreach` on `List<T>` uses a struct enumerator (no allocation).** `foreach` on `IEnumerable<T>` boxes to an interface and allocates. Prefer concrete types in hot loops.
2. **LINQ is lazy and allocates.** Each `.Where().Select()` creates iterator objects and closure classes. In hot paths, use a plain `for`/`foreach`.
3. **Struct vs class:** structs are value types (copied on pass), classes are reference types (heap + GC). Large structs (>16 bytes) passed by value are expensive — use `in` parameters.
4. **Boxing:** passing a struct where an `object` or non-generic interface is expected allocates. Watch for `struct.ToString()` through `object`, `IEnumerable` on a struct field, etc.
5. **`async` / `await`** allocates a state-machine on first suspend. Returning `ValueTask` avoids the `Task` allocation when the result is usually synchronous.
6. **Capturing local variables in a lambda allocates a closure class.** Hoist outside loops when possible.
7. **`string` is immutable — `s += t` in a loop is O(n²).** Use `StringBuilder`.
8. **`default(T)` on a struct is cheap; `new T()` on a class allocates.**
9. **`readonly struct`** enables the compiler to skip defensive copies when you call methods on it.
10. **`stackalloc Span<byte>(n)`** allocates on the stack (bounded n!) — no GC pressure.
11. **`Dictionary<K,V>` lookups box the key if `K` is a struct without `IEquatable<K>`** — always implement it on custom structs used as keys.
12. **JIT tiered compilation:** hot methods get re-jitted with optimizations. Micro-benchmarks must warm up.
13. **Array covariance:** `object[] arr = new string[10]; arr[0] = 42;` throws at runtime and adds a per-store type check. Use `List<T>` or generics.
14. **`Span<T>` cannot be a field in a class or captured by an async method** (ref-struct restriction).
15. **`foreach` with value tuples from `Dictionary<K,V>.GetEnumerator()`** is efficient; do NOT call `.Keys`/`.Values` unnecessarily.

## Profiling

`dotnet-trace` + PerfView (Windows) or `dotnet-trace` + `speedscope` (cross-platform); **BenchmarkDotNet** for microbenchmarks — it handles warmup, statistical noise, and JIT tiers correctly.

## Sources

- https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/memory-t-usage-guidelines
- https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
- https://github.com/dotnet/BenchmarkDotNet
- https://devblogs.microsoft.com/dotnet/performance-improvements-in-net-8/
- https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/ref-struct
