---
name: martix-platform
description: Use for MartiX.Platform library work and for designing, generating, reviewing, or hardening .NET web applications that should follow the MartiX modular-monolith, vertical-slice, SOLID, explicit-DI, TDD, secure, observable, and performance-oriented conventions. Trigger on MartiX.Platform, martix.platform.json, Generated Solutions, Platform migrations, Result/Error contracts, Problem Details adapters, reliable events, module boundaries, or requests to create a modern MartiX web app. Distinguish the shipped preview surface from the approved Wayfinder target before recommending APIs.
license: Complete terms in LICENSE.txt
---

# MartiX Platform router

Use this skill when the work is about the MartiX.Platform base library or a
web application intended to consume it. It is the architecture and Platform
convention layer, not a replacement for general C# or ASP.NET Core expertise.

## First decision

1. Inspect the consuming repository's target framework, package references,
   `martix.platform.json`, generated-solution manifest, and existing composition
   before proposing changes.
2. Read [authority-map](./references/authority-map.md) to decide whether a
   statement is current implementation, fixture evidence, or approved future
   direction.
3. Open the smallest rule or reference map below. Do not load the whole library
   for a one-concern change.

## Route by task

| Task | Start here | Add when needed |
| --- | --- | --- |
| Decide whether a Platform feature is available | [authority and status](./rules/foundation-authority-and-status.md) | [Platform surface](./references/platform-surface-map.md) |
| Choose a generated app shape or capabilities | [presets and capabilities](./rules/foundation-preset-capabilities.md) | [generated solution map](./references/generated-solution-map.md) |
| Design a new web app or module | [modular monolith](./rules/architecture-modular-monolith.md) | [vertical slices](./rules/architecture-vertical-slices.md), [composition and DI](./rules/platform-composition-ownership.md) |
| Add an endpoint or use case | [vertical slices](./rules/architecture-vertical-slices.md) | [Results, errors, and HTTP](./rules/http-openapi-contract.md) |
| Define a failure contract or error code | [Results, errors, and HTTP](./rules/http-openapi-contract.md) | [Platform surface](./references/platform-surface-map.md) |
| Add EF Core persistence or reliable events | [persistence and reliable events](./rules/persistence-efcore-reliable-events.md) | [migrations and AOT](./rules/delivery-migrations-aot.md) |
| Review security, telemetry, health, or performance | [security and operations](./rules/security-operations.md) | [testing and quality](./rules/testing-quality-performance.md) |
| Plan migrations, generation, or trimming/AOT | [migrations and AOT](./rules/delivery-migrations-aot.md) | [presets and capabilities](./rules/foundation-preset-capabilities.md) |
| Triage a likely design mistake | [anti-patterns](./references/anti-patterns.md) | The smallest linked rule |

## Default application stance

- Prefer the `modular-monolith` preset for production-oriented applications:
  one API, one one-shot Migrator, one project per genuine Business Module, and
  one consolidated test project unless a real boundary justifies more.
- Organize behavior by `Features/<Operation>` vertical slices. Keep endpoints
  thin and use internal sealed Application Operations with direct, explicit
  composition.
- Prefer Minimal APIs as the canonical transport. Treat FastEndpoints as an
  optional adapter with behavioral parity, not as a second architecture.
- Use explicit DI and module composition methods. Avoid scanning, reflection
  discovery, service location, generic mediators, catch-all shared projects,
  generic repositories, `IUnitOfWork`, and interface-per-class wrappers.
- Treat security, observability, migration behavior, performance, and tests as
  executable contracts rather than cleanup work.

## Current-versus-target guardrail

The Platform repository is still being implemented. Do not present Wayfinder
blueprint material as an API that is already shipped. Use
[authority and status](./rules/foundation-authority-and-status.md) whenever a
recommendation depends on a package, manifest claim, generated artifact, or
future migration.

## Handoffs

| If the primary question becomes... | Hand off to |
| --- | --- |
| General C#/.NET, ASP.NET Core, EF Core, async, diagnostics, or security practice outside MartiX conventions | `martix-dotnet-csharp` |
| FastEndpoints endpoint authoring or adapter-specific behavior | `martix-fastendpoints` |
| FluentValidation rules, RuleSets, localization, or validator testing | `martix-fluentvalidation` |
| TUnit or Microsoft.Testing.Platform mechanics | `martix-tunit` |
| Editing this skill's Markdown package | `martix-markdown` |

Stay in this skill when the decision concerns MartiX.Platform boundaries,
Generated Solution shape, module composition, Platform Result/Error contracts,
reliable-event semantics, or the web-app guardrails defined here.
