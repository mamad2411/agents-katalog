---
description: "Execute an entire sprint end-to-end: plan → implement (with /fleet) → QA → docs → close"
mode: "agent"
---

# Sprint Run

Execute an entire sprint end-to-end using `/fleet` for parallel ticket execution.

Sprint to execute: {{input}}

---

## Phase 1: Sprint Briefing (orchestrator — sequential)

You are the **orchestrator**. Do NOT implement tickets yourself. Your job is to plan, dispatch subagents via `/fleet`, and merge results.

1. Read `specs/backlog.md` — find the target sprint
2. Read ALL relevant spec files referenced by the sprint's tickets
3. Read relevant `docs/` sections for context
4. Build a **dependency-aware execution plan**:
   - Perform a DAG sort on ticket dependencies
   - Group tickets into **batches** — tickets in the same batch have NO mutual dependencies and CAN run in parallel
   - Batches themselves run sequentially (Batch 2 waits for Batch 1)

5. **Present the plan to the user and WAIT for confirmation:**

```
## Sprint X: [Name] — Execution Plan

### Tickets (dependency order)
| # | Ticket | Owner | Dependencies | Batch | Fleet? |
|---|--------|-------|-------------|-------|--------|
| X.1 | Title | Backend | — | 1 | Yes |
| X.2 | Title | Frontend | — | 1 | Yes |
| X.3 | Title | DB | — | 1 | Yes |
| X.4 | Title | Backend | X.1 | 2 | No (single) |
| X.5 | Title | Frontend | X.2 | 2 | Yes |
| X.6 | Title | Frontend | X.2 | 2 | Yes |

### Execution Strategy
- **Batch 1** → `/fleet` (X.1, X.2, X.3 in parallel subagents)
- **Batch 2** → `/fleet` (X.5, X.6 in parallel) + sequential X.4
- **Batch 3** → QA + docs + close (orchestrator)

Shall I proceed?
```

**Do NOT proceed until the user confirms.**

---

## Phase 1.5: Viewer Planning Data (orchestrator — sequential)

After user approves, populate viewer with planning visualizations:
1. Update `viewer/src/data/sprints.ts` with `SprintVisualization` entry
2. Update `viewer/src/data/backlog.ts` if sprint isn't already there
3. Build and verify: `cd viewer && npm run build`

**Skip if:** sprint is < 5 pts or docs-only.

---

## Phase 2: Ticket Execution (subagents via `/fleet`)

Execute each batch using `/fleet` to dispatch parallel subagents.

### For each batch:

**Step 1 — Prepare subagent briefs.** Before dispatching, write a brief for each ticket as a clear, self-contained task description. Each subagent brief MUST include:

```
Subagent task: Implement ticket [X.Y] — [Title]

Context files to read first:
- specs/backlog.md (ticket X.Y details)
- [relevant spec file, e.g. specs/02_backend_lead.md]
- [relevant docs, e.g. docs/viewer/01_architecture.md]

Requirements:
[Copy the ticket description from backlog]

Implementation rules:
- Follow patterns in [spec file]
- Update specs/backlog.md: change ticket X.Y status 🔲 → 🔄 before starting
- Write tests for your changes
- Update specs/backlog.md: change ticket X.Y status 🔄 → 🧪 when done
- Update relevant docs/ section

Files you may modify:
[List the expected files this ticket touches]

Files you must NOT modify (owned by other subagents in this batch):
[List files that other parallel tickets touch — CRITICAL to avoid merge conflicts]
```

**Step 2 — Dispatch with `/fleet`.** Use `/fleet` to run all tickets in the batch as parallel subagents:

```
/fleet Implement these tickets in parallel. Each is independent — no shared files between them:

Subagent 1: [ticket X.1 brief]
Subagent 2: [ticket X.2 brief]
Subagent 3: [ticket X.3 brief]
```

**Step 3 — Monitor with `/tasks`.** Use `/tasks` to check subagent progress. Wait for all subagents in the batch to complete before starting the next batch.

**Step 4 — Verify no conflicts.** After the batch completes, check for file conflicts between subagents. If conflicts exist, resolve them before the next batch.

### Conflict prevention rules

To prevent subagents from stepping on each other:

| Rule | Why |
|------|-----|
| Each subagent gets an explicit list of files it MAY modify | Prevents two agents editing the same file |
| `specs/backlog.md` updates use ONLY the ticket's own row | Multiple agents can update different rows |
| Shared files (e.g. `index.ts` barrel exports) are updated by the orchestrator AFTER the batch | Single writer for shared files |
| If two tickets must touch the same file, put them in the SAME batch but mark as SEQUENTIAL | Avoids merge conflicts |

---

## Phase 3: QA Verification (orchestrator — sequential)

After ALL batches complete, run QA as the orchestrator:

1. Run full test suite:
   ```bash
   npm test
   npm run build
   ```
2. Fix any regressions
3. For bug fixes: verify the original bug is resolved
4. Add new test cases for untested features
5. Re-run until all tests pass

If the sprint has many independent test suites, use `/fleet` to run them in parallel:
```
/fleet Run these test suites in parallel:
- Subagent 1: cd cli && npm test
- Subagent 2: cd viewer && npm run build
```

---

## Phase 4: Documentation Update (orchestrator or `/fleet`)

For each completed ticket, update the relevant `docs/` section.

If docs updates are independent (different files), use `/fleet`:
```
/fleet Update documentation for completed tickets:
- Subagent 1: Update docs/viewer/ for tickets X.1, X.2
- Subagent 2: Update docs/cli/ for tickets X.3, X.4
- Subagent 3: Update docs/methodology/ for ticket X.5
```

If docs updates touch the same files, do them sequentially.

---

## Phase 5: Sprint Close (orchestrator — sequential)

1. Mark all tickets ✅ Done in `specs/backlog.md`
2. Create `sprints/sprint_X/` directory
3. Generate `sprints/sprint_X/summary.md`:

```markdown
# Sprint X Summary

**Date:** YYYY-MM-DD
**Status:** ✅ COMPLETE
**Theme:** [Sprint theme]
**Execution:** /fleet with [N] parallel batches, [M] subagents total

## Overview
[2-3 sentence summary]

## Completed Tickets
| # | Ticket | Description | Status | Batch | Docs |
|---|--------|-------------|--------|-------|------|

## Execution Timeline
| Batch | Tickets | Strategy | Duration |
|-------|---------|----------|----------|
| 1 | X.1, X.2, X.3 | /fleet parallel | — |
| 2 | X.4, X.5 | /fleet parallel | — |
| 3 | QA + docs | orchestrator | — |

## Documentation Updated
| Doc File | Change | Related Tickets |
|----------|--------|-----------------|

## Key Files Modified
[Table of files changed]

## QA & Test Results
| Suite | Pass | Fail | Total | Notes |
|-------|------|------|-------|-------|

## Retrospective
### What went well
### What to improve
### Fleet effectiveness
- Subagent conflicts encountered: [count]
- Parallelization ratio: [X of Y tickets ran in parallel]
```

4. Update sprint status to COMPLETE in backlog

---

## Phase 5b: Viewer Retrospective Data (orchestrator — sequential)

1. Update sprint's `SprintVisualization` in `viewer/src/data/sprints.ts`
2. Update `viewer/src/data/backlog.ts` — match all ticket statuses
3. Build viewer: `cd viewer && npm run build`

**Skip if:** sprint is < 5 pts or docs-only.

---

## Phase 6: Final Report (orchestrator)

Present summary to user:
- Tickets completed vs planned
- Batches executed (how many used `/fleet`)
- Test results
- Docs updated
- Files ready for git commit

---

## Important Rules

- **ALWAYS** get user confirmation after Phase 1 before executing
- **ALWAYS** use `/fleet` for batches with 2+ independent tickets
- **ALWAYS** write subagent briefs with explicit file ownership before dispatching
- **ALWAYS** include "files you must NOT modify" in each brief to prevent conflicts
- **ALWAYS** run QA (Phase 3) before closing (Phase 5)
- **ALWAYS** update docs (Phase 4) before closing (Phase 5)
- **NEVER** let two subagents modify the same file in the same batch
- **NEVER** mark sprint complete with failing tests
- Use `/tasks` to monitor subagent progress between batches
- Shared files (barrel exports, configs, backlog) are updated by the orchestrator only
