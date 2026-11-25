---
name: task-routing
description: >-
  Classify task scope (frontend, backend, fullstack) and
  route to the correct developer(s). Used by the team lead
  for every task before spawning agents.
compatibility: Requires bash, Claude Code
metadata:
  team: fullstack
  role: team-lead
  version: "1.0"
tags:
---

The team lead uses this skill to classify and route every
task to the correct developer(s).

## Scope Classification Procedure

### Step 1: Read Task Spec

Read the task description, any referenced files, and .claude-loop/reports/task-{id}-spec.md
(if it exists from a prior architect pass).

### Step 2: Identify File Signals

| Files / Directories | Scope |
|---------------------|-------|
| `src/components/`, `src/views/`, `src/pages/`, `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.css`, `*.scss` | frontend |
| `src/api/`, `src/routes/`, `src/services/`, `src/models/`, `src/middleware/`, `migrations/`, `*.controller.*`, `*.service.*` | backend |
| `src/lib/`, `src/utils/`, `src/types/`, `src/config/` | shared (check contents) |
| `tests/unit/views/`, `tests/unit/components/`, `*.test.tsx` | frontend tests |
| `tests/unit/api/`, `tests/unit/services/`, `tests/integration/` | backend tests |
| `tests/e2e/` | fullstack tests |

### Step 3: Identify Keyword Signals

| Keywords in Task Description | Scope |
|------------------------------|-------|
| component, view, page, layout, responsive, design token, CSS, WCAG, accessibility, UI | frontend |
| endpoint, API, route, controller, service, model, migration, database, query, auth, middleware | backend |
| feature (that names both UI and API), user flow, integration | fullstack |

### Step 4: Decide

- If ALL signals point to one stack -> route to that stack
- If signals are mixed -> classify as **fullstack**
- If ambiguous -> default to **fullstack** (safer to
  involve both developers than to miss a stack)

### Step 5: Log Decision

Always document the routing decision in SUMMARY.md:

```markdown
## Routing Decision
- **Scope**: frontend | backend | fullstack
- **Routed to**: fe-dev | be-dev | both
- **Signals**: [list of files/keywords that drove the decision]
```

## Common Routing Mistakes

- Routing a "fix API validation" task to fe-dev
- Routing a "add loading spinner" task to be-dev
- Routing a "add user settings" task to only one dev
  when it needs both a settings API and a settings page
- Assuming test tasks don't need routing (they do --
  frontend tests go to fe-dev, backend tests to be-dev)
