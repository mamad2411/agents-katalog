---
name: layer-boundaries
description: Use when implementing or reviewing namespace, assembly, and project-reference boundaries for layered .NET solutions.
---

# Layer Boundaries

## Specialization

Define and enforce stable namespace, assembly, and dependency boundaries across models, services, and repositories in .NET solutions.

## Trigger Conditions

Invoke this skill when any of the following is true:

- Implementing or reviewing namespace and assembly organization in a .NET solution.
- A dependency direction violation is suspected between layers.
- A new project or assembly is being added and boundary placement needs validation.

## Namespace Pattern

- Use feature-first namespaces with explicit layer suffixes:
  - `<RootNamespace>.<Context>.<Subcontext>.Models`
  - `<RootNamespace>.<Context>.<Subcontext>.Services`
  - `<RootNamespace>.<Context>.<Subcontext>.Repositories`
- Keep repository interfaces and implementations in the same namespace.
- Use file-scoped namespaces.

## Naming Conflict Avoidance

- Avoid namespace segments that collide with common type names.
- If a context token could collide with a type (for example `Exchange`, `Drop`, `User`), add a disambiguating subcontext segment:
  - Preferred: `<RootNamespace>.Exchanges.Trades.Models`
  - Avoid when possible: `<RootNamespace>.Exchange.Models` with a type named `Exchange`
- If a collision exists in legacy code, use explicit aliases (`using ExchangeEntity = ...`) until a full namespace rename is approved.

## Assembly Rules

- Keep layer separation explicit at assembly boundaries.
- Align project and namespace naming 1:1 whenever practical:
  - Namespace `<RootNamespace>.Security.Authentication.Models` -> assembly `<RootNamespace>.Security.Authentication.Models`
- Do not place model records/classes in `*.Services` or `*.Repositories` assemblies.
- Do not place service classes in `*.Models` or `*.Repositories` assemblies.
- Do not place repository implementation classes outside `*.Repositories` assemblies.

## Allowed Dependency Direction

Use one-way dependencies only:

1. `*.Models` -> no project references to `*.Services` or `*.Repositories`.
2. `*.Services` -> may reference `*.Models` and repository abstractions.
3. `*.Repositories` -> may reference `*.Models` and data-access libraries only.
4. API/host/composition roots -> may reference all implementation layers for DI wiring.

## Implementation Checklist

Before creating or editing code, ensure:

1. The target namespace ends with exactly one layer suffix: `.Models`, `.Services`, or `.Repositories`.
2. The file location mirrors namespace segments after `<RootNamespace>`.
3. New types do not introduce namespace/type-name ambiguity.
4. New project references do not violate allowed dependency direction.
5. Any alias added for ambiguity is temporary and documented in the change summary.
6. Shared imports are centralized in approved project-level imports files and not duplicated ad hoc across many files.
7. Keep exactly one top-level type per `*.cs` file; only nested types may share a file with their containing type.

## Refactor Rules

- For boundary refactors, move files physically to match namespace structure in the same change.
- Update API endpoints, dependency-injection installers, and tests in the same change set.
- Run focused unit tests for affected projects after each boundary move.

## Inputs

- User request context and target scope.
- Root namespace and target layer.
- Affected projects and dependency graph.

## Required Outputs

- Boundary decision summary for namespaces, assemblies, and references.
- Concrete code/project edits aligned with dependency rules.
- Verification summary for impacted tests and boundary checks.

## Workflow

1. Identify affected layers and current namespace/assembly layout.
2. Validate intended dependencies against one-way direction rules.
3. Apply namespace, file-location, and project-reference updates.
4. Run focused checks/tests for impacted boundaries.
5. Record temporary aliases, exceptions, and follow-up cleanup decisions.
