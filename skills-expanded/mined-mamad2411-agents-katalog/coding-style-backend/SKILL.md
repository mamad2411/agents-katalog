---
name: coding-style-backend
description: C# coding conventions for the BallastLane backend — file-scoped namespaces, one-type-per-file, records for Commands/Queries/DTOs, sealed handlers/validators/controllers, async naming, MediatR naming, pattern matching. Load this skill whenever writing or editing any C# file in Domain, Application, Infrastructure, or WebAPI — before creating a handler, command, DTO, entity, controller, or validator.
---

# Coding Style — Backend (C#)

Apply these conventions to every C# file. They are cross-cutting — this skill is the one to load whenever you author or edit backend code, regardless of layer. See the `clean-architecture` skill for *where* code goes; this covers *how it's written*.

## File Organization

- **File-scoped namespaces always.**
- **One type per file**, file name matches the type (`CreateTaskHandler.cs` contains `CreateTaskHandler`).
- **One use case per folder** under `UseCases/` — `Command`/`Query`, `Handler`, `Validator`, `Response` live together.

## Type Declarations

- **Records for Commands, Queries, and DTOs** — immutability and value equality fit MediatR requests naturally.

```csharp
public sealed record CreateTaskCommand(string Title, string Description, DateTime DueDate, Guid UserId)
    : IRequest<CreateTaskResponse>;

public sealed record TaskResponse(Guid Id, string Title, string Status, DateTime DueDate);
```

- **Constructor injection for Controllers and Handlers.** Keep the injection style consistent across the solution — consistency matters more than which style is newer.
- **`sealed` on Handlers, Validators, and Controllers** unless a class is explicitly designed for inheritance.
- **`internal` by default**, `public` only where a project boundary requires it.

## Expressions and Patterns

- **Pattern matching over if-else chains** for status/enum branching.

```csharp
var label = task.Status switch
{
    TaskStatus.Pending => "Pending",
    TaskStatus.Completed => "Completed",
    _ => "Unknown"
};
```

- **Collection expressions** (`List<int> ids = [1, 2, 3];`) where the target framework supports them.

## Naming

- **Async suffix on all async methods** (`GetTaskByIdAsync`, not `GetTaskById`).
- **PascalCase** for public members/types/methods; **camelCase** for locals/parameters.
- **MediatR naming:** `<Verb><Entity>Command` / `<Verb><Entity>Query`; handler is the same name + `Handler` (`CreateTaskCommand` → `CreateTaskHandler`).
- **Repository interfaces:** `I<Entity>Repository` (these live in Domain — see the `clean-architecture` skill); implementation `<Entity>Repository` in Infrastructure.

## Related skills

- `clean-architecture` — layer boundaries and where each type belongs.
- `packages-backend` — how to add NuGet packages without pinning stale versions.
