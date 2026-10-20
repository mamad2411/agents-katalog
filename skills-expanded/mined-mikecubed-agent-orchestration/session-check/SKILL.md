---
name: session-check
description: >
  Session hygiene enforcement. Detects stale or absent session state, exceeded
  failed-hypothesis budgets, and missing codebase briefs before non-trivial
  implementation tasks. Wired into the conductor's write and review operations.
  Renamed from ctx-check in v4.0 to free the "context" namespace for the new
  DDD-strategic context-check (bounded contexts, ubiquitous language).
version: "1.0.0"
last-reviewed: "2026-04-04"
languages: [agnostic]
changelog: "../../CHANGELOG.md"
tools: Read, Bash
model: opus
permissionMode: default
---

# Session Check — Session Hygiene

Language-agnostic. Fires on `write` and `review` operations regardless of language.

---

## Rules

### SESS-1 — Stale or Absent SESSION.md
**Severity**: WARN | **Languages**: all | **Source**: CCC

**What it prohibits**: Starting a non-trivial implementation or review session when
`.agent/SESSION.md` is absent or its `last-updated` frontmatter field is more than
24 hours old, without first confirming intent with the developer.

**Prohibited patterns**:
```text
# Absent session file
.agent/SESSION.md does not exist

# Stale session file
last-updated: "2026-01-01T10:00:00Z"   # > 24h ago, session resumed silently
```

**Exemptions**:
- Single-file bug fixes or tasks explicitly scoped to < 30 minutes of work
- Sessions where the developer has explicitly stated "start fresh"
- Trivial test runs, formatting, or documentation-only edits

**Detection**:
1. Read `.agent/SESSION.md` if it exists; check the `last-updated` frontmatter field
2. If absent: warn once before proceeding
3. If `last-updated` is > 24 hours before the current time: warn and ask the developer
   to confirm the session is intentionally resumed
4. If HANDOFF.json is present and valid, treat it as satisfying the session-state
   requirement even if SESSION.md is absent or stale

**agent_action**:
1. Cite: `SESS-1 (WARN): No active session state found (SESSION.md absent or stale).`
2. Ask: "This looks like a resumed or new session with no recent checkpoint.
   Should I start fresh, or is there context I should know about?"
3. Do not block — wait for developer confirmation, then proceed

---

### SESS-2 — Failed-Hypothesis Budget Exceeded
**Severity**: WARN | **Languages**: all | **Source**: CCC

**What it prohibits**: Continuing implementation or debugging when
`## Failed Hypotheses` in `.agent/SESSION.md` contains 3 or more entries, without
a context-hygiene pause to consolidate state and prune dead ends.

**Prohibited patterns**:
```yaml
# SESSION.md — too many failed hypotheses without a pause
## Failed Hypotheses
- "Caching layer is the bottleneck"
- "Race condition in auth middleware"
- "Database connection pool exhaustion"
# ^ 3 entries: pause required before forming new hypotheses
```

**Exemptions**:
- A context-hygiene pause has already been completed this session
  (`current-phase: "context-hygiene-pause"` was set and cleared)
- HANDOFF.json `failed-hypotheses` array has < 3 entries
- The task is a fresh start with no prior hypotheses

**Detection**:
1. Read `.agent/SESSION.md` `## Failed Hypotheses` section
2. Count distinct hypothesis entries
3. Warn if count ≥ 3 and no prior pause is recorded in `## Decisions`

**agent_action**:
1. Cite: `SESS-2 (WARN): {n} failed hypotheses recorded — context-hygiene pause recommended.`
2. Recommend: "Before forming new hypotheses, write a consolidated summary of what
   is ruled out to `.agent/SESSION.md` and start fresh with only confirmed facts."
3. Do not block — warn and let developer decide

---

### SESS-3 — Missing Codebase Brief for Non-Trivial Implementation
**Severity**: WARN | **Languages**: all | **Source**: CCC

**What it prohibits**: Beginning a non-trivial implementation task (new module,
new service, architectural change) without a recorded codebase brief or scout
discovery summary in the session state or task context.

**Prohibited patterns**:
```text
# Starting "implement new auth service" with:
# - No scout brief
# - No relevant files listed
# - No dependency map
# - SESSION.md Current Task section is empty or generic
```

**Exemptions**:
- The task is a single-file change with clear, bounded scope
- A discovery brief has been passed in the agent prompt directly
- The session's `## Current Context` section references a prior scout run
- The task is a bug fix, not a new feature or structural change

**Detection**:
1. Read `.agent/SESSION.md` `## Current Context` section
2. If the current task involves new modules, new services, or architectural changes
   (infer from task description) AND the context section is empty or lacks file
   references: warn

**agent_action**:
1. Cite: `SESS-3 (WARN): Non-trivial implementation task with no codebase brief recorded.`
2. Recommend: "Run a scout pass first to map relevant files, boundaries, and
   dependencies before implementing. This prevents scope drift and redundant
   exploration mid-task."
3. Do not block — warn and let developer decide

---

Report schema: see `skills/conductor/shared-contracts.md`.
