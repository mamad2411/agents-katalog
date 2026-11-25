---
name: project-assistant
description: Use when any software project task may require project memory: code/file changes, new features, refactors, debugging, API/database/UI/desktop/deployment changes, docs updates, or final delivery checks that must keep .ai_project.md and docs/ aligned with the codebase.
---

# Project Assistant

## Purpose

Act as the project memory operator. Ensure each development task reads the right context before work, routes documentation updates after work, and leaves future sessions with accurate references.

Use with `documentation-and-adrs` for project rules and decisions, `docs-index-maintainer` for index updates, `project-sync-audit` for drift checks, and `zhuluyou` for cross-project user preferences.

V5.0 adds a closed-loop requirement: do not only write project memory. Make sure every durable record has a future read path and a maintenance trigger.

## Trigger

Invoke this skill when a task includes any of:
- Creating, editing, moving, deleting, or generating project files.
- Adding a feature, module, page, service, API, database object, Tauri command, desktop capability, deployment config, or test suite.
- Fixing a bug with lasting knowledge value.
- Changing architecture, module boundaries, build commands, dependencies, security, auth, release flow, or UI system.
- Creating or updating `.ai_project.md`, `AGENTS.md`, prompt files, or skills.
- The user repeats project-level requirements or explicitly says a rule should apply to this project going forward.

Do not invoke for simple Q&A that does not touch project state.

## Workflow

1. **Classify task**: feature, bug, refactor, UI, API, database, desktop, release, docs, prompt/skill, or audit.
2. **Read context**: load `.ai_project.md`, `AGENTS.md`, README, relevant docs, and nearby code/tests before modifying files.
3. **Create missing baselines**: for new/multi-step projects, use `scripts/init-project-memory.ps1` or `assets/ai_project_template.md` to create minimal `.ai_project.md` and required `docs/` folders before implementation.
4. **Support implementation**: keep new code within existing module boundaries; flag files nearing 1000 lines or mixed responsibility.
5. **Inspect changes**: after edits, compare changed files against documentation triggers.
6. **Update memory**: update `.ai_project.md` and matching `docs/` files when triggers apply.
7. **Update project rules**: update `AGENTS.md` when stable project-level AI collaboration rules change.
8. **Index docs**: every new/moved/deleted docs file must be reflected in `.ai_project.md` Docs Index.
9. **Close reuse loop**: for each durable record, define `Read When`, `Owner`, `Update Trigger`, and `Validation`.
10. **Report**: final answer must include `文档` and `演进记录` when changed; if not changed, give a short reason when docs were considered.

## Closed-Loop Memory Contract

Every new or updated project-memory entry must answer:

| Field | Meaning |
|---|---|
| Read When | Which future task must read this record before acting |
| Owner | Which role maintains the record: project-assistant, debugger, architect, rule-governor, or user-preference assistant |
| Update Trigger | Which code/config/doc/rule change makes this record stale |
| Validation | Which test, command, file check, or manual check proves the record still matches reality |

If these fields cannot be defined, do not create a standalone document. Put the information in a short candidate note or skip it.

## Read Matrix

| Task | Read first |
|---|---|
| Feature or upgrade | `.ai_project.md`, `docs/features/`, `docs/roadmap/`, related modules/tests |
| Architecture or refactor | `.ai_project.md`, `docs/architecture/`, `docs/decisions/`, `docs/maintenance/` |
| UI design/polish | UI docs, component/style system, screenshots/design references, relevant frontend code |
| API/client | `docs/api/`, API client/server modules, schemas, error handling |
| Database | `docs/database/`, migrations/schema, data access code |
| Tauri/desktop | `docs/desktop/`, `src-tauri/`, permissions, commands, updater/packaging docs |
| Bug/debug | `known-issues.md`, development log, related code/tests |
| Release | `docs/deployment/`, changelog, packaging/release config |
| Prompt/skills | `MANIFEST.md`, relevant `SKILL.md`, prompt files |
| Project AI rules | `AGENTS.md`, `.ai_project.md`, relevant docs, repeated user requirements |

## Update Matrix

| Change | Update |
|---|---|
| New/changed module, page, service, command, feature | `.ai_project.md` Features/Directory Map and `docs/features/` when behavior matters |
| API route, schema, auth, error contract | `.ai_project.md` APIs and `docs/api/` |
| Table, migration, index, transaction, RLS | `.ai_project.md` Database and `docs/database/` |
| Tauri command, permission, updater, native capability | `.ai_project.md` Desktop and `docs/desktop/` |
| Architecture boundary or major tradeoff | `docs/architecture/` and ADR |
| Known bug, workaround, technical debt, large file | `docs/maintenance/` |
| Build/test/release/deploy command | `.ai_project.md` Commands and `docs/deployment/` |
| New/moved/deleted docs file | `.ai_project.md` Docs Index |
| Repeated project-level user requirement | `AGENTS.md` |
| Cross-project user preference | `zhuluyou/references/profile.md` |

## Reuse Matrix

Use this matrix to prevent "recorded but never used" project memory.

| Record Type | Must Be Read When |
|---|---|
| `.ai_project.md` Stack / Commands | starting, testing, building, deploying, or changing tooling |
| `.ai_project.md` Directory Map / Module Boundaries | creating or moving files, adding modules, refactoring |
| `.ai_project.md` Features | modifying an existing feature or planning a related feature |
| `.ai_project.md` APIs | changing API routes, clients, schemas, auth, error handling |
| `.ai_project.md` Database | changing schema, migrations, indexes, transactions, RLS |
| `.ai_project.md` Desktop | changing Tauri commands, permissions, updater, packaging |
| `.ai_project.md` Known Risks | debugging, release, production-readiness checks, high-risk refactors |
| `docs/features/` | adding or changing user-facing behavior |
| `docs/architecture/` / ADRs | changing module boundaries, dependencies, runtime, auth, deployment |
| `docs/maintenance/debug-reports/` | debugging same symptom, same module, build/deploy failure, Tauri/db/auth issue |
| `docs/maintenance/technical-debt.md` | refactor, large-file work, simplification, production-readiness review |
| `AGENTS.md` | every coding task in that project before applying project-specific conventions |

## `AGENTS.md` Rules

`AGENTS.md` stores project-level AI collaboration rules.

Update `AGENTS.md` when:
- The user repeats the same project-level requirement.
- The user explicitly says the project should always/never follow a rule.
- The project gains a stable AI workflow requirement, test command, build command, forbidden area, or documentation rule.
- A repeated assistant mistake in this project should be prevented by a project rule.

Good `AGENTS.md` entries:
- "Before editing backend API code, read `docs/api/` and run `npm test -- api` when available."
- "Do not modify generated files under `src/generated/`."
- "New UI screens must define loading, empty, error, disabled, and success states."

Do not put in `AGENTS.md`:
- Cross-project user preferences. Put those in `zhuluyou`.
- Detailed feature design. Put that in `docs/features/`.
- Project index tables. Put those in `.ai_project.md`.

## `.ai_project.md` Minimum Sections

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

Keep `.ai_project.md` concise and index-like. Put detailed behavior in `docs/`.

## Bundled Resources

- `references/project-memory-schema.md`: exact `.ai_project.md` schema and writing rules. Read before creating or repairing project memory.
- `assets/ai_project_template.md`: baseline project memory template.
- `scripts/init-project-memory.ps1`: deterministic initializer for `.ai_project.md` and standard docs folders.

Run example:

```powershell
.\codex-v5.0-skill-pack\50-project-assistant\scripts\init-project-memory.ps1 -Root .
```

## Final Output Contract

For development tasks, include:

```markdown
文档：
- 更新 `.ai_project.md`
- 更新 `docs/features/example.md`
- 更新 `AGENTS.md`

演进记录：
- 记录 feature 状态或 ADR / technical debt
```

If no docs changed but the task touched code:

```markdown
文档：
- 未更新：本次仅修复局部实现，未改变长期项目知识。
```

For V5.0, also include a concise memory status when relevant:

```markdown
项目记忆：
- 读取：`.ai_project.md`, `docs/...`
- 更新：`docs/...`
- 复用入口：已写入 Docs Index / AGENTS / Read When
```

## Avoid

- Starting implementation without reading project context.
- Updating docs with generic summaries that do not help future work.
- Creating docs but not indexing them.
- Letting `.ai_project.md` become a long changelog.
- Mixing unrelated UI/API/database/deployment edits in one change.


