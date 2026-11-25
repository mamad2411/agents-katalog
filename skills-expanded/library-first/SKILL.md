---
name: library-first
description: |
  Mandatory protocol before executing any fast-track task.
  Analyzes the task, builds a table: what we do / where it comes from / how many lines of code.
  Principle: maximum reuse of existing libraries and components, minimum new code.
  Waits for explicit user approval — does nothing until confirmed.

  Use when: fast-track task, quick task, before starting implementation
---

# Library-First Protocol

Runs first in a fast-track task. Does nothing until explicit user approval.

## Input

The approved `flow-first-{N}.{R}.md` with Landscape and Solution cells identifying what exists vs what needs building.

## Output

A LOC table with 5 columns (What we do / Source / What we use / LOC / Type) plus Watchpoints and Out-of-scope blocks, saved as `library-first-{N}.{R}.md`.

## Hands off to

`plan-first` (auto-invoked after user approval).

---

## Step 0 — Check task context

Check: are `{log_dir}` and `{slug}` known in the current session?

If yes — continue. If no — list the latest task folders under `{tasks_root}/log/` and ask which is current, then set `{slug}` and `{log_dir}`. Cannot skip — without `{log_dir}` the artifact won't be saved.

---

## Step 0.5 — Chain verification

If `{N}` is known — check for a flow-first artifact:

```bash
ls "{log_dir}"/flow-first-{N}.*.md 2>/dev/null | head -1
```

File found → continue. Not found → invoke `Skill(flow-first)` and resume after it completes. `{N}` unknown → silently skip.

### Step 0.5.1 — Read and extract Solution

From the flow-first file extract: **Landscape / Problem / Solution / Result** across three axes (UI / DB / Integrations).

Use **Solution** as the basis for atoms in Step 1. Use **Landscape** for the "Source" field: existing component mentioned → `Library ✅`; not mentioned → `From scratch ⚠️`.

If the flow-first table is empty or all cells say "not involved" — prompt once to repeat flow-first; on retry, continue with what's there.

---

## Step 1 — Task analysis

Break the task into atomic parts. For each part determine:
- **Source:** existing component/library → `Library ✅`; nothing suitable → `From scratch ⚠️`
- **What we use:** specific file/component name. If from scratch — "no ready-made"
- **LOC:** approximate new lines. Library — 0 or minimum for integration

---

## Step 2 — Output the table

```
| # | What we do        | Source          | What we use     | LOC | Type     |
|---|-------------------|-----------------|-----------------|-----|----------|
| 1 | [action]          | Library ✅       | [file]          | 0   | ui       |
| 2 | [action]          | From scratch ⚠️  | no ready-made   | ~40 | ai-skill |

Total new lines of code: ~40
```

**Row types:** `ui` / `backend` / `integration` / `infra` / `ai-skill` / `manual`.

**Atomicity rule:** 1 row = 1 type. If an action touches two types — split into two rows.

After the table — two mandatory blocks:

### Watchpoints

Each item contains a specific `file:line` or fact from the code. Abstract risks forbidden. No risks → write `—`. If there's a 🛑 blocker — stop and ask before executing.

### Out of scope

Three sources: (1) what's not in the task description, (2) adjacent files intentionally untouched, (3) `Library ✅` rows left as-is. Nothing → write `—`. Empty and missing block both forbidden.

---

After the blocks:

```
library-first complete. LOC table ready. Waiting for "ok" → launching plan-first.
```

---

## Step 2.5 — Save table to log

**1. Round number:**

```bash
R=$(( $(ls "{log_dir}"/library-first-{N}.*.md 2>/dev/null | wc -l) + 1 ))
```

**2. Write** `{log_dir}/library-first-{N}.{R}.md` via Write tool. Contents: task reference, full table, `## Summary` (row counts + total LOC + unique types), `## Watchpoints`, `## Out of scope`.

**3. Register** the artifact in `task_artifacts` with `artifact_type='library-first'`.

**4. Append row** to `## Task files` in `task.md` via Edit tool.

Output on success:

```
✅ Artifact: library-first-{N}.{R}.md → created ✅ registered ✅
```

---

## Step 3 — Wait for approval

Do not execute anything until explicit response.

| Response | Action |
|---|---|
| "ok" / "go" / "yes, relevant" | Hand control to `plan-first` |
| Row edit | Update row → show updated table → wait again |
| Task too complex / too many LOC | Escalate to Brief (Step 4) |

**"Too complex" criterion:** total LOC > 150 or more than 3 "From scratch ⚠️" rows.

---

## Step 3.5 — Decision on run_ui_ai_first

After approval — evaluate by row types:

| Condition | run_ui_ai_first |
|---|---|
| At least one `ui` row | `true` — always |
| All rows `ai-skill` and/or `manual` | `false` — always |
| `backend`/`integration`/`infra` + no `ui` | `false` only if all `Library ✅` AND markers `fix`/`bug`/`repair` |
| Mixed without `ui` and without `ai-skill`/`manual` | `false` only if all `Library ✅` AND fix markers |

In all other cases — `true`. Set the flag in session context; `ship-first` reads it later.

---

## Step 4 — Escalate to Brief

If the user escalates: create a brief draft with status `draft`, archive the fast-track task, link as `escalated_into`, stop — do not proceed to `plan-first`.

---

## Rules

- Never start execution before explicit table approval
- Always look for existing components before writing new code
- LOC is an approximate estimate — better slightly overestimate than underestimate
- One-line task still gets a one-row table

---

## Anti-patterns

### ❌ Hallucinating risks without file:line

Wrote `⚠️ There might be an authorization problem` with no file, line, or fact. Every "Watchpoints" item must contain a specific `file:line` or explicit fact from analysis.

### ❌ Skipping "Out of scope" without an explicit "—"

Skipped because "obvious". The user doesn't know that an adjacent file is intentionally untouched. Always required. Nothing → write `—`.

### ❌ Not setting run_ui_ai_first flag when criteria are met

Task creates a new endpoint but flag isn't set — ship-first skips ui-ai-first, new code left without UX check. If at least one row is `From scratch ⚠️` — flag `true` by default.

### ❌ Inlining the skill instead of using the Skill() tool

Executed the protocol manually from memory — outdated version, no accuracy guarantee. Always launch via `$library-first`.

---

## Related skills

- **flow-first** — captures landscape / problem / solution / result upstream
- **plan-first** — receives control after approval, plans concrete steps
- **ship-first** — reads `run_ui_ai_first` flag at end of block

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'library-first', datetime('now'))" 2>/dev/null || true
```
