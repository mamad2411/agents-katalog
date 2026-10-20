---
name: dotnet-data-access
description: Apply when persisting aggregates with EF Core in api/ — optimistic concurrency via RowVersion, idempotent application-service retry, FluentValidation rule ordering for write requests.
metadata:
  stack: [dotnet]
  requires: [dotnet-clean-architecture]
---

# .NET data access (EF Core)

## Optimistic concurrency

- Every aggregate persisted to SQL Server carries a `byte[] RowVersion` property configured as `IsRowVersion()` in the EF mapping.
- `DbUpdateConcurrencyException` is translated in the repository to a domain-level conflict exception (`InvalidVerificationStateException` or equivalent) — which surfaces as HTTP 409 via the exception middleware (see `dotnet-api-design`).
- Repositories with unique-index races (e.g. email-keyed aggregates) translate `DbUpdateException` the same way: catch, inspect the inner SQL exception number, throw the domain conflict exception.

## Idempotent callbacks

Application services that can be hit by **concurrent callbacks** (typical pattern: a vendor redirect comes back at the same time as a webhook) must:

1. Wrap `UpdateAsync` in a `try` / `catch (DbUpdateConcurrencyException)`.
2. Reload the aggregate.
3. If the aggregate is now in a **terminal** state, return that state — duplicate callers get an idempotent response, not a 409.
4. If still in a non-terminal state, the lost-race caller can retry the operation.

```csharp
try
{
    aggregate.Mutate(...);
    await _repo.UpdateAsync(aggregate);
}
catch (DbUpdateConcurrencyException)
{
    var winning = await _repo.GetAsync(aggregate.Id);
    if (winning.IsTerminal)
        return winning.ToResult(); // idempotent — winner already finished
    throw new InvalidVerificationStateException(...); // genuine conflict
}
```

This pattern is the difference between a flaky integration and one that survives a vendor's "callback both ways at once" behaviour.

## FluentValidation rule ordering (for writes that hit the DB)

Order: **mutual exclusivity → presence → format → business rules.**

Explicit rejection for mutually exclusive fields must come **before** "at least one required" — otherwise the user gets the wrong message. (Also stated in `dotnet-api-design`; mirrored here because write-side validators are where rule order shows up.)

```csharp
RuleFor(x => x).Must(NotBothFooAndBar).WithMessage("Foo and Bar are mutually exclusive");
RuleFor(x => x).Must(EitherFooOrBar).WithMessage("Either Foo or Bar is required");
RuleFor(x => x.Foo).Matches(FooPattern);
RuleFor(x => x).MustAsync(BeUniqueFoo);
```

## Anti-patterns

- Application-level ETag headers as a substitute for `RowVersion` — keep the concurrency token where EF can manage it.
- Catching `DbUpdateConcurrencyException` and rethrowing as 500 — that's data loss masquerading as a bug.
- Forgetting the reload-and-check pattern in callback handlers — leads to "the webhook randomly fails because the redirect won the race".
- Validators that put async DB checks (`MustAsync(BeUnique...)`) before cheap synchronous checks — slow and noisy.
- Cross-aggregate transactions. One transaction modifies one aggregate (see `dotnet-clean-architecture` skill, "Cross-aggregate references").
