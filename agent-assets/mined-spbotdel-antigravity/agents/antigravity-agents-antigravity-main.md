# Codex Adapter Entry

## Scope Note

This is a framework/internal tooling document for Codex session orchestration.

Do not use it as the source of truth for the product architecture or documentation reading order.

For the application itself, start with:
- `REPO_MAP.md`
- `PROJECT_SUMMARY.md`
- `ARCHITECTURE_RULES.md`
- `DECISIONS.md`

## Purpose

This file is the Codex entry orchestrator for projects that use the framework.
It runs Codex workflows on top of shared project memory.

## Shared State

Primary memory files:
- `.claude/SNAPSHOT.md`
- `.claude/BACKLOG.md`
- `.claude/ARCHITECTURE.md`
- `CHANGELOG.md` (optional, if project tracks release notes)

Codex and Claude use the same state contract.

## Startup Context

On every `start`, load the startup context defined in `.codex/config/framework-adapter.json` under `startup_context_paths`.

Human-readable descriptions of the project documents live in `README.md`, but the runtime source of truth for the startup file list is `.codex/config/framework-adapter.json`.

## Command Routing

### `start`
Run:
- `bash .codex/commands/start.sh`

### `sart` (typo alias)
Run:
- `bash .codex/commands/sart.sh`

### `dev-status`
Run:
- `bash .codex/commands/dev-status.sh`

### `/fi`
Run:
- `bash .codex/commands/fi.sh`

### migration detection
Run:
- `bash .codex/commands/migration-router.sh`

### version check
Run:
- `bash .codex/commands/update-check.sh`

## Core Runtime

Shared command entry points:
- `python3 src/framework-core/main.py cold-start`
- `python3 src/framework-core/main.py completion`

Output contract:
- `.codex/contracts/core-cli-contract.md`


## Template Project Overview (Not Source Of Truth For Antigravity)
- Backend: FastAPI
- DB: PostgreSQL
- Queue: Celery
- Frontend: React

This section comes from framework scaffolding and is not the real product stack for this repository.

## Architecture rules
- API routes call services only
- Services may call repositories
- Repositories are the only DB access layer
- No business logic in controllers
- Reuse existing utilities before creating new ones

## Coding rules
- Always add type hints
- Prefer small focused functions
- Do not rename public APIs unless requested
- Update tests if behavior changes
- Keep patches minimal

## File Creation Policy

The Antigravity codebase prioritizes architectural stability and minimal surface area.

Agents must avoid introducing unnecessary new files.

### Default Principle

Prefer modifying existing modules over creating new ones.

Most changes should be implemented by extending:

- existing repository logic
- existing validators
- existing display/tree logic
- existing route handlers
- existing UI components

Creating a new file should be considered an exceptional step.

---

### Before Creating A New File

Before adding a new file, check whether the change can be implemented by:

1. extending an existing function
2. adding logic to an existing module
3. extending an existing API route
4. extending an existing component
5. extending the repository layer

If any of these are reasonable, do not create a new file.

---

### Allowed New File Cases

A new file may be created only when one of the following is clearly true:

- a new API route requires its own route file
- a database migration is required
- a new test file is needed for focused coverage
- an existing file would become significantly harder to maintain
- the repository already uses a clear pattern requiring a new module

---

### Forbidden Patterns

Do not introduce:

- parallel utility modules
- duplicate service layers
- alternative repository implementations
- redundant helper modules
- "temporary abstractions"
- new architectural layers

Do not create files simply to reduce the size of an existing file.

---

### Architecture-Sensitive Areas

Be especially cautious when adding files under:

- `lib/`
- `components/`
- `app/api/`

These directories define the core runtime structure.

Extending existing modules is strongly preferred.

---

### If A New File Is Created

If a new file is introduced, the agent must explain:

- why existing modules were not suitable
- why the new file is necessary
- how it fits the current architecture
- why it is the smallest correct change

The change summary must explicitly list all new files created.

## Workflow
Before editing:
1. Determine the task type and use `REPO_MAP.md` `Required Reading Matrix` to select the minimum docs to read
2. Read the relevant files
3. Explain current behavior
4. Propose a short plan
5. Then implement

After editing:
1. Run relevant tests / linters
2. Summarize changed files
3. List risks / follow-ups
