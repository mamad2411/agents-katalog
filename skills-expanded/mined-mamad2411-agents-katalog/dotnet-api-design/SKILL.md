---
name: dotnet-api-design
description: Apply when defining or modifying Minimal API endpoints, DTOs, validators, or the exception-to-Problem-Details mapping in api/. Covers endpoint structure, single-DTO-per-entity, AutoMapper, FakeItEasy, FluentValidation, and RFC 7807 error handling.
metadata:
  stack: [dotnet]
---

# .NET Minimal API design

## Minimal API conventions

| Rule | Detail |
|---|---|
| Endpoint registration | Static classes with `Map*Endpoints()` extension methods on `IEndpointRouteBuilder` |
| Single DTO per entity | Nullable fields for response-only data (`Id`, `OwnerId`, audit fields) |
| No service layer for plain CRUD | Endpoint handlers call repositories directly |
| AutoMapper | Entity ↔ DTO mapping via assembly scanning; one `Profile` per aggregate |
| Mocking in tests | FakeItEasy (not Moq, not InMemory equivalents) |
| Request validation | FluentValidation; auto-discovered from the `*.Application` assembly |
| Persistence | Public setters on entities for SQL serialisation; logic enforced via `Create` / `Update` methods |
| Regex on entities | `[GeneratedRegex]` with `partial class` |

## Endpoint anti-patterns — do NOT put these in handlers

- Field classification logic (e.g. which fields are "structural" vs "non-structural").
- Conditional business logic (e.g. "if format changed, block update").
- Domain calculations or old/new state comparisons.
- Business rule checks beyond simple null/empty guards.

**Endpoints should ONLY:** validate auth → map DTOs → delegate to domain or application service → return HTTP response. Nothing else.

If the handler grows past these responsibilities, extract an application service (see `dotnet-clean-architecture` skill, "Service extraction criteria").

## Error handling (RFC 7807 Problem Details)

`ExceptionHandlingMiddleware` converts exceptions to Problem Details:

| Exception category | HTTP | Body | Notes |
|---|---|---|---|
| Domain state violation (e.g. `InvalidVerificationStateException`) | 409 | Echo `ex.Message` | Safe — message is synthesised from enum names + literal verbs |
| Domain not-found (e.g. `VerificationNotFoundException`) | 404 | Generic "Not found" | **Suppress** `ex.Message` |
| `ArgumentException` (validation) | 400 | Generic "Invalid request" | **Suppress** `ex.Message` |
| `UnauthorizedAccessException` (tampered signed state, invalid HMAC) | 401 | No body | |
| `ProviderException` (third-party / upstream failure) | 502 | Generic "Upstream provider unavailable" | |
| Unhandled | 500 | Generic body with a correlation id | Log `ex` internally at `Error` |

**Why suppress `ex.Message` for 400/401/404/500:** exception messages can leak internals — connection strings, Key Vault identifiers, file paths, stack frames. Only `InvalidVerificationStateException.Message` is safe to echo because it is composed of enum name + literal verbs.

## FluentValidation rules

Order rule chains: **mutual exclusivity → presence → format → business rules.**

Explicit rejection for mutually exclusive fields must come **before** "at least one required" — otherwise the user gets the wrong error message.

```csharp
RuleFor(x => x).Must(NotProvideBothFooAndBar).WithMessage("Foo and Bar are mutually exclusive");
RuleFor(x => x).Must(HaveAtLeastFooOrBar).WithMessage("Either Foo or Bar is required");
RuleFor(x => x.Foo).Matches(FooPattern);
RuleFor(x => x).MustAsync(BeUniqueFoo);
```

## Anti-patterns

- Multiple DTOs per entity (a create-DTO, an update-DTO, a response-DTO). Use one record with nullable response fields; reduces mapping noise.
- Repository-only mocking when a real EF context would catch a bug — but never use InMemory provider for SQL-specific behaviour (rowversion, unique indexes, raw SQL).
- `ex.Message` leakage to clients.
- Endpoint handler does the work without delegating; if you find a handler longer than ~20 lines of non-mapping code, extract a service.
