---
name: backend-refactor-quality-gate
description: >
  Quality gate for Fintrack.Server backend refactors in CeroBase: verify domain encapsulation, CQRS folder layout,
  Result-based application messaging, FluentValidation, EF migrations, API consistency, and mandatory tests before
  marking work complete. Use whenever refactoring aggregates (e.g. Guid migrations), restructuring Application
  commands/queries, aligning a feature with an established pattern such as Budgets, or any multi-layer backend change
  where "quick fixes" would leave the codebase inconsistent—load this skill first, then open only the referenced
  skill files needed for the task rather than duplicating their text.
---

# Backend refactor quality gate (Fintrack.Server)

This skill does **not** restate other skills. It defines **what “done” means** for a backend refactor and **which skills to read** to implement it correctly.

## When to use

- You are changing **Domain**, **Application**, **Infrastructure**, **API**, or **database shape** together.
- You are making a feature **consistent with an existing exemplar** (in this repo, **`Budget`** / **Budgets** are the default reference for CQRS + `Result` + folder layout).
- You touched **IDs, repositories, migrations, handlers, or controllers** and need a single checklist so nothing is forgotten.

## In-repo reference (concrete layout)

Use **`Application/Budgets/`** as the pattern for:

- One folder **per** command or query under `Commands/<UseCase>/` and `Queries/<UseCase>/`.
- `ICommand` / `ICommand<T>` / `IQuery<T>` with handlers returning **`Result`** / **`Result<T>`** (see messaging under `Fintrack.Server/Application/Abstractions/Messaging/`).
- Co-located **FluentValidation** `*Validator` types.
- **`ApiControllerBase`** + **`HandleResult`** / **`HandleFailure`** in API projects (see `Fintrack.Server/Api/Controllers/ApiControllerBase.cs`).

Use **`Domain/Budgets/Budget.cs`** as the pattern for a **rich aggregate** when that is the target (factory, private setters, domain events, `RegisterDeletion` where applicable).

## Completion checklist (must all be true before “done”)

Work through the list; for each row, **open the linked skill** and apply it—do not invent parallel conventions.

### 1. Intent and scope

- If the change is new behavior or ambiguous design, use **`brainstorming`** (`.agents/skills/brainstorming/SKILL.md`) before coding.

### 2. Domain layer

- **Entities, factories, invariants, encapsulation:** `.agents/skills/domain-entity-generator/SKILL.md`
- **`Result` / `Error` for domain rules (not thrown exceptions for business failures in the domain):** `.agents/skills/result-pattern/SKILL.md`
- **Domain events (if the aggregate should raise them):** `.agents/skills/domain-events-generator/SKILL.md`  
  - If you adopt outbox-style dispatch, follow `.agents/skills/outbox-pattern/SKILL.md` **as already wired** in this solution; do not fork a second pattern.
- **Aggregate persistence port:** repository interface stays with the aggregate under `Fintrack.Server/Domain/...` per `.agents/skills/dotnet-clean-architecture/SKILL.md` (Critical Rules + repository placement).

### 3. Application layer

- **Folder layout (one use case per leaf folder, grouped under `Commands/` / `Queries/`):** `.agents/skills/dotnet-clean-architecture/SKILL.md` (Application `{Feature}` folder layout).
- **Commands/queries detail:** `.agents/skills/cqrs-command-generator/SKILL.md`, `.agents/skills/cqrs-query-generator/SKILL.md`
- **Validators:** `.agents/skills/fluent-validation/SKILL.md`
- **Cross-cutting MediatR behaviors (if adding pipeline concerns):** `.agents/skills/pipeline-behaviors/SKILL.md`

### 4. Infrastructure

- **Repository implementations:** `.agents/skills/repository-pattern/SKILL.md`
- **EF mappings / constraints / relationships:** `.agents/skills/ef-core-configuration/SKILL.md`
- **Postgres/migration safety for non-trivial type changes:** `.agents/skills/supabase-postgres-best-practices/SKILL.md` (when writing raw SQL or tricky migrations)

### 5. API

- **Controller shape, MediatR, authorization:** `.agents/skills/api-controller-generator/SKILL.md`, `.agents/skills/permission-authorization/SKILL.md`
- Prefer **`Result` end-to-end** from handler to controller for commands/queries that already return `Result`, matching **`BudgetsController`** + **`ApiControllerBase`**.

### 6. Testing (mandatory — the refactor is NOT done until every layer is covered)

**Placement rules:** unit tests only in `Fintrack.Tests/`, integration tests only in `Fintrack.IntegrationTests/` — never inside `Fintrack.Server/`. See `AGENTS.md`.

Open each skill below and follow its **completion checklist** for the feature being refactored. Do not silently skip any layer — if a layer does not apply, acknowledge it explicitly.

- **Unit tests** (all layers): `.agents/skills/unit-testing/SKILL.md` — see the "Per-layer completion checklist" section. Covers:
  - Domain entity / aggregate tests
  - Command handler tests
  - Query handler tests
  - Validator tests
  - Repository tests (EF Core InMemory)
  - API controller unit tests (mock ISender)
- **Integration tests** (CRUD + authorization): `.agents/skills/integration-testing/SKILL.md` — see the "CeroBase monorepo completion checklist" section. Covers:
  - Functional CRUD tests (create, get, update, delete, user isolation)
  - Authorization tests (401, 403, read-only role)
  - Integration-test roles in `Roles.cs` / `RolePermissions.cs`
- **Green bar:** `dotnet test` passes for **both** `Fintrack.Tests` and `Fintrack.IntegrationTests` before claiming completion.

### 7. Persistence and data rollout

- If schema changed: **add an EF migration**, update snapshot, and document any **unsafe `Down`** (if used) for operators.
- Reseed or migration notes follow existing **`DefaultCategorySeeder`** / migration patterns—no ad hoc one-off scripts unless the task explicitly requires them.

### 8. Git

- Commit with **Conventional Commits**: `.agents/skills/conventional-commit/SKILL.md`
- If the API contract changes (**route shape, id type, status codes**), mark **breaking changes** in the commit footer when appropriate.

## Explicit anti-patterns (fail the gate)

- Multiple unrelated use cases in the same **leaf** Application folder (flat `Commands/` or `Queries/` dumping ground).
- Handlers that **throw** for normal business outcomes when **`Result`** is the established pattern for that feature area.
- **Business logic** left in controllers instead of MediatR handlers.
- **Tests** added under `Fintrack.Server/` (forbidden).
- **Domain** types referencing Application or Infrastructure.

## After the refactor

Offer to run **description optimization** only if this gate skill is installed in a **Claude Code** environment with the skill-creator scripts; see `.agents/skills/skill-creator/SKILL.md` (“Description Optimization”). For day-to-day refactors, completing the checklist is sufficient.
