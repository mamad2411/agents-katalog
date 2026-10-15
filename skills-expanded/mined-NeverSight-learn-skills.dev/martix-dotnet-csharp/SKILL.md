---
name: martix-dotnet-csharp
description: Trigger when the task involves SDK-style .NET modernization, ASP.NET Core, EF Core, async/concurrency, diagnostics, testing, or security defaults; hand off FastEndpoints endpoint work to `martix-fastendpoints` and validator-focused FluentValidation work to `martix-fluentvalidation`.
license: Complete terms in LICENSE.txt
---

## MartiX .NET 10 and C# 14 router

- Standalone-first package for released .NET 10+ and C# 14+ practices.
- Ground decisions in the bundled rule files and Microsoft-backed reference
  maps.
- Take a **narrow route**: choose one domain map, read its linked rule, and
  expand only when the change crosses a named boundary.

## When to use this skill

- Review or modernize SDK-style .NET repos, including older baselines.
- Shape ASP.NET Core HTTP surfaces, options binding, results, and middleware.
- Review EF Core, async and concurrency, diagnostics, testing, or security
  defaults.
- Use companion skills for FastEndpoints endpoint authoring or
  FluentValidation-specific validator design.

## Compatibility stance

- Default to released .NET 10+ and C# 14+ guidance for greenfield work and
  explicit upgrade tasks.
- Older SDK-style repos are still in scope; stay within the repo's current
  target framework and language version unless the task includes upgrading
  them.
- Check the project file and shared build settings before recommending net10-only
  APIs, extension blocks, or other newer language or runtime features.

## First decision

1. For an existing repository, inspect `TargetFramework`, `LangVersion`,
   `global.json`, and shared build settings before selecting newer APIs.
2. Choose the closest domain row below and open its linked rule files.
3. Use [AGENTS.md](./AGENTS.md) only when the change crosses domains or needs a
   review route spanning several concerns.

For greenfield ASP.NET Core bootstraps, copy-ready patterns and their
trade-offs live in [Web bootstrap recipes](./references/web-bootstrap-recipes.md).
For recurring mistakes, start with the
[anti-patterns quick reference](./references/anti-patterns-quick-reference.md).

## Domain routing table

| Domain | Rule files | When |
| --- | --- | --- |
| Language | [lang-modern-features](./rules/lang-modern-features.md), [lang-pattern-matching](./rules/lang-pattern-matching.md), [lang-nullability](./rules/lang-nullability.md) | Modernizing syntax, branch clarity, or nullability contracts |
| SDK and build | [sdk-project-system](./rules/sdk-project-system.md), [sdk-build-test-pack-publish](./rules/sdk-build-test-pack-publish.md) | Editing `.csproj`, `global.json`, or build workflow |
| Runtime and performance | [runtime-memory-spans](./rules/runtime-memory-spans.md), [runtime-collections-immutability](./rules/runtime-collections-immutability.md) | Hot paths, spans, large buffers, or collection choices |
| Async and concurrency | [async-tasks-valuetasks](./rules/async-tasks-valuetasks.md), [async-cancellation-timeouts](./rules/async-cancellation-timeouts.md), [async-concurrency-channels](./rules/async-concurrency-channels.md) | `Task` vs `ValueTask`, cancellation, channels, or background work |
| Design | [design-api-type-design](./rules/design-api-type-design.md), [design-exceptions-validation](./rules/design-exceptions-validation.md) | New public APIs, DI boundaries, or exception contracts |
| Web | [web-aspnet-core](./rules/web-aspnet-core.md), [web-http-resilience](./rules/web-http-resilience.md) | ASP.NET Core shape, Minimal APIs, or outbound HTTP |
| Data | [data-serialization](./rules/data-serialization.md), [data-efcore](./rules/data-efcore.md) | JSON contracts or EF Core modeling and queries |
| Quality and security | [testing-unit-integration](./rules/testing-unit-integration.md), [diagnostics-logging-tracing](./rules/diagnostics-logging-tracing.md), [security-auth-authz](./rules/security-auth-authz.md) | Testing strategy, observability, or auth defaults |

## Handoff triggers

| Hand off to | When |
| --- | --- |
| `martix-fastendpoints` | The API surface is explicitly FastEndpoints — endpoint base types (`Endpoint<TRequest>`, `Endpoint<TRequest, TResponse>`), `Group`/`SubGroup` configuration, `IPreProcessor<>`/`IPostProcessor<>`, or `AddFastEndpoints(...)`/`UseFastEndpoints(...)` setup. |
| `martix-fluentvalidation` | Validation is a first-class design topic with reusable validators, RuleSets, async rules, localization, or `FluentValidation.TestHelper` usage. |
