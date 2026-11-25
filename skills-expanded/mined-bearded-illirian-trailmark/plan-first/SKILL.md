---
name: plan-first
description: |
  Mandatory protocol before any document creation, code writing, refactoring,
  DB migration, test plan, or git operation. Shows a plan table → picks a mode →
  waits for confirmation → executes step by step.

  Use when: before writing/refactoring code, migrating DB, writing tests,
  git commit/PR; "/plan-first", "make a plan first"
---

# Plan-First Protocol

Mandatory protocol before **any** of the following:

- Writing a document (spec, README, guide, architecture)
- Writing new code (file, module, component)
- Refactoring existing code
- Database migration
- Writing tests / test plan
- Git operations (commit, PR, merge)

## Input

The approved `library-first-{N}.{R}.md` with atomic rows the plan will execute.

## Output

A 7-15 row plan table saved as `plan-first-{N}.{R}.md`; after execution — `report-{N}.{R}.md` and `user-note-{N}.{R}.md`.

## Hands off to

`ship-first` — per-block mode closes the block and moves to next; task-level mode closes the task.

---

## Step 0 — Task context

Ensure `{log_dir}` and `{slug}` are known.

---

## Step 1 — Build the plan table

A table of 7–15 rows. Each row = one atomic step.

Columns:
- **#** — sequential number
- **Step title** — verb + object ("create X", "update Y", "delete Z")
- **Short summary** — 1 sentence what this step actually does

Rules:
- 7 to 15 rows — fewer means the block is too small (skip planning), more means it's too big (decompose)
- Right column is a concrete summary, not "TBD" or empty
- No research steps ("read X", "figure out Y") — those belong in flow-first / library-first, not plan-first

---

## Step 2 — Show table + pick mode

Show the plan table to the user. Ask for one of three modes:

```
Mode:
1 — Autopilot: I execute every step without pauses, then a final report
2 — Step-by-step: I pause after each step, wait for "ok" to continue
3 — Draft only: I don't execute, just save the plan for later
```

Wait for the user's response.

Auto-execution context (e.g. `dev-auto-first`): mode = 1 (autopilot) chosen automatically.

---

## Step 3 — Save the artifact

Write `{log_dir}/plan-first-{N}.{R}.md` where:
- `N` = current block number
- `R` = round (1 by default, 2+ on revision)

Structure:

```markdown
> 🔗 Task: tasks/log/{slug}/task.md

# plan-first — plan for block {N}

**Date:** {date}
**Mode:** {chosen mode}

## Plan

| # | Step title | Short summary |
|:-:|---|---|
| 1 | ... | ... |
| ... | ... | ... |

## Risks

- {risk 1}
- ...

## Out of scope

- {what is deliberately not done in this block}
```

Register in `task_artifacts` (`artifact_type = 'plan-first'`, `round_num = R`).

---

## Step 4 — Execute per mode

**Mode 1 (Autopilot):** run each step in order. Report only when done.

**Mode 2 (Step-by-step):** after each step ask "next?". User writes "ok" → continue. User writes anything else → treat as feedback, adjust.

**Mode 3 (Draft only):** stop after saving the plan. Do not execute.

Handle failures per step:
- Non-critical error → log and continue
- Critical error → stop, report, wait for the user

---

## Step 5 — Deploy (default embedded, opt-out only)

Unless the user says "no deploy" or the changes are draft-only:
- Commit the changes with a message referencing the block
- Push to `origin main`
- Sync to sibling projects if the change affects shared skills / commands (`sync-agents.sh`)

Rule: deploy is the default. Only pause for confirmation when the diff touches non-whitelist paths (per CLAUDE.md push policy).

---

## Principles

1. **Every code / doc change goes through plan-first** — otherwise the actual scope drifts silently
2. **7–15 rows** — the sweet spot. Under 7 = block too small, over 15 = decompose the block
3. **Verb + object per step** — makes progress checkable
4. **Explicit out-of-scope** — prevents feature creep during execution
5. **Save the plan even in draft mode** — future you can resume

---

## Anti-patterns

### ❌ Skipping plan-first for "quick" edits
"It's just one line" — until it accidentally breaks three consumers. Plan-first anchors the change.

### ❌ Research steps in the plan table
"Read X to figure out Y" belongs in flow-first / library-first, not plan-first. Plan-first steps are actions, not investigations.

### ❌ Empty "short summary" column
"TBD" or blank means the plan isn't real. Every step must be concretely described.

### ❌ Skipping "Risks" and "Out of scope" sections
Even if you write `—`, mark them explicitly. Silence = these dimensions weren't thought about.

### ❌ Executing before user picks a mode
Wait for mode selection. Even in autopilot orchestration, the mode is picked via automated answer, not silent execution.

### ❌ Inlining instead of `Skill()`
Always via the Skill tool.

---

## Related skills

- **flow-first** — landscape check before planning (Tier 1 cycle)
- **library-first** — reuse audit before planning (Tier 1 and Tier 2 cycles)
- **ship-first** — finalization after execution
