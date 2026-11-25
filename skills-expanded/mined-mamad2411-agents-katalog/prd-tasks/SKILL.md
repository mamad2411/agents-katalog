---
name: prd-tasks
description: 'Generate task files from an existing PRD. Use when a PRD is approved and ready for implementation, when you need to break a PRD into trackable tasks, or when asked to create tasks from a PRD. Triggers on: create tasks from prd, generate tasks, break down prd, task breakdown.'
user-invocable: true
---

# PRD Task Generator — MGM-Web

Read an existing PRD from `docs/prd/` and generate individual task files in `docs/tasks/XX/`, one per User Story.

---

## The Job

1. **Identify the PRD**: User provides PRD number or file path. If not provided, read `docs/prd/INDEX.md` to list available PRDs.
2. **Read the PRD**: Parse `docs/prd/XX_feature-name.md`
3. **Pre-research**: Verify real schemas, hooks, and prior context (see Step 0 below)
4. **Extract User Stories**: Each `US-XXX` becomes one task file
5. **Create task folder**: `docs/tasks/XX/` (matching the PRD number)
6. **Generate task files**: One `.md` per User Story
7. **Update INDEX.md**: Set PRD status to "Em andamento", add detail section with US table

**Important:** Do NOT start implementing. Just create the task files.

---

## Step 0: Pre-Research (Before Generating Tasks)

Before writing any task file, **verify real data** from the codebase:

1. **Check `database.types.ts`**: Verify real column names for tables mentioned in the PRD — Supabase columns may use unexpected naming (hyphens like `"uazapi-host"`, camelCase, or snake_case)
   ```
   Grep for the table name in src/lib/supabase/database.types.ts
   ```
2. **Check existing hooks**: Look for hooks that already reference API routes — some may call endpoints that don't exist yet (ghost references). Document these in the task so the implementer knows.
   ```
   Grep for the API path in src/hooks/ to find client-side consumers
   ```
3. **Check existing routes**: Verify which routes exist vs. need to be created
   ```
   Glob for src/app/api/{domain}/**/route.ts
   ```
4. **Check `.claude/tasks/`**: Search for related session context files that may have prior investigation on the feature
   ```
   Grep for the feature keyword in .claude/tasks/context_session_*.md
   ```
5. **Check folder-specific CLAUDE.md**: Read the relevant `CLAUDE.md` files for folders being modified (e.g., `src/app/api/CLAUDE.md`, `src/lib/services/CLAUDE.md`)

This pre-research prevents writing tasks with wrong field names, missing context, or referencing non-existent code.

---

## Task File Format

Each task file follows this structure:

**Filename:** `docs/tasks/XX/US-NNN_title-kebab-case.md`

```markdown
# US-NNN: Title

> **PRD**: `docs/prd/XX_feature-name.md`
> **Task**: `docs/tasks/XX/US-NNN_title-kebab-case.md`
> **Status**: Pendente

## Description

As a [role], I want [feature] so that [benefit].

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] `npm run fix` passes (lint + typecheck)
- [ ] **[If UI]** Verify in browser at localhost:3003
- [ ] **[If Supabase]** Migration created and RLS policies defined
- [ ] **[If permissions]** OrgContext permission checks added

## Implementation Notes

### Files to modify/create

- `src/components/...` — description
- `src/hooks/...` — description
- `src/app/api/...` — description
- `src/lib/types.ts` — description

### Código atual (referência)

Include relevant code snippets from the current codebase so the implementer
knows the exact function signatures, variable names, and patterns to follow.
This avoids the need to read files before starting.

### Key patterns to follow

- Auth via `getOrgContextFromCookies()` (if API route)
- Filter by `group_owner = org.organizationRootUserId` (if querying groups)
- Types: Zod schema in `src/lib/types.ts`, infer with `z.infer<>`
- Query key: `["domain", ...params]` (TanStack Query convention)
- Import hooks from `@/hooks` barrel file
- Follow `src/app/api/CLAUDE.md` for API route patterns (requestId, logging)

### Dependencies

- Depends on: US-NNN (if applicable)
- Blocks: US-NNN (if applicable)

## Testing

- [ ] Manual test: description
- [ ] Verify in browser at localhost:3003
```

---

## Rules

### Ordering and Dependencies

- Extract dependency order from the PRD's Functional Requirements
- Schema/migrations first, then types, then API routes, then hooks, then UI
- Mark dependencies explicitly in each task file

### Implementation Notes

For each task, analyze the PRD's Architecture Considerations and add:

- **Specific file paths** to modify or create
- **Which existing hooks/components** to extend
- **Supabase changes** needed (migrations, RLS, triggers)
- **Permission checks** if applicable (`canManageUsers`, `canCreateGroups`, `canViewAllGroups` via `getOrgContextFromCookies()`)
- **TanStack Query keys** to use or invalidate
- **Zod schemas** to add in `src/lib/types.ts`

This is what makes the tasks actionable — a developer or AI agent should know exactly where to start.

### Task Sizing

Each task must fit in **one context window** without compression. Guidelines:

- **Max 3 files** to modify/create per task
- **~80 lines** of new code per task
- If a task touches both API route + hook + UI component, it's too big — split it

If a User Story is too large, split it:

```
# Original US-003 is too big → split into:
docs/tasks/02/US-003a_health-score-api.md
docs/tasks/02/US-003b_health-score-ui.md
```

Use letter suffixes (a, b, c) to keep the numbering aligned with the PRD.

### Include Real Schemas

When a task involves Supabase tables, **include the actual Row type** from `database.types.ts` in the task file. This prevents the implementer from guessing field names.

Example:
```typescript
// From database.types.ts — instances table (note: hyphens, not underscores!)
Row: {
  "uazapi-host": string | null
  "uazapi-instanceToken": string | null
  instance: string | null
}
```

### Flag Ghost References

If pre-research reveals a hook calling an API route that doesn't exist yet, **document it explicitly** in the task:

```markdown
### ⚠️ Ghost reference
The hook `useDeleteGroups` in `src/hooks/useGroups.ts` (line ~319) already calls
`POST /api/groups/delete`, but this route does not exist yet. This task creates it.
```

This prevents confusion when the implementer sees client-side code referencing the route.

---

## INDEX.md Update

After generating tasks, update `docs/prd/INDEX.md`:

1. **Change PRD status** from "Draft" or "Aprovado" to "Em andamento"
2. **Update progress**: "0/N US"
3. **Add detail section** below the table:

```markdown
---

## PRD XX: Feature Name

| US     | Título         | Status   | Branch/PR |
| ------ | -------------- | -------- | --------- |
| US-001 | Title from PRD | Pendente | —         |
| US-002 | Title from PRD | Pendente | —         |
| US-003 | Title from PRD | Pendente | —         |
```

---

## Example

Given `docs/prd/02_group-health-score.md` with 2 User Stories:

**Creates:**

```
docs/tasks/02/
├── US-001_display-health-score.md
└── US-002_sort-by-health-score.md
```

**US-001 file content:**

```markdown
# US-001: Display health score on group card

> **PRD**: `docs/prd/02_group-health-score.md`
> **Task**: `docs/tasks/02/US-001_display-health-score.md`
> **Status**: Pendente

## Description

As an owner, I want to see a health score on each group card so I can quickly identify which groups need attention.

## Acceptance Criteria

- [ ] Health score (0-100) displayed on GroupCard component
- [ ] Color coding: green (70-100), yellow (40-69), red (0-39)
- [ ] Trend indicator arrow (up/down/stable) based on 7-day comparison
- [ ] Score calculated from `statistics_daily` table (NOT `interactions`)
- [ ] API route returns score via `/api/groups` response
- [ ] `npm run fix` passes (lint + typecheck)
- [ ] Verify in browser at localhost:3003

## Implementation Notes

### Files to modify/create

- `src/lib/analytics/health-score.ts` — new utility with `calculateHealthScore()` function
- `src/lib/types.ts` — add `HealthScoreSchema` Zod schema with score (number), trend (enum)
- `src/app/api/groups/route.ts` — extend GET response to include health score per group
- `src/components/groups/GroupCard.tsx` — add score badge with color coding
- `src/hooks/useGroups.ts` — update return type to include healthScore field
- `src/hooks/index.ts` — ensure barrel export is updated if new hooks added

### Key patterns to follow

- Use `statistics_daily` table (NOT `interactions` — 3.6M+ rows, too slow)
- Filter by `group_owner = org.organizationRootUserId`
- Auth via `getOrgContextFromCookies()`
- Types: Zod schema in `src/lib/types.ts`, infer with `z.infer<>`
- Query key: `["groups", ...]` (follows existing convention)

### Dependencies

- Depends on: none (first task)
- Blocks: US-002 (sort requires score data to exist)

## Testing

- [ ] Manual: Load home page → verify each group card shows health score
- [ ] Manual: Verify color coding matches expected ranges
- [ ] Manual: Compare score trend with actual 7-day data
- [ ] Manual: Verify score not shown for groups with insufficient data
```

**INDEX.md updated:**

```markdown
| 02 | [Group Health Score](02_group-health-score.md) | #42 | Em andamento | 0/2 US |
```

---

## Updating Task Status

When working on implementation, update task files:

1. **Starting a task**: Change status to `Em andamento` in task file header and INDEX.md detail
2. **Completing a task**: Check all acceptance criteria boxes, change status to `Concluída`, update INDEX.md progress
3. **All tasks done**: Update INDEX.md PRD status to "Concluído", remove detail section

---

## Context Systems

This project has **two separate context systems** — do not confuse them:

| System | Location | Purpose |
|--------|----------|---------|
| **Session context** | `.claude/tasks/context_session_X_description.md` | Developer diary — what was investigated, decided, tried |
| **PRD tasks** | `docs/tasks/XX/US-NNN_title.md` | Implementation tasks from PRDs |

**Cross-reference rule**: When generating tasks, check `.claude/tasks/` for prior session context about the feature. If found, reference it in the task's Implementation Notes so the implementer has background context.

---

## Checklist

Before finishing task generation:

- [ ] Read the PRD completely
- [ ] **Pre-research**: Verified `database.types.ts` column names for tables involved
- [ ] **Pre-research**: Checked hooks for ghost references (calls to non-existent routes)
- [ ] **Pre-research**: Checked `.claude/tasks/` for prior session context
- [ ] **Pre-research**: Read folder-specific CLAUDE.md for affected directories
- [ ] Created `docs/tasks/XX/` folder
- [ ] One task file per User Story (with letter splits if needed)
- [ ] Each task has max 3 files, ~80 lines new code (fits in one context window)
- [ ] Each task has implementation notes with specific file paths
- [ ] Each task includes "Código atual (referência)" with relevant code snippets
- [ ] Each task includes "Key patterns to follow" section
- [ ] Real DB schemas included for tasks involving Supabase tables
- [ ] Ghost references flagged where hooks call non-existent routes
- [ ] Acceptance criteria use `npm run fix` (NOT separate lint/build)
- [ ] Dependencies marked between tasks
- [ ] Testing section with manual test steps
- [ ] Updated `docs/prd/INDEX.md` with status and detail section
