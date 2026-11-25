---
name: lang-csharp
description: C# (.NET 8/9) engineering, nullable reference types (#nullable enable), Span<T> memory efficiency, cancellation tokens, IDisposable/IAsyncDisposable with using, and Stryker mutation testing.
---

# C# & .NET Engineering Contract

## 1. Type Safety & State Discipline
- Enable nullable reference types unconditionally (`#nullable enable` or `<Nullable>enable</Nullable>`).
- Prohibit unvetted null-forgiving operators (`!`). Use explicit guards or `ArgumentNullException.ThrowIfNull()`.
- Use `record` or `record struct` for immutable data transfer objects.

## 2. Resource & Allocation Management
- All `IDisposable` and `IAsyncDisposable` instances must be bound to `using` declarations.
- Utilize `Span<T>`, `ReadOnlySpan<T>`, and `Memory<T>` for high-throughput slicing without heap allocations.
- Prohibit `unsafe` code blocks without formal escape-hatch registration in `.prumo/escape-hatches.json`.

## 3. Asynchronous & Concurrency Invariants
- Every asynchronous method must accept and propagate a `CancellationToken`.
- Never use `.Result` or `.Wait()` on Tasks (risk of deadlock); always `await` or configure `ConfigureAwait(false)` in library code.
