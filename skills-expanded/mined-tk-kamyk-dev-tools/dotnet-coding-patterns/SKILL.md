---
name: dotnet-coding-patterns
description: Apply when writing or reviewing C# in api/ — language-level conventions for style, async, repository queries, loop safety, and early-return control flow.
metadata:
  stack: [dotnet]
---

# .NET coding patterns

## General style

- **Clean Architecture** with dependency injection (see `dotnet-clean-architecture` skill).
- **DDD** — logic lives in domain entities, not in handlers.
- **Options Pattern** for all configuration — one `*Options` class per bound section, validated at startup.
- **4-space indentation**, Allman brace style, `var` for local declarations.
- **Record types** for DTOs, value objects, and simple data structures.
- **Primary constructors** — prefer primary constructors over explicit constructors + backing fields when a class only needs to capture its injected dependencies or initialisation data. Use captured parameters directly in the class body; do NOT add a `_name = name` field layer just out of habit. Explicit constructors remain acceptable when init logic is non-trivial (validation, computed fields from multiple inputs, multiple overloads).

## Control flow

- **Early returns** (guard clauses) over nested `if/else`.
- Handle simple / default cases first → return → main logic at top indentation.
- A method that ends with three layers of nesting almost always has a missed guard.

## Async patterns

- **Never `.Result`** on a Task — always `await`.
  - `.Result` deadlocks on synchronisation contexts and hides exceptions inside `AggregateException`.
  - Same with `.Wait()`, `.GetAwaiter().GetResult()`.
- For concurrent operations: `await Task.WhenAll(t1, t2, t3)`, then `await` each task individually to surface its result (or propagate its exception cleanly).
- `ConfigureAwait(false)` is unnecessary in ASP.NET Core (no sync context), so don't sprinkle it.

## Repository query design

- **Push filtering to the database.** No fetch-all + in-memory `.Where(...)`.
- Build WHERE clauses conditionally from optional parameters (`IQueryable` composition).
- **Parameterised queries only** — EF Core LINQ expressions, or `FromSqlInterpolated` with `FormattableString`. **Never** string-interpolation into raw SQL — SQL injection.
- Concurrency via `byte[] RowVersion` + `IsRowVersion()` (see `dotnet-data-access` skill), not application-level ETag headers.

```csharp
// Good
var query = _db.Cards.AsQueryable();
if (customerId is { } cid) query = query.Where(c => c.CustomerId == cid);
if (status is { } st)      query = query.Where(c => c.Status == st);
return await query.ToListAsync();

// Bad — fetches everything, filters in memory
var all = await _db.Cards.ToListAsync();
return all.Where(c => c.CustomerId == customerId && c.Status == status);
```

## Loop safety

- **Unbounded loops prohibited.** A `for(;;)` or `while(true)` must have a safety limit (e.g. `items.Count * 10`) and throw `InvalidOperationException` when reached.
- Extract complex loop bodies into `Try*` methods returning `bool` so the outer loop is the state machine and the body has one job.

```csharp
var maxIterations = items.Count * 10;
var iter = 0;
while (!IsDone(state))
{
    if (++iter > maxIterations)
        throw new InvalidOperationException($"Loop did not converge after {maxIterations} iterations");
    if (!TryAdvance(ref state))
        break;
}
```

## Anti-patterns

- `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` anywhere in production code.
- `async void` outside of event handlers.
- Repository methods that return `IEnumerable<T>` after materialising — return `IReadOnlyList<T>` to make intent explicit and avoid double enumeration.
- String concatenation / interpolation into SQL — even when "the input is trusted".
- `for(;;)` / `while(true)` without an iteration cap.
- Helper methods that hide async state machine creation (e.g. wrapping `await` in a `Task.Run` for "performance").
