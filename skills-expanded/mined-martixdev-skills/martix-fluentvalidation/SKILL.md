---
name: martix-fluentvalidation
description: FluentValidation guidance for `AbstractValidator<T>` authoring, built-in validator selection, RuleSets/cascade flow, `ValidateAsync(...)`, `ValidationProblem`, `FluentValidation.TestHelper`, runtime metadata/localization, and 11/12 upgrades. Use when a .NET task centers on validator behavior, API-boundary validation, validator tests, or FluentValidation migration decisions.
license: Complete terms in LICENSE.txt
---

# MartiX FluentValidation

This router is the entrypoint for FluentValidation-specific work in .NET apps.
Open only the closest map/rule for the task and keep decisions source-backed.

## Use this skill for

- `AbstractValidator<T>` authoring and composition.
- Built-in validator selection before `Must`, `Custom`, or custom property validators.
- RuleSets, conditions, cascade behavior, messages, property paths, and
  dependent rules.
- `ValidateAsync(...)`, cancellation, and API-boundary `ValidationProblem` mapping.
- `FluentValidation.TestHelper` validator tests and targeted boundary tests.
- FluentValidation version planning and 11/12 migration cleanup.

## Quick routes

| Task | Start with | Add when needed |
| --- | --- | --- |
| New validator | [Validator basics](./rules/foundation-validator-basics.md) + [built-in validators map](./references/built-in-validators-map.md) | [Collections and composition](./rules/foundation-collections-composition.md) |
| API boundary | [ASP.NET Core integration](./rules/integration-aspnet-core.md) + [Web bootstrap recipes](./references/web-bootstrap-recipes.md) | [Async validation](./rules/integration-async-validation.md) |
| Async bug | [Async validation](./rules/integration-async-validation.md) + [Anti-patterns quick reference](./references/anti-patterns-quick-reference.md) | [Testing map](./references/testing-map.md) |
| Validator tests | [Test helper usage](./rules/testing-validator-testhelper.md) + [Testing bootstrap recipes](./references/testing-bootstrap-recipes.md) | [Integration boundaries](./rules/testing-integration-boundaries.md) |
| Upgrade plan | [Current baseline](./rules/upgrade-current-baseline.md) + [breaking changes](./rules/upgrade-breaking-changes-history.md) | [Upgrade map](./references/upgrade-map.md) + [compatibility matrix](./references/compatibility-matrix.md) |

## Default decisions

- Prefer built-in validators before extensibility points.
- Use `ValidateAsync(...)` with ambient `CancellationToken` whenever any async
  rule/dependency exists.
- Prefer manual boundary validation over legacy MVC auto-validation unless
  migration-constrained.
- Start with validator black-box tests; add boundary tests only when framework
  wiring is contractual.

## Workstream maps

- Foundation: [foundation map](./references/foundation-map.md)
- Built-in validators: [built-in validators map](./references/built-in-validators-map.md)
- Rule configuration: [rule configuration map](./references/rule-configuration-map.md)
- Integration: [integration map](./references/integration-map.md)
- Extensibility: [extensibility map](./references/extensibility-map.md)
- Runtime metadata/localization: [runtime metadata map](./references/runtime-metadata-map.md)
- Testing: [testing map](./references/testing-map.md)
- Upgrade: [upgrade map](./references/upgrade-map.md)

## Boundary and handoff policy

- Stay here for FluentValidation behavior, APIs, metadata, testing, and upgrades.
- Hand off to `martix-dotnet-csharp` when host/API architecture, DI
  composition, or non-validation ASP.NET Core behavior dominates.
- Hand off to `martix-fastendpoints` when FastEndpoints pipeline behavior is central.
- Use `martix-markdown` only for markdownlint/authoring concerns.

Use [AGENTS.md](./AGENTS.md) for multi-workstream reviews, package inventory,
and long-form maintainer guidance.
