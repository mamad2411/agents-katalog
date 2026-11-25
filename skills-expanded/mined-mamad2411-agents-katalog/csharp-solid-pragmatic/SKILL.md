---
name: csharp-solid-pragmatic
description: Pragmatic C# and ASP.NET Core design review, refactoring, and implementation guidance centered on SOLID, DI, maintainability, testability, and clean boundaries without unnecessary abstraction. Use when Codex needs to review or redesign a C# class hierarchy, service layer, controller, background job, repository, domain workflow, or feature slice; when requests mention SOLID, SRP/OCP/LSP/ISP/DIP, coupling, cohesion, testability, overengineering, YAGNI, KISS, or clean architecture; or when a user asks whether a C# design is too broad, too coupled, or too abstract.
---

# Pragmatic C# SOLID

## Overview

Apply SOLID as a decision framework, not as a ritual. Prefer the smallest design change that improves clarity, testability, and change safety in C# code.

Bias toward preserving existing team conventions and behavior. Introduce new abstractions only when they buy a real seam: a boundary, a second policy, a testable dependency, or a stable extension point.

## Workflow

### 1. Frame the design pressure first

Identify the concrete pain before proposing structure:

- Too many reasons to change
- Too many dependencies in one class
- Hard-to-test logic because of concrete infrastructure
- Repeated `if` or `switch` growth around policy differences
- Unsafe inheritance or surprising overrides
- Fat interfaces that force irrelevant members
- Global/static state or direct `new` inside domain/application services

If the code has no real pressure, do not force a pattern onto it.

### 2. Choose the lightest intervention

Prefer this order:

1. Keep the code as-is if it is already clear and local complexity is low.
2. Extract a private method if the problem is only readability.
3. Extract a focused class if responsibilities are mixed.
4. Introduce an interface only when a consumer benefits from a stable seam.
5. Introduce a strategy/factory/polymorphic model only when multiple behaviors must vary independently.

Use YAGNI as a brake:

- Do not create an interface for a single stable implementation with no boundary pressure.
- Do not build a generic framework for a one-off rule.
- Do not split code into many micro-types if the result obscures the use case.

### 3. Match the task mode

If the user asks for review:

- Flag correctness and data-integrity risks before architecture cleanup.
- Identify the highest-risk design issues first.
- Separate architecture problems from style-only cleanup.
- Recommend the smallest effective next step.

If the user asks for refactoring:

- Preserve behavior.
- Refactor in slices that can be tested.
- Improve seams only where they reduce real coupling or testing pain.

If the user asks for a new design:

- Start from the use case and feature boundary.
- Prefer a simple vertical slice over a broad layered abstraction plan.
- Read [references/aspnet-core-feature-slices.md](references/aspnet-core-feature-slices.md) when the task involves controllers, handlers, services, repositories, or application boundaries.

## SOLID Pass

### SRP

Ask: does this type have more than one reason to change?

Common smells:

- A controller/service validates input, maps DTOs, performs business rules, persists data, and sends notifications.
- A class has many injected dependencies.
- UI formatting and domain rules live in the same method.

Prefer:

- An orchestration shell that coordinates use-case steps
- Worker classes that each own one policy or concern
- A thin entry point that acts like a quarterback and delegates the work

### OCP

Ask: when a new business variant appears, do you add a new type or keep editing old conditionals?

Prefer extension when behavior genuinely varies:

- Strategy objects for rule families
- Policy interfaces for external behavior
- Registration-based composition in DI

Do not apply OCP blindly. If there is only one rule and no credible second variant, keep the code simple.

### LSP

Ask: can the subtype replace the base type without surprising callers?

Flag:

- Overridden members that throw `NotSupportedException` for normal calls
- Stronger preconditions in child types
- Weaker postconditions or broken invariants
- “Is-a” hierarchies that are really role differences

When inheritance lies, prefer composition or smaller role interfaces.

### ISP

Ask: does each consumer depend only on members it actually uses?

Prefer:

- Small role-based interfaces
- Consumer-specific abstractions
- Combined interfaces only when the consuming boundary truly needs the union

Avoid “god interfaces” that mix unrelated responsibilities.

### DIP

Ask: do high-level policies depend on abstractions or concrete infrastructure?

Prefer:

- Constructor injection for collaborators
- Composition root or DI container wiring at the edge
- Domain/application services that do not instantiate infrastructure directly

Allow direct `new` for value objects, simple data holders, and clearly local helper objects that do not create architectural coupling.

## C# Heuristics

Apply these by default unless the repo has an established alternative:

- Name things precisely. Use PascalCase for types and members, camelCase for locals and parameters, and `I` prefixes for interfaces.
- Keep one public type per file unless the local pattern clearly differs.
- Default to `private`; widen visibility only when needed.
- Prefer properties over public fields.
- Keep methods focused on one job and one abstraction level.
- Use braces for conditionals and loops even for single-line bodies.
- Prefer composition over inheritance unless the subtype relation is stable and substitutable.
- Validate external input early. Never trust user or network input.
- Avoid global mutable state and unnecessary statics.

## Async, Exceptions, and Tests

For deeper nuance, read [references/dotnet-guidance.md](references/dotnet-guidance.md).

Use these defaults:

- Prefer TAP-style async APIs with `Task` or `Task<T>`.
- Reserve `async void` for event handlers.
- Do not block on async work with `.Result` or `.Wait()` in normal application code.
- Catch exceptions only when you can recover, translate, or add useful context.
- Rethrow with `throw;`, not `throw ex;`.
- Keep unit tests fast, isolated, and explicit about one behavior.

## Review and Refactor Output

When reviewing code:

- Start with the highest-risk design problems.
- Explain which principle is being violated and why it matters in this code path.
- Distinguish between true architecture issues and style-only nits.
- Call out overengineering risk explicitly when proposed abstractions are not yet justified.

When refactoring:

- Preserve behavior first.
- Prefer small, staged changes over broad rewrites.
- Keep public APIs stable unless the user asked for breaking changes.
- Add or update tests when the refactor changes seams or behavior boundaries.

## Decision Shortcuts

Use these fast checks before adding abstraction:

- Two likely variants soon: abstraction may be justified.
- External boundary to mock or swap: abstraction is often justified.
- Single implementation with no seam pressure: concrete type is usually better.
- Many constructor dependencies: split responsibilities before adding more patterns.
- Base class with “unsupported” overrides: redesign the model.
- Repeated policy differences across workflows: consider strategy or policy abstractions.
- Infrastructure dependency at an application boundary: consider an interface at the boundary, not everywhere.

## References

- Read [references/dotnet-guidance.md](references/dotnet-guidance.md) for current .NET guidance on DI, naming, async, exceptions, testing, analyzers, and maintainability.
- Read [references/pragmatic-review-checklist.md](references/pragmatic-review-checklist.md) for a compact design-review checklist and C#-specific smell catalog.
- Read [references/aspnet-core-feature-slices.md](references/aspnet-core-feature-slices.md) for pragmatic controller/use-case/service/repository boundaries in ASP.NET Core.
