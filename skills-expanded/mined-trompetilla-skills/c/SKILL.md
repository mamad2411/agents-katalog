---
name: C#
description: Avoid common C# mistakes — null traps, async pitfalls, LINQ gotchas, and disposal leaks.
metadata: {"clawdbot":{"emoji":"🟣","requires":{"bins":["dotnet"]},"os":["linux","darwin","win32"]}}
---

## Null Handling
- Enable nullable reference types `<Nullable>enable</Nullable>` — catches null issues at compile time
- `?.` returns null if left is null — chain safely: `obj?.Property?.Method()`
- `??` for default: `value ?? fallback` — `??=` for assign-if-null
- `!` null-forgiving hides bugs — prefer proper null checks or patterns

## Async Pitfalls
- `async void` only for event handlers — can't await, exceptions crash app
- `await Task.Run()` for CPU work — don't wrap already-async IO methods
- `ConfigureAwait(false)` in libraries — avoids deadlocks, not needed in app code
- `.Result` and `.Wait()` deadlock in UI/ASP.NET — always await instead
- Return `Task` not `void` — caller can't await void

## LINQ Traps
- `IEnumerable` is lazy — multiple enumeration re-executes query
- `.ToList()` or `.ToArray()` to materialize — when you need to iterate twice
- `.Count()` on IEnumerable iterates all — use `.Any()` for existence check
- `FirstOrDefault()` returns null/default — check before use or use `First()` if guaranteed
- LINQ to SQL executes on enumeration — `.ToList()` triggers DB call

## Equality
- `==` for reference types checks reference — override `Equals()` for value comparison
- `string` uses value equality with `==` — special case, works correctly
- Records use value equality by default — prefer records for DTOs
- Override `GetHashCode()` with `Equals()` — required for dictionary keys

## Value vs Reference
- `struct` copied on assignment — mutations don't affect original
- Mutable structs are dangerous — prefer readonly struct or class
- Boxing struct to interface allocates — performance trap in hot paths
- `ref` and `out` pass by reference — `in` for readonly ref (no copy, no mutation)

## Disposal
- `using` statement auto-disposes — `using var x = new Resource();` in modern C#
- `IAsyncDisposable` needs `await using` — for async cleanup
- Finalizers are expensive — implement only when wrapping unmanaged resources
- Event handlers prevent GC — unsubscribe to avoid leaks: `-=`

## Collections
- Modifying during `foreach` throws — copy to list or use `for` with index
- `Dictionary` throws on missing key — use `TryGetValue()` or `GetValueOrDefault()`
- `List<T>` not thread-safe — use `ConcurrentBag<T>` or lock
- Array size is fixed — use `List<T>` when size varies

## String Gotchas
- Strings are immutable — concatenation in loops creates garbage
- `StringBuilder` for multiple appends — or use `string.Join()`, interpolation for few
- `string.IsNullOrEmpty()` vs `IsNullOrWhiteSpace()` — latter catches " "
- `StringComparison.Ordinal` for perf — `OrdinalIgnoreCase` for case-insensitive

## Pattern Matching
- `is` pattern: `if (obj is string s)` — declares and assigns in one
- `switch` expression: `x switch { 1 => "one", _ => "other" }` — exhaustive
- Property patterns: `obj is { Name: "test" }` — concise null-safe check
- `not`, `and`, `or` patterns — combine: `is not null and { Length: > 0 }`
