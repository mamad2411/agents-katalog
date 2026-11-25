---
name: docs
description: "Analyze codebase and manage project docs/. Actions: init (generate all docs from codebase scan), update (post-feature update), summarize (refresh codebase-summary only). Use: /docs [init|update|summarize]"
---

# /docs - Project Documentation

Analyze the codebase and manage the `docs/` directory.

**Input:** Action via `$ARGUMENTS`: `init`, `update`, or `summarize`

---

## /docs init — Generate all docs (first-time setup)

For a project with no `docs/` or incomplete documentation.

### Step 1: Scan codebase

Read the following to understand the project:
- `package.json` — dependencies, scripts, project name
- `.claude/rules/stack-rules.md` — stack, architecture patterns, commands
- `src/` directory structure — map all modules/features
- Existing `README.md` or `README.MD` if present
- `.env.example` if present — environment variables required

### Step 2: Generate docs/

Create the `docs/` directory. Generate each file:

#### `docs/code-standards.md`

Extract from codebase scan:
- **Naming conventions** — files, variables, functions, classes (derive from existing code)
- **Architecture patterns** — established patterns in src/ (derive from stack-rules.md + actual code)
- **Import conventions** — path aliases, barrel exports
- **Anti-patterns** — things explicitly avoided (from stack-rules.md anti-patterns section)
- **Pre-commit rules** — lint, build, test commands from stack-rules.md

Keep under 150 lines. Scannable, actionable. No duplication with stack-rules.md.

#### `docs/codebase-summary.md`

- **Project overview** — what the system does, who uses it
- **Module map** — list all src/ modules with one-line description each
- **Key entities/models** — main data structures (from entity/model files)
- **External integrations** — APIs, services the project calls
- **Feature inventory** — list of implemented features, grouped by domain
- **Key dependencies** — important packages and their purpose (from package.json)

Keep under 200 lines.

#### `docs/module-index.md`

**Purpose:** Quick-reference index for AI skills to locate code without scouting. Scan `src/` deeply to extract:

- **Services** — class name → file path → key public methods
- **Controllers** — class name → file path → HTTP endpoints it handles
- **Entities/Models** — class name → file path → key fields
- **DTOs** — grouped by module, file paths listed
- **Enums/Constants** — name → file path

**Format:**
```markdown
## Services
| Class | File | Key Methods |
|-------|------|-------------|
| DealService | src/deal/deal.service.ts | create, findAll, close, calculateCommission |
| AgentService | src/agent/agent.service.ts | findById, updatePoints |

## Controllers
| Class | File | Endpoints |
|-------|------|-----------|
| DealController | src/deal/deal.controller.ts | POST /deals, GET /deals/:id, PATCH /deals/:id/close |

## Entities
| Entity | File | Key Fields |
|--------|------|-----------|
| Deal | src/deal/entities/deal.entity.ts | id, status, closedAt, agents, commissions |

## Enums
| Enum | File | Values |
|------|------|--------|
| DealStatus | src/deal/enums/deal-status.enum.ts | OPEN, CLOSED, CANCELLED |
```

Keep under 250 lines. Scan ALL files in src/ — this is the one file that replaces codebase scouting.

#### `docs/system-architecture.md`

- **Architecture diagram** (ASCII or Mermaid) — layers and data flow
- **Module relationships** — which modules depend on which
- **Request flow** — how a request travels through the system (BE) or user action flow (FE)
- **Database overview** — main entities and relationships (BE only)
- **State management** — how state flows (FE only)

Keep under 150 lines.

#### `docs/deployment-guide.md`

Extract from stack-rules.md and .env.example:
- **Environment variables** — list from .env.example with descriptions
- **Setup steps** — getting the project running locally
- **Build and deploy commands** — from stack-rules.md Commands section
- **Environments** — dev / staging / production differences if known

Keep under 100 lines. Leave placeholders if info not found.

### Step 3: Report

```markdown
## Docs Generated

- docs/code-standards.md      [X lines]
- docs/codebase-summary.md    [X lines]
- docs/system-architecture.md [X lines]
- docs/deployment-guide.md    [X lines]

**Review recommended:**
- [List any sections with placeholders or assumptions]

Next: /docs update after each feature implementation to keep docs current.
```

---

## /docs update — Update after feature implementation

Run after `/implement` or `/commit` when significant code was added or changed.

### Step 1: Determine what changed

- If called right after `/implement`: read the plan file to see what was added
- Otherwise: run `git diff --name-only HEAD~1..HEAD` to see changed files

### Step 2: Update relevant docs

Based on what changed, update the corresponding sections:

| Change type | Update target |
|-------------|--------------|
| New service/controller | `module-index.md` — add row to Services/Controllers table |
| New entity/model | `module-index.md` — add row to Entities; `codebase-summary.md` — add to key entities; `system-architecture.md` — update DB overview |
| New enum/DTO | `module-index.md` — add to Enums section |
| New module/feature added | `codebase-summary.md` — add to module map and feature inventory |
| New pattern established | `code-standards.md` — add to patterns section |
| New integration | `codebase-summary.md` — add to external integrations |
| New env variable | `deployment-guide.md` — add to environment variables |
| Architecture change | `system-architecture.md` — update diagram/flow |

**Rules:**
- Read the existing file before editing — preserve accurate content
- Only update sections affected by the change
- Keep each file within its line limit

### Step 3: Report

```markdown
## Docs Updated

- docs/codebase-summary.md — added [module name] to module map
- docs/code-standards.md   — added [pattern] to patterns section
(or: No docs update needed for this change)
```

---

## /docs summarize — Refresh codebase summary

Quick refresh of `docs/codebase-summary.md` only. Use when docs feel stale.

1. Scan `src/` for modules — compare to current module map in codebase-summary.md
2. Identify new modules not yet documented
3. Update module map, feature inventory, and key entities sections
4. Report: list what was added/updated

---

## Rules

- **Always read existing docs before editing** — don't overwrite accurate content
- **code-standards.md is highest priority** — skills reference it constantly; keep it accurate
- **Don't duplicate stack-rules.md** — docs are project-specific observations, not framework rules
- **Keep files concise** — docs that are too long won't be read or maintained
- **Leave placeholders** rather than guess — `[TODO: fill in deployment steps]` is better than wrong info
- **Use the `docs-manager` agent** for complex doc restructuring tasks
- **Commit docs** on the feature branch alongside the code changes
