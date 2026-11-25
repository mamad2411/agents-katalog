# De-Sloppify — Per-Step Reference

Loaded by `/de-sloppify` Step execution. Details, safety checks, and code
examples for each of the 7 pipeline steps.

## Step 1: Format All Code

```bash
dotnet format
```

Why first: formatting touches many files. Getting it out of the way prevents
merge conflicts with subsequent steps.

Verify: `dotnet format --verify-no-changes` reports no changes.
Commit: `chore: apply dotnet format`

## Step 2: Remove Unused Usings

```bash
dotnet format analyzers --diagnostics IDE0005
```

Why second: unused usings are noise; removing them makes subsequent analysis
cleaner and reduces false positives in review.

Verify: `dotnet build`; run `dotnet test` if removal was extensive.
Commit: `chore: remove unused using statements`

## Step 3: Fix Analyzer Warnings

```
MCP: get_diagnostics(scope: "solution", severityFilter: "warning")
```

Triage by category, compiler warnings first:

- **Nullability (CS8600-CS8604)** — add null checks, or the null-forgiving
  operator with a comment explaining why null is impossible
- **Unused variables (CS0219)** — remove
- **Obsolete API (CS0618)** — migrate to the recommended replacement
- **IDE suggestions (IDE0xxx)** — apply if they improve readability

Verify: `dotnet build` with zero new warnings; `dotnet test` passes.
Commit: `chore: fix analyzer warnings`

## Step 4: Remove Dead Code

```
MCP: find_dead_code(scope: "solution", kind: "all")
```

**Safety check before every removal** — Roslyn cannot see string-based usage:

```
1. find_references(symbolName: "DeadType") — confirm zero compile-time refs
2. Grep for string-based usage:
   - nameof(DeadType) in attributes or logging
   - Reflection: Type.GetType("DeadType"), Activator.CreateInstance
   - DI registration: services.AddScoped(typeof(IHandler<>), typeof(DeadType))
   - Serialization: [JsonDerivedType(typeof(DeadType))]
3. Check if it's a public API consumed by external packages
4. Check configuration files (appsettings.json, etc.)

ONLY remove if all checks come back clean.
```

Verify: `dotnet build` and `dotnet test` pass.
Commit: `chore: remove dead code`

## Step 5: Resolve TODOs

```bash
grep -rn "TODO\|HACK\|FIXME\|XXX" --include="*.cs"
```

For each: **fix now** (small, self-contained), **create an issue** and tag it
(`// TODO(#142): Implement retry logic`), or **remove** (stale — the work was
done or is no longer relevant).

Verify: `dotnet build` and `dotnet test` pass.
Commit: `chore: resolve TODO comments`

## Step 6: Seal Non-Inherited Classes

```
MCP: find_dead_code(scope: "solution", kind: "type") — candidate type list
MCP: get_type_hierarchy(typeName: "EachClass") — check for derived types
```

Seal every class that has no derived types, is not a base class by design (no
`virtual`/`abstract` members), is not an open generic in DI registration, and
is not a test fixture base class.

Why: sealed classes enable devirtualization, communicate design intent, and
prevent accidental inheritance.

```csharp
// BEFORE
public class OrderValidator : AbstractValidator<CreateOrderCommand> { ... }

// AFTER — sealed, because nothing inherits from it
public sealed class OrderValidator : AbstractValidator<CreateOrderCommand> { ... }
```

Before sealing, also grep test projects for inheritance — a class tests derive
from must stay open:

```
MCP: get_type_hierarchy(typeName: "OrderService") → no derived types in production
Grep: "OrderService" in test projects → inheritance found? Skip sealing.
```

Verify: `dotnet build` and `dotnet test` pass.
Commit: `chore: seal non-inherited classes`

## Step 7: Propagate CancellationToken

```
MCP: detect_antipatterns(severity: "warning") — filter "missing CancellationToken"
```

Trace async chains from entry points (endpoints, handlers) through services to
data access. Common propagation points:

- Minimal API endpoints: add `CancellationToken ct` parameter (auto-bound)
- Mediator handlers: already provided in `Handle(TRequest, CancellationToken)`
- EF Core: `SaveChangesAsync(ct)`, `ToListAsync(ct)`, `FindAsync([key], ct)`
- HttpClient: `GetAsync(url, ct)`, `PostAsync(url, content, ct)`

```csharp
// BEFORE — token stops at the endpoint
app.MapGet("/orders/{id}", async (Guid id, AppDbContext db) =>
{
    var order = await db.Orders.FindAsync(id);
    return order is not null ? Results.Ok(order) : Results.NotFound();
});

// AFTER — token propagated to EF Core
app.MapGet("/orders/{id}", async (Guid id, AppDbContext db, CancellationToken ct) =>
{
    var order = await db.Orders.FindAsync([id], ct);
    return order is not null ? Results.Ok(order) : Results.NotFound();
});
```

Verify: `dotnet build` and `dotnet test` pass.
Commit: `chore: propagate CancellationToken through async chains`
