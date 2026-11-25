---
name: vault-maintainer
description: |
  PARA maintenance knowledge — batch discipline, CI-001 loop, inbox lifecycle, archive patterns.
  Load for vault maintenance capability without role enforcement.
  Keywords: PARA, maintenance, inbox lifecycle, CI-001, batch, archive, housekeeping, frontmatter,
  vault hygiene, scan, triage, dispatch, completion gate, NDP-001
triggers:
  - vault maintenance
  - CI-001 loop
  - inbox lifecycle
  - batch maintenance
  - archive vault items
  - housekeeping cycle
  - PARA hygiene
  - frontmatter maintenance
  - scan vault
  - triage inbox
negative_triggers:
  - create a note
  - apply template
  - dataview query
  - frontmatter schema definition
  - git operations
  - plugin development
version: 3.7.0
author: Christian Kusmanow / Claude
last_updated: 2026-06-17
---

# Vault Maintainer

PARA maintenance knowledge for the Teslasoft Obsidian vault. Encapsulates batch discipline, inbox item lifecycle, CI-001 loop capabilities, and archive patterns.

## When to Use

- Performing batch vault maintenance (frontmatter fixes, status updates, archival)
- Running a CI-001 housekeeping cycle (scan, propose, execute, report)
- Managing inbox item lifecycle (create through archive)
- Applying NDP-001 archive decision matrix
- Triaging and dispatching work items

## When NOT to Use

- Looking up PARA frontmatter schemas (use `vault-metadata`)
- Creating individual vault notes (use `vault-notes`)
- Applying templates (use `vault-templates`)
- Session bootstrapping (use `vault-boot`)

---

## PARA Schema Reference

Canonical schemas live in the `vault-metadata` skill. Load it for full definitions, validation rules, and migration patterns.

Quick reference for maintenance decisions:

| Type | Required Fields | Status Values |
|------|----------------|---------------|
| inbox | type, status, project, priority, phase | active, dispatched, review, done, blocked |
| project | type, status, goal, priority | active, paused, complete |
| goal | type, status, timeframe | active, achieved, deferred |
| area | type, status | active, archived |
| resource | type, status | active, archived |
| spec | type, status, project, version | draft, review, approved |

**Canonical type values:** `inbox`, `project`, `goal`, `area`, `resource`, `spec`, `collab`, `science`, `skill`

**Important:** `type: resource` is canonical (never `ressource`). `assigned_role` is canonical (never `role`). `phase` must be a string value: `collect`, `analyze`, `implement`, `verify`, `integrate`.

### Wikilink Fields — Format Rules (CRITICAL)

The `project` and `goal` fields use wikilink format. Getting this wrong breaks Dataview, lifecycle panels, and para-indexer relationship chains.

#### `project` field — all PARA types

```yaml
project: "[[P60-Cowork-Plugin-Rewrite]]"   # CORRECT
project: P60-Cowork-Plugin-Rewrite           # WRONG — plain string
project: [[P60-Cowork-Plugin-Rewrite]]       # WRONG — unquoted
```

#### `goal` field — project notes only

```yaml
# CORRECT — single goal (quoted wikilink string)
goal: "[[G-2026-Q1 Teslasoft Portfolio fertigstellen]]"

# CORRECT — multiple goals (YAML block sequence)
goal:
  - "[[G-2026-Q1 Teslasoft Portfolio fertigstellen]]"
  - "[[G-2026-Q1 FixIt Aachen Mockup vorbereiten]]"

# WRONG — inline bracket array, breaks Dataview queries
goal: ["[[G-2026-Q1 Teslasoft Portfolio fertigstellen]]"]

# WRONG — unquoted wikilink
goal: [[G-2026-Q1 Teslasoft Portfolio fertigstellen]]
```

For a single goal use a quoted wikilink string. For multiple goals use YAML block sequence (one entry per line with `  - `). Never use inline bracket array `[...]` syntax.

**The linter may fix working-tree copies AFTER staging.** Always verify staged content with `git diff --cached` before committing — the staged version is what goes into git, not the working-tree copy.

---

## Batch-First Discipline

All vault maintenance operations follow a deterministic batch pipeline. Never process items one-by-one.

### Pipeline Phases

```
scan --> classify --> batch-prepare --> batch-execute --> verify
```

1. **Scan** — Collect all items requiring attention. Use MCP tools (`inbox_list`, `vault_list`, `vault_query`) or Jarvis state data.
2. **Classify** — Group items by operation type (frontmatter fix, status update, archival, creation). Assign risk level (low/medium/high).
3. **Batch-prepare** — Plan all changes before executing any. For each batch:
   - List affected files
   - Describe the change per file
   - Identify dependencies between changes
   - Estimate blast radius
4. **Batch-execute** — Apply all changes in the batch. Group related changes into single atomic commits.
5. **Verify** — Confirm all changes applied correctly. Check frontmatter validity, link integrity, and status consistency.

### Batch Commit Rules

- One atomic commit per logical batch (not per file)
- COM-001 attribution tag required: `[ai:vault-maintainer@{branch}]`
- Never mix PARA content changes with infrastructure changes in the same commit
- Always run `verification-before-completion` skill before committing

---

## Inbox Item Lifecycle Protocol (CI-001 Gates)

Every inbox item follows this lifecycle. Each transition has a quality gate.

### Lifecycle States

```
create --> triage --> dispatch --> execute --> review --> complete --> archive
```

### State Transitions

| From | To | Gate | Who |
|------|----|------|-----|
| (new) | **create** | Must have `project` field, valid frontmatter per vault-metadata | vault-maintainer, inbox-author |
| create | **triage** | Assign priority, execution_mode, phase, assigned_role | orchestrator |
| triage | **dispatch** | status -> `dispatched`, assign to session/worktree | orchestrator |
| dispatch | **execute** | Agent works, records commit IDs in progress log | assigned agent |
| execute | **review** | Quality gate check: commit present, tests recorded, gate result per phase | orchestrator, reviewer |
| review | **complete** | status -> `done`, all quality gates pass | orchestrator |
| complete | **archive** | Move to `90_Archive/` via archive skill or INTEGRATE phase | vault-maintainer (with archive skill) |

### Quality Gate Checklist (per phase)

Each phase in an inbox item's CI-001 structure must record:

- [ ] Commit hash (the specific commit delivering this phase)
- [ ] Test count or "N/A" with justification
- [ ] Gate result: `PASS`, `FAIL`, or `BLOCK`
- [ ] Date of completion

### Progress Log Format

Every inbox item must maintain a Progress Log table:

```markdown
| Phase | Status | Commit | Tests | Date |
|-------|--------|--------|-------|------|
| 1. ANALYZE | done | abc1234 | N/A | 2026-03-28 |
| 2. IMPLEMENT | in-progress | --- | --- | --- |
```

---

## CI-001 Loop Capabilities

The 7-step housekeeping cycle for automated vault hygiene. Previously owned by the housekeeper role, now absorbed into vault-maintainer.

### Prerequisites

1. Drone sidecar running (`pnpm health`)
2. `coordination/jarvis/state.json` contains a `housekeeping` section
3. `00_Inbox/housekeeping/` directory exists

### The 7-Step Cycle

Execute sequentially. Each step completes before the next begins.

#### Step 1: Scan

Read `coordination/jarvis/state.json`, extract `housekeeping` section. Group items by risk level:

- **Low risk** (auto-resolvable) — proceed to Step 2
- **Medium/High risk** — proceed to Step 3

If `housekeeping` section is missing, trigger collection via Jarvis (`jarvis_collect` MCP tool or `POST /jarvis/collect`). Wait, retry once. If still missing, exit cycle with error log.

#### Step 2: Auto-Execute (Low Risk)

Execute items where `auto_resolvable: true` and `risk_level: low`.

| Category | Action | Verification |
|----------|--------|--------------|
| `vop002_drift` | Diff package.json scripts against VAULT.md. Add missing, remove stale. | Re-read both files, confirm parity. |
| `thread_archival` | Move done threads from harness-control.md to archive. | Confirm removed from active table. |
| `alert_stale` | Resolve alerts older than 24h via Jarvis API. | Confirm alert count decreased. |
| `resolved_proposal` | Archive resolved/executed/deferred proposals. | Confirm removed from inbox. |

After each auto-execution, verify the result. If verification fails, log and continue.

#### Step 3: Propose (Medium/High Risk)

Create proposal notes at `00_Inbox/housekeeping/HK-{YYYY-MM-DD}-{NNN}.md` for items requiring human review.

| Category | Risk | Strategies |
|----------|------|------------|
| `learned_rule` | medium | apply, defer (30 days), modify |
| `hook_fix` | high | apply (worktree), defer, modify |
| `policy_change` | high | apply, defer (30 days), modify |
| `drone_code` | high | apply (worktree + tests), defer, modify |

#### Step 4: Check Approvals

Scan `00_Inbox/housekeeping/*.md` for proposals with `review_status: approved` and `strategy` set.

#### Step 5: Execute Approved

- **apply (low/medium):** Execute directly, verify, update proposal to `executed`
- **apply (high risk):** Use worktree at `.worktrees/housekeeping`, branch `housekeeping/{id}`, do NOT auto-merge
- **defer:** Set `deferred_until` (+30 days), resolve related Jarvis alert
- **modify:** Read user comments, adapt approach, proceed as apply or mark `needs-attention`

#### Step 6: Report

1. Update executed proposals: `review_status: executed`
2. Resolve related Jarvis alerts
3. Emit `HOUSEKEEPING_CYCLE_COMPLETE` telemetry event
4. Print summary table

#### Step 7: Purge

Archive resolved proposals and old reports from `00_Inbox/housekeeping/` to `90_Archive/00_Inbox/housekeeping/`. Use archive skill. Follow NDP-001.

### After Cycle: Commit

Single atomic commit per cycle:
```
[ai:vault-maintainer@{branch}] chore: housekeeping cycle -- {summary}
```

---

## Archive Patterns

All archive operations follow the NDP-001 Archive Decision Matrix.

### Decision Matrix (Quick Reference)

| Category | Action | Examples |
|----------|--------|---------|
| **Always archive** | Move to 90_Archive/ | Completed projects, goals, historical decisions, user-created content |
| **Summarize then delete** | Add "Superseded by" link, then delete | Superseded project files, processed inbox items, replaced drafts |
| **Delete without archive** | Delete directly | Test/scratch files, generated artifacts, duplicates, WIP drafts, lifecycle files |
| **Never delete** | Leave in place | Active projects, policy files, config files, user data |

### MCP Tools for Archive Operations

- `inbox_archive` — single item archive
- `inbox_archive_batch` — batch archive (preferred for multiple items)

### Archive Conventions

- Preserve directory structure under `90_Archive/`
- Add `archived_from: {original_path}` to frontmatter when archiving
- For bulk operations: stage specific files (never `git add -A`), max 5 deletions per commit without explicit approval
- Archive operations require the `archive` skill loaded OR explicit INTEGRATE phase authorization (LR-ARC-005)

---

## Domain-Scoped Guidance

### PARA_DOMAIN: governance

The vault-maintainer operates in governance mode. This means:

- Frontmatter guidance is scoped to PARA governance (type correctness, status consistency, link integrity)
- Operations are limited to PARA note paths (00-90 directories, coordination specs/policies, .claude/roles and agents)
- Submodule code editing is forbidden (`submodule_code_edit: forbidden`)

### PARA Note Operations

| Operation | Method | Gate |
|-----------|--------|------|
| Create | `inbox_create` MCP or Write tool | Must have `project` field if project-scoped (LR-INB-001) |
| Update status | `vault_frontmatter` MCP or Edit tool | Verify no downstream query breakage |
| Update frontmatter | `vault_frontmatter` MCP or Edit tool | Must match vault-metadata schema |
| Move | Bash mv + update internal links | Verify all wikilinks still resolve |
| Archive | `inbox_archive` MCP or archive skill | NDP-001 matrix check |

### Wikilink Conventions

- **Filename-only wikilinks** with uniqueness check — never path-qualified unless basename is ambiguous
- No `[ARCHIVED]` suffix in wikilinks
- After rename/move: verify all incoming links still resolve

### Completion Gate Checklist

Before committing any vault maintenance batch:

- [ ] All modified frontmatter is valid per vault-metadata schema
- [ ] No submodule paths appear in the git diff
- [ ] `verification-before-completion` skill has been run
- [ ] Wikilinks in modified files resolve correctly
- [ ] Progress Log updated in affected inbox items
