---
name: dotnet-vertical-slice
audience: team
description: >
  Scaffold vertical slice architecture with CQRS + FreeMediator, including optional Telerik
  Blazor UI generation. Use when creating feature-based .NET projects with command/query
  separation and pipeline behaviors. Do NOT use when the project uses layer-based (N-tier)
  architecture — this skill enforces feature folder structure and will conflict with existing
  layer conventions.
---

# Vertical Slice Architecture with CQRS + FreeMediator

> "The whole idea is that the abstraction we use to reason about the system should be the feature, not the layer."
> -- Jimmy Bogard

## Core Philosophy

This skill scaffolds and maintains vertical slice architecture in .NET projects using FreeMediator for CQRS and pipeline behaviors. Every feature is a self-contained unit. Layers are an implementation detail inside the slice, not a project-level organizing principle.

**Non-Negotiable Constraints:**

1. **Feature Isolation** — Each feature lives in its own folder. No feature may reach into another feature's folder for types or logic.
2. **No Shared Base Handlers** — Abstract base handlers and handler inheritance defeat the purpose of vertical slices. Each handler is independent.
3. **Handler-Per-Feature** — Every command, query, or notification gets its own handler class. A single handler must never process multiple unrelated operations.
4. **Cross-Cutting via Pipeline** — Validation, logging, transactions, and caching are pipeline behaviors, not base class methods.
5. **CQRS Separation Is Structural** — Commands mutate state; queries return data. A single handler must never both read and write.

## Workflow

Scaffold proceeds in phases: **SCAFFOLD** (create folder and stub files) → **COMMAND or QUERY** (implement handler) → **PIPELINE** (wire behaviors) → **VALIDATE** (run tests, verify isolation). Use a notification (`INotification`) when an event must fan out to multiple handlers. When a feature both reads and writes, split it: extract the write as a command and the read as a separate query. Pipeline behaviors (validation, logging, transactions, caching) belong in `Infrastructure/Behaviors/` and are registered once in DI — they must never contain feature-specific conditional logic.

### Pre-Flight Checklist

- [ ] Feature has a clear, single responsibility
- [ ] Feature name describes the action, not the layer (e.g., `CreateOrder`, not `OrderService`)
- [ ] FreeMediator is registered in `Program.cs`
- [ ] FluentValidation is registered
- [ ] Pipeline behaviors registered in correct order
- [ ] `Features/` directory exists in the project

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase), AI Discipline Rules, Telerik Blazor UI Generation (Conditional), Anti-Patterns, Error Recovery.

## State Block Format

```
<vslice-state>
step: [SCAFFOLD | COMMAND | QUERY | NOTIFICATION | PIPELINE | VALIDATE]
feature: [description]
pattern: [command | query | notification]
folder_path: [path to feature folder]
last_action: [what was just done]
next_action: [what should happen next]
blockers: [any issues]
</vslice-state>
```

**Example:**

```
<vslice-state>
step: SCAFFOLD
feature: CreateOrder - creates a new order from a cart
pattern: command
folder_path: src/MyApp/Features/Orders/CreateOrder/
last_action: Created feature folder structure
next_action: Define CreateOrderCommand record and CreateOrderResponse record
blockers: none
</vslice-state>
```

## Output Templates

```markdown
## Vertical Slice Session: [Feature Name]
**Pattern**: [Command | Query | Notification] | **Folder**: `Features/[Domain]/[FeatureName]/`
**Files created**: Request, Response, Handler, Validator, Endpoint
**State**: [current vslice-state block]
**Next**: [action]
```

**Reference files:**

- [Feature Folder Patterns](references/feature-folder-patterns.md) — Folder layouts, request/response records, handler classes, validators, FreeMediator registration
- [Pipeline Behaviors](references/pipeline-behaviors.md) — Behavior implementations for validation, logging, transactions, caching
- [Vertical Slice Testing](references/dotnet-vertical-testing.md) — Testing patterns for handlers, validators, endpoints using xUnit and FluentAssertions

## Integration with Other Skills

- **`ef-migration-manager`** — When a slice requires schema changes, plan the migration alongside the feature. Define the entity first, then create the migration.
- **`tdd-loop`** — Each slice is an ideal TDD unit. Write a failing handler test (RED), implement minimally (GREEN), refactor. Handler isolation makes testing straightforward without mocking half the application.
- **`tdd-agent` (agent)** — For autonomous vertical slice development: scaffold the folder, write handler tests RED, implement GREEN, refactor.
