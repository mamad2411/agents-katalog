---
name: dotnet-patterns
description: .NET (C#) stack conventions agentic-forge applies when the detected stack is .NET — the toolchain (dotnet build / test / format), nullable-reference-type and async idioms, testing discipline, layout, and the high-value C# pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# .NET patterns

The .NET stack pack (C#): loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports .NET. It carries only what is
**.NET-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md).
(Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's solution/scripts** — the `.sln`/`.csproj` and CI workflow. Defaults:

| Job | Conventional command | Gate |
| --- | --- | --- |
| build | `dotnet build` | clean (treat nullable warnings as errors if configured) |
| test | `dotnet test` | green; new behaviour covered |
| format | `dotnet format` | applied |

## Idioms

- **Nullable reference types on** (`<Nullable>enable</Nullable>` / `#nullable enable`); honour
  the warnings rather than `!`-suppressing.
- **`async`/`await` all the way** — never block on async (`.Result` / `.Wait()` deadlock);
  `ConfigureAwait(false)` in reusable **library** code (avoids capturing a caller's sync context;
  unneeded in ASP.NET Core app code, which has none); `CancellationToken` flows through.
- `record` types for data, switch expressions + pattern matching, **LINQ** (enumerate once),
  **`using` / `await using`** for `IDisposable` / `IAsyncDisposable`, expression-bodied members, `var`.
- Constructor **dependency injection** via the built-in container; program to interfaces.

## Testing

- **xUnit** (`[Fact]`/`[Theory]`) or NUnit, FluentAssertions, Moq/NSubstitute. Cover the happy
  path plus a boundary and an **exception** case. Deterministic — no real network/clock; fake
  the clock. Never weaken or delete a test to go green.

## Pitfalls (.NET / C#-specific, high-value)

- **`async void`** (except event handlers) — its exceptions escape the caller and can crash the
  process; **blocking on async** (`.Result`/`.Wait()` → deadlock in a sync context).
- **Not disposing `IDisposable`/`IAsyncDisposable`** (missing `using`/`await using`); missing
  `ConfigureAwait(false)` in libs.
- **Null-reference** despite NRTs (don't suppress with `!`); **multiple enumeration** of an
  `IEnumerable`; exceptions used for control flow; `==` on reference types vs `.Equals`.

## Definition of done (.NET)

`dotnet build` is clean (nullable warnings respected / as errors if configured), `dotnet test`
is green with the new boundary/exception cases, `dotnet format` applied, async-all-the-way with
no blocking, `IDisposable`s disposed — using the repo's own solution and commands.
