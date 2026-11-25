---
name: check-first
description: |
  Coverage validation protocol before a final approval gate.
  Reads requirements from any structured requirements document, matches
  them against the proposed decomposition units (blocks, epics, tasks),
  outputs a coverage table. If gaps exist — stops, waits for user
  decision. If everything is covered — continues without pause.

  Use when: after proposing any decomposition of work (blocks / epics /
  tasks) before committing to execution — as a safety net that no
  requirement fell through the cracks.
---

# Check-First Protocol

Runs after a decomposition step in any workflow (e.g. after proposing
epics for a brief, or blocks for a specification). Verifies that every
requirement from the source document is covered by at least one
proposed unit.

---

## Step 1 — Extract requirements

From the already-read requirements document (brief, specification,
technical description, product doc) extract every requirement. Look in
sections like:

- Scope / What's included
- Acceptance criteria
- What must exist
- Functional requirements
- Non-functional requirements

Each requirement is one row. Don't duplicate near-identical items —
merge them if the essence is the same.

---

## Step 2 — Output a coverage table

```
Requirements coverage check:

┌─────┬────────────────────────────────────┬──────────────┬────────────┐
│  #  │ Requirement                        │ Unit         │ Status     │
├─────┼────────────────────────────────────┼──────────────┼────────────┤
│ 1   │ [requirement from source doc]      │ Unit N       │ ✅ Covered │
│ 2   │ [requirement from source doc]      │ Unit N       │ ✅ Covered │
│ 3   │ [requirement from source doc]      │ —            │ ⚠️ Gap     │
└─────┴────────────────────────────────────┴──────────────┴────────────┘
```

"Unit" = the smallest labelled thing in your decomposition: an epic, a
block, a task — whatever the current workflow produces.

---

## Step 3 — Decision

**If every row is ✅:**

```
✅ All requirements covered — continuing.
```

Proceed without pause.

**If there are ⚠️ gaps:**

```
⚠️ N gap(s) found. Options:
1. Add to an existing unit [Unit X]
2. Create a new unit
3. Move to backlog — not part of this cycle
```

Wait for user decision per gap. After decisions land — update the unit
list and continue.

---

## Rules

- Don't skip even when the decomposition looks obviously complete
- On gaps — don't proceed without a user decision
- Extract requirements from the source text, don't invent them
- The point of the protocol is a paper trail: even a "no gaps" result
  is a first-class artifact — future readers see what was checked

---

## Anti-patterns

### ❌ Skipping when decomposition looks obvious

The decomposition seems to fully cover the requirements — skip the
check. Later a requirement surfaces in production, and nobody can
reconstruct whether it was considered or missed.

**Rule:** always run coverage check, even for "obvious" decomposition.
Even a "no gaps" result is a first-class artifact.

### ❌ Inventing requirements

The agent invents a requirement to make unit N fit — user approves.
The actual source document never contained that requirement, and the
decomposition now includes phantom work.

**Rule:** extract from source text only. If a unit doesn't map to any
extracted requirement, that's a signal the unit itself is scope creep,
not that a requirement is "implicit".

### ❌ Silent gap dismissal

Agent finds a gap → decides «it's minor, skip» → doesn't surface to
user. Later the gap becomes a bug or missed feature, and there's no
record of the decision to skip.

**Rule:** every gap requires an explicit user decision (add / new unit
/ backlog). Never dismiss silently. Recording "we chose to defer this"
is itself the audit trail.

### ❌ Inlining instead of Skill()

The agent read the protocol from memory and executed it inline — no
coverage-table artifact, no logged decision, no paper trail.

**Rule:** always launch via `$check-first` tool. The whole
value of the protocol is the artifact it produces.

---

## Related skills

- **plan-first** — invokes check-first after outputting the plan
  decomposition table, before executing
- **arch-first** — decomposition source for larger multi-block tasks;
  check-first validates coverage against the original brief/spec
- **ship-first** — closes work; check-first ensures nothing missed
  before the block or task is marked done

---

## Step 99 — Log invocation

Before exiting, log this skill invocation to routing.db:

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'check-first', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true` keeps a logging failure from aborting the skill.
