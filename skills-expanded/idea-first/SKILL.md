---
name: idea-first
description: |
  Entry point of the self-organizing skill chain. Launched right
  after task creation. Asks 5-7 questions, determines task type
  (product / feature / fix), waits for approval — then proposes the
  next skill per branch: product → habit-first, feature → arch-first,
  fix → audit-first.

  Principle: without a defined type, the downstream skills are built
  on guesses. idea-first closes this gap before all the others.

  Use when: automatically as the first step after task creation;
  manually before any task needing type + scope check
---

# Idea-First Protocol

Idea-first is the **entry point** of the self-organizing skill chain. Runs right after the task is created, before any technical analysis.

**Why:** without an explicit definition of the task type the next skills are built on guesses — arch-first decomposes a fix into blocks when audit-first was needed, library-first looks in a non-existent layer, the agent goes into code when habit design is required.

Idea-first closes this gap with a 5-10 minute dialog.

**Key principle:** idea-first **does not read code** — it determines the task type through dialog. Code is read by the next skills.

## Input

A new task description just registered by the fast-track flow.

## Output

`idea-first-{N}.md` fixing the task type (product / feature / fix) and scope, after 5-7 discovery questions and user approval.

## Hands off to

`habit-first` (product), `arch-first` (feature), or `audit-first` (fix), based on the classified type.

---

## Step 0 — Check task context

Ensure `{log_dir}` and `{slug}` are known.

If not — run resolver (list recent tasks, prompt user), then continue.

**Cannot skip.** Without `{log_dir}` the artifact will not be saved.

---

## Step 0.5 — Hot-fix exception

If the task is an obvious small edit (one line, a typo, a known problem with a known fix) — **skip all of idea-first** and go straight to execute.

### Signs of a hot-fix

| Sign | Example |
|---|---|
| One line / one value | Change timeout from 30 to 60 sec |
| Typo / formatting | Fix a typo in a button label |
| Known fix for a known problem | Remove a duplicate in SQL you added yourself |
| Time to complete < 5 minutes | — |

### What to output

```
Looks like a hot-fix — one line / obvious edit.
Skipping idea-first → going straight to execute.
If more complex than it looks — say "stop" and we'll launch idea-first.
```

Then 3 short steps:

1. **Register block 1 in task_blocks** — hot-fix = one task = one block. `atom_type='manual'`, `source='idea-first'`. `INSERT OR IGNORE` guards repeats.
2. **Execute** — Claude does the edit manually (Read / Edit / Bash). After completion — commit + push, remember `{last_commit_hash}`.
3. **Finalize via `$ship-first` task-level** — invoke WITHOUT `{block_num}` → activates task-level mode: closes block 1, updates STATUS.md, appends sessions.md.

**Hot-fix branch is done here.** No `flow-first-*.md` / `library-first-*.md` / `plan-first-*.md` — that's specific to the short path.

If unsure whether it's a hot-fix — launch idea-first. Better 5 minutes of calibration than the wrong way.

---

## Step 1 — Discovery questions

Ask 5-7 open questions. Understand the task at the why / for-whom / how-often level, not only technical.

### Baseline set

| # | Question | What we're figuring out |
|---|---|---|
| 1 | What hurts — what problem are we solving? | Type of pain |
| 2 | Is this new or already exists? | Product vs feature vs fix |
| 3 | Who will use it — only you or others? | Habit-fit / scope |
| 4 | How often — every day / by event / one-off? | Habit loop (if a product) |
| 5 | Is there something similar already in the project? | Anchors for the next skill |
| 6 | What should exist at the end — in one sentence? | Final scope |
| 7 | (optional) Deadline or background? | Work mode |

### Rules

- **Open-ended, not yes/no** — "who will use it?" not "is it for you?"
- **One at a time** — don't dump all 7 at once
- **Adapt on the fly** — clear "fix" signal → skip habit questions

### Shortened mode

If task.md already shows the type — ask only 2-3 clarifying questions, not all 7.

---

## Step 2 — Task type determination

### Three types

| Type | Sign | Next skill |
|---|---|---|
| **New product** | Building from scratch, for people, habit loop needed | `habit-first` |
| **New feature** | Adding inside existing product/system | `arch-first` |
| **Fix / problem** | Something broke or works incorrectly | `audit-first` |

### Heuristics

| Sign from answers | Type |
|---|---|
| "Want to build X for myself/team/clients" | New product |
| "Add Y into existing Z" | New feature |
| "Extend the functionality of A" | New feature |
| "Broken", "not working", "bug" | Fix |
| "Security hole", "vulnerability" | Fix |
| "Audit", "find gaps in X" | Fix |

### Subtypes

| Subtype | Type | Specific |
|---|---|---|
| Hot-fix | Fix | Already cut off in Step 0.5 |
| Refactoring | Fix | Not a bug — still audit-first |
| Epic / large task | Any | 5+ blocks → arch-first regardless of type |
| Skill / agent | Feature | AI infra special case |

### If unambiguous determination fails

Show options with rationale, ask user. Do not guess.

---

## Step 3 — Calibration + approval

Before writing the artifact — show user the determined type + scope and wait for explicit approval.

### Output format

```
Based on the answers I determined:

**Type:** {product / feature / fix}
**Subtype:** {if any}
**Scope:** {1-2 sentences}
**Out of scope:** {what we don't do}

Next step → {habit-first / arch-first / audit-first}

Ok? Or correct me.
```

### Variants

| Answer | Action |
|---|---|
| "ok" / "go" / "yes" | Proceed to Step 4 |
| Type correction | Update → show again → wait for approval |
| Scope correction | Update → show again → wait for approval |
| "stop" | Stop, wait for instructions |

**Prohibited:** proceeding to Step 4 without explicit type approval.

---

## Step 4 — Write the artifact

After approval — write `idea-first-{N}.{R}.md` to `{log_dir}` and register in routing DB.

Default `{N}` = `0` (task-level, since idea-first runs before block decomposition).

### File format

```markdown
> 🔗 Task: {log_dir}/task.md

# Idea-First — {N}.{R}

**Date:** {date}
**Task:** {slug}

## Type
**{product / feature / fix}** — {subtype if any}

## Scope
{1-2 sentences}

## Out of scope
{what we don't do}

## Discovery answers
| # | Question | Answer |

## Next skill
`{habit-first / arch-first / audit-first}` — because {rationale}
```

Register in task_artifacts + append row to `## Task files` in task.md.

---

## Step 5 — Route to the next skill

After writing the artifact — **automatically** invoke the next skill per type. Do not ask.

| Task type | Next skill | What it does |
|---|---|---|
| New product | `Skill('habit-first')` | Designs habit loop → outputs Habit Brief → hands off to arch-first |
| New feature | `$arch-first` | Decomposes into blocks → pins decisions |
| Fix / problem | `$audit-first` | Audit across 6 planes → gap table |

Context (`{log_dir}`, `{slug}`, artifact path) is passed via session — the next skill picks it up at Step 0.

---

## Anti-patterns

### ❌ Guess the task type from the title without questions

Received "migration logic" → decided "feature, going to arch-first" without discovery. The user meant a fix of an existing migration mechanism.

**Rule:** 5-7 questions (or 2-3 shortened) mandatory. Type derived from answers, not the title.

### ❌ Move to the next skill without type approval

Determined type → immediately called `Skill(arch-first)` without showing calibration. The user had no chance to correct.

**Rule:** Step 3 (calibration + approval) is mandatory. Explicit "ok" before Step 4.

### ❌ Read code inside idea-first

Asked 2 questions and went to grep the project structure "to understand better". That's the job of flow-first / audit-first.

**Rule:** idea-first works only through dialog. No Read / grep / find. Code reading in the next skills.

### ❌ Ignore the hot-fix exception

One-line config change. Agent honestly asked 7 questions, wrote an artifact, called arch-first. 30 minutes on a five-second edit.

**Rule:** Step 0.5 hot-fix exception — always check. Obvious one-step edit → skip idea-first.

### ❌ Inlining the skill instead of Skill()

Agent received task → executed idea-first protocol manually from memory, without `Skill()` tool. Outdated / incomplete protocol version, no accuracy guarantee.

**Rule:** always launch via `$idea-first`. Never imitate inline.

---

## Related skills

- **habit-first** — designs the habit loop for new products; invoked from idea-first for the "product" branch
- **arch-first** — decomposes features into blocks; invoked for "feature"
- **audit-first** — scans across 6 planes for fixes; invoked for "fix"
- **ship-first** — closes the task at the end; also handles the hot-fix short-path finalization

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'idea-first', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true` keeps a logging failure from aborting the skill.
