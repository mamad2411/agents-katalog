---
name: dev-backlog
argument-hint: "[orient|plan|work|next|sync] [issue-number]"
description: Manage development work through GitHub Issues + local sprint files. Issues/Milestones are the source of truth; local sprint files handle execution — batching, ordering, context, and progress. Use for creating issues, planning sprints, checking what to work on, reviewing progress, syncing with GitHub, managing milestones, backlog, 다음 작업, 이슈 만들어, 스프린트 계획, 백로그.
compatibility: Requires gh CLI and git. Works on Claude Code and Codex.
metadata:
  related-skills: "backlog-triage, relay, relay-plan, relay-dispatch, relay-review, relay-merge"
---

# Dev Backlog

README covers install and human quick start. This skill file is the execution contract for agents: file roles, sprint structure, process, and script behavior.

Related skill: [`backlog-triage`](../backlog-triage/SKILL.md) for weekly backlog grooming before you plan the next sprint.

Two layers, each with a clear job:

```
GitHub (source of truth — what to do)
  Issues, Milestones, Labels, Comments, PR links
  Defines tasks. Visible to collaborators. Persists across tools.
       ↕  gh CLI (sync is always explicit)
Local (execution hub — how to do it)
  backlog/sprints/   ← THE working file. Plan, context, notes, progress.
  backlog/tasks/     ← Thin mirror of GitHub issues (sync cache).
```

**The sprint file is where you live during execution.** Start every session by reading it. Update it as you work. It carries context across tasks and sessions.

---

## Directory Structure

```
backlog/
├── sprints/              # Sprint execution (the core)
│   ├── _context.md      # Cross-sprint persistent context
│   ├── 2026-03-auth-system.md        # Active (status: active)
│   └── 2026-02-api-v2-migration.md   # Past (status: completed)
├── tasks/                # GitHub issue mirror (thin sync)
│   ├── BACK-42 - OAuth.md
│   └── BACK-43 - Rate-limit.md
├── completed/            # Archived done tasks
└── config.yml            # Project config
```

**Bootstrap (first time):** If `backlog/` doesn't exist, create it: `mkdir -p backlog/{sprints,tasks,completed}`. See `references/file-format.md` for config.yml and task file format. See `references/github-sync.md` for one-time label setup.

### sprints/ Rules

- **One active sprint at a time.** The file with `status: active` is the current sprint.
- **Naming: `YYYY-MM-<topic>.md`** — date prefix for timeline, topic for content.
  - Task-focused: `2026-03-auth-system.md`, `2026-04-payment-integration.md`
  - Time-focused: `2026-03-W13-misc.md`, `2026-03-tech-debt.md`
  - The filename alone should tell you "when and what was worked on."
- **`_context.md`** holds knowledge that outlives any single sprint — architecture decisions, conventions, recurring gotchas. Sprint-specific context stays in the sprint file's Running Context; project-level context goes here.
- **Completed sprints stay.** They're the record of what happened, what was decided, and why. Don't delete them.

---

## Sprint File Format

The sprint file in `backlog/sprints/` is the execution hub. One file per sprint.

```markdown
---
milestone: Sprint W13
status: active
started: 2026-03-22
due: 2026-03-28
---

# Auth + API Foundation

## Goal
One sentence: what's true when this sprint is done.

## Plan
Ordered batches. Small tasks grouped into one session.

### Batch 1 — DB + seed (one session)
- [x] #38 DB schema setup (~15min)
- [x] #39 Seed data script (~10min)

### Batch 2 — Core auth
- [~] #42 OAuth2 flow (~2hr) → PR #87 (reviewing)

### Batch 3 — Hardening (one session)
- [ ] #43 Rate limiting (~30min)
- [ ] #44 Input validation (~20min)

### Batch 4 — Verification
- [ ] #45 Integration tests (~1hr)

## Running Context
Carries across all tasks in this sprint. Add entries as you learn things.
- argon2 for hashing (decided in #42 — GPU resistant, memory-hard)
- rate limit middleware: middleware/rateLimit.ts
- test DB: docker-compose.test.yml
- IMPORTANT: token refresh must use sliding window, not fixed expiry

## Progress
- 2026-03-22 AM: Batch 1 done. Schema + seed in one session.
- 2026-03-22 PM: #42 started. 3/5 AC done. Token refresh logic remaining.
- 2026-03-23 AM: #42 complete. Started Batch 3.
```

### Plan checkbox states

| Marker | Meaning | Set by |
|--------|---------|--------|
| `[ ]` | Not started | sprint-init.js or manual |
| `[~]` | In-flight — dispatched, PR under review | dev-relay (after dispatch) |
| `[x]` | Done — merged or completed | Manual or dev-relay (after merge) |

```
[ ] #42 OAuth2 flow              ← Planning (sprint-init or manual)
 │
 ├─ Do yourself ──→ [x] #42       ← commit "Fixes #42"
 └─ Delegate ─────→ [~] #42 → PR #87 (reviewing)
                     │
                     └──────────→ [x] #42 → PR #87 (merged)
```

### dev-relay data flow

```
backlog/sprints/{active}.md          backlog/tasks/{PREFIX}-{N}.md
┌──────────────────────┐             ┌────────────────────┐
│ ## Plan               │──reads───→ │ AC checkboxes      │──→ relay-plan
│  [ ] / [~] / [x]     │←─writes──  └────────────────────┘
│ ## Running Context    │←─writes──  relay-merge (learnings)
│ ## Progress           │←─writes──  relay-merge (audit log)
└──────────────────────┘
```

### What each section does

| Section | Purpose | When to update |
|---------|---------|---------------|
| **Goal** | Sprint-level success criteria | Once, at planning |
| **Plan** | Ordered batches with issue refs + time estimates | At planning; adjust if scope changes |
| **Running Context** | Decisions, conventions, gotchas that span tasks | During work — whenever you learn something that affects later tasks |
| **Progress** | Timestamped log of what happened | End of each session or batch |

### Cross-Sprint Context (`_context.md`)

Some knowledge outlives a single sprint. When you notice a Running Context entry that's project-level (not sprint-specific), promote it to `backlog/sprints/_context.md`:

```markdown
# Project Context

## Architecture Decisions
- argon2 for all password hashing (2026-03-22, Sprint W13)
- API versioning via URL prefix /v1/ (2026-03-15, Sprint W12)

## Conventions
- All new endpoints need rate limiting middleware
- Test DB via docker-compose.test.yml, never local postgres
- Commit format: Fixes #N or Refs #N

## Known Gotchas
- token refresh must use sliding window (fixed expiry caused logout storms)
- Safari doesn't send cookies on first redirect — workaround in auth middleware
```

At sprint start, read `_context.md` alongside the new sprint file. At sprint end, review Running Context and promote anything that future sprints need to know.

---

## Task Files (thin GitHub mirror)

Files in `backlog/tasks/` are synced copies of GitHub Issues — kept thin on purpose. Their job is to let AI read issue details without an API call.

```yaml
---
id: BACK-42
title: Implement OAuth2 flow
status: In Progress
labels: [auth, backend]
priority: high
milestone: Sprint W13
created_date: '2026-03-22'
---

## Description
[Synced from GitHub issue body]

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] Valid credentials return JWT token
- [x] Expired tokens get 401 response
- [ ] Test coverage > 90%
<!-- AC:END -->
```

Task files get AC checkboxes updated during work. Everything else (notes, decisions, context) goes in the **sprint file**, not here.

---

## Process

**Orient** → Read `_context.md` + active sprint file. No sprint? → Plan. All done? → Complete.

**Work** → Option A (do it yourself): read batch → implement → verify AC → commit `Fixes #N`. Option B (delegate): follow the relay skill's dispatch process.

**Complete** → Check off Plan, add Progress entry. Sprint done? → set `status: completed`, move tasks to `completed/`, promote Running Context to `_context.md`.

Full process details: `references/process.md` (Orient, Create, Plan, Work, Complete, Sync, Quick Fix, Unplanned Work, Next).

---

## References (load on demand)

- `references/file-format.md` — Backlog.md file format, config.yml, task file fields, naming conventions
- `references/github-sync.md` — `gh` CLI patterns: label setup, milestone management, sync commands
- `references/workflow-patterns.md` — Sprint planning, bug triage, feature breakdown, retrospective
- `references/integration-contract.md` — dev-relay ↔ dev-backlog interop surface: file paths, sections, regex patterns
- [`../backlog-triage/SKILL.md`](../backlog-triage/SKILL.md) — sibling skill for weekly backlog review before sprint planning

## Scripts (deterministic, no LLM needed)

All scripts live in `${CLAUDE_SKILL_DIR}/scripts/` (the skill's own directory, not the target project). Run from the target project root.

- `scripts/lib.sh` — Shared bash functions: `find_active_sprint`, `count_checkboxes`, `extract_section`
- `scripts/lib.js` — Shared Node functions: `slugify`, `escapeYaml`, `readConfig`, `estimateSize`
- `scripts/init.sh [project-name]` — Bootstrap `backlog/` directory with config.yml
- `scripts/next.sh` — Show next actionable batch from active sprint (zero LLM cost)
- `scripts/status.sh` — Project status from sprint file + GitHub
- `scripts/sync-pull.js [PREFIX] [--update] [--dry-run] [--json] [--limit N]` — Pull open GitHub issues to local backlog/tasks/. By default it fetches all open issues; `--limit N` caps the fetch size. PREFIX defaults to config.yml's `task_prefix`. `--update` refreshes frontmatter while preserving local AC checkboxes. `--json` emits a machine-readable summary.
- `scripts/sprint-init.js "auth-system" [--milestone "Name"] [--dry-run] [--json]` — Generate sprint file skeleton. `--json` emits the target sprint file path plus metadata.
- `scripts/progress-sync.js [--month YYYY-MM] [--dry-run] [--json] [--relay-manifest PATH] [--finalize]` — Sync the monthly GitHub Progress issue. `--finalize` adds the month-end block and closes the target month's issue idempotently.
- `scripts/sprint-close.sh [backlog-dir] [--dry-run] [--close-milestone]` — Close active sprint: set completed, move tasks, remind about context promotion
- `scripts/context-hook.sh [backlog-dir]` — One-line sprint summary for Claude Code PreToolUse hook (always exits 0)
