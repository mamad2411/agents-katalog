---
name: project-maintenance
description: Maintain long-lived project context for software projects. Use when creating or modifying project code, adding features, changing architecture, adding files, changing APIs, database schema, deployment, tests, or documentation. Ensures .ai_project.md and docs/ are read before work and updated after meaningful changes.
---

# Project Maintenance

## Purpose

Keep the project understandable across future Codex sessions and future developers.

`.ai_project.md` is the project index. `docs/` contains detailed references. Both must stay aligned with code.

Use with `project-assistant` for orchestration, `project-evolution` when the change affects roadmap/ADRs/technical debt/history, and `docs-index-maintainer` when docs files are created, moved, renamed, or deleted.

## Read Before Work

Read relevant maintenance docs before:
- Adding or changing a feature.
- Modifying project code.
- Refactoring modules.
- Changing API, database, auth, desktop capabilities, deployment, build, tests, or docs.
- Debugging behavior that may be documented.
- Creating new files or directories.

Minimum read set:
1. `.ai_project.md`
2. `AGENTS.md` if present
3. README or equivalent
4. Relevant docs subfolder
5. Nearby code and tests

Project Assistant handoff:
- Before implementation: provide only task-relevant project facts to the active role.
- After implementation: inspect changed files and decide which `.ai_project.md` / `docs/` updates are required.
- If no documentation update is needed after code changes, record a concise reason in the final answer.

If docs are missing:
- Continue for small fixes.
- For new projects or multi-step features, create baseline `.ai_project.md` and required docs.
- Mention missing docs in the final answer when it affects continuity.

## Update `.ai_project.md`

Update when any of these change:
- Tech stack, package manager, runtime, framework, or major dependency.
- Start, build, test, lint, deploy, or packaging command.
- Directory structure or module ownership.
- New feature, page, service, command, API, table, job, integration, or desktop capability.
- Important architectural decision or long-term constraint.
- Current project progress, known risk, or next-step todo.

Recommended sections:

```markdown
# Project Context

## Stack
## Commands
## Directory Map
## Module Boundaries
## Features
## APIs
## Database
## Desktop / Native Capabilities
## Decisions
## Docs Index
## Current Progress
## Known Risks
```

Keep entries concise, factual, and linked to detailed docs.

Docs Index entries should identify path, purpose, read trigger, and related area. Use `docs-index-maintainer` for index drift or docs reorganization.

## Update `docs/`

Create or update the right document based on change type:

| Change | Destination |
|---|---|
| Architecture, module boundaries, data flow | `docs/architecture/` |
| Feature behavior, user flow, acceptance notes | `docs/features/` |
| API endpoints, schemas, errors, auth | `docs/api/` |
| Tables, migrations, indexes, transactions | `docs/database/` |
| Desktop capabilities, Tauri commands, permissions | `docs/desktop/` |
| Deployment, env vars, packaging, rollback | `docs/deployment/` |
| Important decisions | `docs/decisions/ADR-xxxx-title.md` |
| Development progress | `docs/changelog/development-log.md` |

## Documentation Rules

- Document facts that help future work.
- Do not write generic summaries.
- Include paths, commands, APIs, modules, and decision reasons when useful.
- Keep docs aligned with code in the same change when feasible.
- If docs would become large, split by feature or module.
- Treat documentation as part of the change when behavior, interfaces, structure, or operations change.
- Avoid creating documentation debt during feature work; if documentation cannot be updated, state the reason and record a follow-up.

## File And Module Rules

- Keep files under 1000 lines where practical.
- When a file approaches 1000 lines or mixes responsibilities, split by module, component, service, hook, utility, type, route, or test.
- Put new functionality in the existing module if ownership is clear.
- Create a new folder only when it represents a real domain, feature, platform layer, or shared utility.
- Avoid mixing UI, API client, database, deployment, and unrelated refactors in one change.

## Final Answer Requirements

For development tasks, include `文档` when maintenance files changed:

```markdown
文档：
- 更新 `.ai_project.md`
- 新增 `docs/features/export-flow.md`
```

If docs should have changed but did not, state why.
