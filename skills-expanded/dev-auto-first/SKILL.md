---
name: dev-auto-first
description: |
  Autonomous orchestrator of the per-block go-fast cycle. Takes over after
  arch-first/audit-first when "autopilot" mode is chosen. Runs every block:
  flow-first → library-first → plan-first → execute without manual approvals.
  Validates each skill's artifact against built-in rules. On blockers —
  escalates to a chat bot and waits for a reply.

  Use when: arch-first or audit-first asks "how do we work?" and the user
  chooses autopilot mode; "/dev-auto-first", "autopilot", "run automatically"
---

# Dev-Auto-First Protocol

Autonomous orchestrator of the per-block cycle. Runs instead of manual approval
at each step: flow-first → library-first → plan-first → execute.

**Key principle:** dev-auto-first does not wait for the user's "ok" — it reads
the artifact itself, validates it against the rules, and on success continues
the chain. On blockers — it escalates to a chat bot and waits for a reply.

**How it differs from manual mode:**

| | Manual | dev-auto-first |
|---|---|---|
| flow-first waits for "ok" | User writes "go" | Skill validates artifact → auto-approve |
| library-first waits for "ok" | User writes "go" | Skill validates table → auto-approve |
| plan-first asks for mode | User picks 1/2/3 | Skill answers "1 — Autopilot" |
| Blocker in a skill | User decides | Escalation to chat bot |

**Important:** dev-auto-first is a SKILL, not an agent. Works in the same context,
manages sub-skills via `Skill()` calls.

## Input

Task context (`{slug}`, `{log_dir}`) plus a list of blocks with status `open` or `pending` in the tracking database.

## Output

Per-block auto-approve log lines to chat, artifacts from each sub-skill (flow-first / library-first / plan-first / report / user-note), and a final summary table with block statuses + escalation counts.

## Hands off to

— (terminal). Final task closure is a separate step (`ship-first` invoked manually or from a future auto-closer).

---

## Step 0 — Check task context

Check: are `{slug}` and `{log_dir}` known in the current session?

**If yes** — continue to Step 0.5.

**If no** — list latest task folders under `{tasks_root}/log/`, request user selection, set `{slug}` and `{log_dir}`.

**Cannot skip.** Without `{log_dir}` sub-skill artifacts cannot be read.

---

## Step 0.5 — Load the block list

```bash
sqlite3 {tasks_root}/routing.db \
  "SELECT block_num, title, status FROM task_blocks
   WHERE task_id='{slug}' AND status IN ('open','pending')
   ORDER BY sort_order;"
```

Save as `{pending_blocks}`. If empty — output "No blocks with status open/pending" and finish.

Otherwise show the run plan and start with the first block.

---

## Step 1 — Per-block cycle

For each block from `{pending_blocks}`:

```
1. Skill(flow-first)     → read artifact → validate (4 rules)
2. Skill(library-first)  → read artifact → validate (6 rules)
3. Skill(plan-first)     → read artifact → validate (5 rules) → answer "1"
4. plan-first executes the block in Autopilot mode
5. Mark the block done → move to the next
```

### Auto-approve principle

When a sub-skill outputs "waiting for `ok`" — **do not wait for the user**. Instead:

1. Find the skill's artifact in `{log_dir}` (latest by filename)
2. Read via Read tool
3. Run the corresponding validation rules
4. All 🛑-checks pass → **immediately** call the next Skill()
5. Any 🛑-violation → invoke chat-bot escalation (Step 2)

### plan-first mode selection

When plan-first shows the plan table and asks about the mode —
**immediately answer "1" (Autopilot)** without waiting for the user.

### Logging

After each auto-approve output one line:

```
✅ auto-approve: {skill} block {N} — {X}/{total} checks passed
```

---

## flow-first validation rules

Read `{log_dir}/flow-first-{N}.*.md` (latest by sort).

| # | Check | Criticality |
|---|---|---|
| 1 | All 4 sections present: `## Landscape`, `## Problem`, `## Solution`, `## Result` | 🛑 blocker |
| 2 | No empty table cells — only explicit "not affected" allowed | 🛑 blocker |
| 3 | `## Solution` contains at least one specific action verb (create/add/change/delete/rework) | 🛑 blocker |
| 4 | In `## Solution` at least one cell ≠ "not affected" | 🛑 blocker |

**All 4 pass** → auto-approve → `$library-first`.

---

## library-first validation rules

Read `{log_dir}/library-first-{N}.*.md`.

| # | Check | Criticality |
|---|---|---|
| 1 | All 5 columns filled: What we do / Source / What we use / LOC / Type | 🛑 blocker |
| 2 | Type only from set: `ui` / `backend` / `integration` / `infra` / `ai-skill` / `manual` | 🛑 blocker |
| 3 | LOC — integer or with `~` (not text) | 🛑 blocker |
| 4 | Source = "From scratch ⚠️" → "What we use" contains "no ready-made" | ⚠️ warning |
| 5 | `## Summary` section with "Total new LOC: ~N" | ⚠️ warning |
| 6 | `## Watchpoints` and `## Out of scope` sections present | ⚠️ warning |

**All 🛑 pass** → auto-approve → `$plan-first`.

---

## plan-first validation rules

Read `{log_dir}/plan-first-{N}.*.md`.

| # | Check | Criticality |
|---|---|---|
| 1 | Plan table contains 7 to 15 rows | 🛑 blocker |
| 2 | Right column "Brief summary" — specific text, not empty or "not filled" | 🛑 blocker |
| 3 | `## Risks` block present and filled (or explicit "—") | ⚠️ warning |
| 4 | `## Out of scope` block present and filled (or explicit "—") | ⚠️ warning |
| 5 | No research steps in table ("read X", "check if", "figure out how") | ⚠️ warning |

**All 🛑 pass** → answer "1" (Autopilot) → plan-first executes.

---

## Step 2 — Chat-bot escalation

Real integration via 3 endpoints on `{ops_host}`. The skill lives in the agent, hits the API via `Bash + curl`.

### 2.1 — Send question

```bash
SESSION_ID="${slug}-block-${N}-$(date +%s)"
curl -s -X POST "{ops_host}/api/dev-bot/ask" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"${QUESTION}\",\"session_id\":\"${SESSION_ID}\"}"
```

### 2.2 — Poll for reply

Poll every 4 seconds up to 75 iterations (5 min timeout).

### 2.3 — Parse intent

```bash
curl -s -X POST "{ops_host}/api/dev-bot/parse-intent" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"${IN_TEXT}\"}"
# response: {"intent":"approve|reject|skip|retry|select|other",...}
```

### 2.4 — Intent → action mapping

| Parser intent | Action | What to do |
|---|---|---|
| `approve` | approve_anyway | Ignore violations → continue chain |
| `reject` | stop | Stop → output final report |
| `skip` | skip | Skip block → mark skipped → next block |
| `retry` | retry | Repeat `Skill()` for problematic skill |
| `other` | escalate_v2 | Send clarifying question |

### 2.5 — Fallback on no reply

If no reply within 5 min → default action = `stop`, log fallback note, output interrupted-status final report.

---

## Step 3 — Final report

After finishing all blocks — output summary:

```
✅ dev-auto-first finished.
Task: {slug}

| # | Block | Status | Escalations | Commit |
|---|---|---|---|---|
| 1 | {title} | ✅ Done | 0 | {hash} |
| 2 | {title} | ⚠️ Skipped | 2 | — |

Total: executed {X} of {N} blocks. Escalations: {M}.
```

**After the report — do not call ship-first.** dev-auto-first stops here.
Final task closure is a separate step.

---

## Anti-patterns

### ❌ Waiting for user "ok" like a regular skill

flow-first wrote "waiting for ok" — dev-auto-first stopped and waits for a human.

**Rule:** dev-auto-first reads the artifact immediately without pausing.

### ❌ Skipping validation on auto-approve

dev-auto-first answered "ok" without reading the artifact — "probably fine".

**Rule:** every artifact goes through all validation rules. No exceptions.

### ❌ Calling sub-skills inline instead of via Skill()

dev-auto-first executed flow-first logic from memory instead of `$flow-first`.

**Rule:** always `$flow-first`, `$library-first`, `$plan-first`. Never inline.

### ❌ Closing the task itself

dev-auto-first after the final report called ship-first itself.

**Rule:** dev-auto-first stops after Step 3. ship-first is a separate step.

### ❌ Ignoring ⚠️-warnings entirely

dev-auto-first silently continued without logging warnings.

**Rule:** ⚠️-warnings are logged and appear in the final report.

---

## Related skills

- **flow-first / library-first / plan-first** — sub-skills that dev-auto-first orchestrates
- **arch-first / audit-first** — parent skills that invoke dev-auto-first when user selects autopilot mode
- **ship-first** — separate closure step, NOT called by dev-auto-first

---

## Step 99 — Log invocation

```bash
sqlite3 {tasks_root}/routing.db \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', NULL, 'dev-auto-first', datetime('now'))" 2>/dev/null || true
```
