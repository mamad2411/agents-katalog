---
name: arch-first
description: |
  Protocol for architecturally clean execution of complex multi-block tasks.
  Decomposition into blocks → research before library-first → explicit
  decision pinning → clear scope vs out-of-scope → report after each block.
  Principle: every architectural decision is pinned explicitly, no ambiguity,
  epics don't sprawl.

  Use when: task has 5+ blocks; DB migration; rewriting skills;
  any task where architectural cleanliness must be preserved over distance
---

# Arch-First Protocol

A meta-skill for executing **architectural tasks** — too big for a fast-track, too small for a full feature-execution. Use when:

- The task decomposes into 5+ blocks with dependencies
- Affects several layers (DB + code + skills + prompts + configs)
- Requires decisions on multiple forks (not just execution)
- May spawn a follow-up epic after closure
- Architectural cleanliness over distance is principally important

## Input

A 5+ block feature task (typically routed from `idea-first`); optionally a Mode Brief path.

## Output

`research-doc.md` with baseline assessment; block decomposition (5-15+ atomic blocks) inserted into `task_blocks`; per-block reports as blocks close.

## Hands off to

Per-block `flow-first` cycle for each open block, then `ship-first` at task-level closure.

---

## Principles

### 1. Decomposition by BLOCKS, not tasks

A large task = numbered blocks with an explicit goal each. Blocks live inside one task, in one `task.md`. An epic appears when a block is deferred or extracted.

Execution order != numbering order — reflects real **dependencies**.

### 2. Research BEFORE library-first

If the task has an unfamiliar component (new skill, new DB, unstudied table) — a separate **research phase** before planning.

Research outputs a **comparison table** "as is vs should be" with criticality (HIGH/MED/LOW) per item.

Without research → library-first builds on guesses → wrong scope estimates → missed deadlines.

### 3. Explicit pinning of architectural decisions

After each fork — pin the **decision with rationale** in task.md or a dedicated `decision-NN.md`.

Structure:
```
### Decision N — Brief statement

We choose **X** (not Y, not Z).

**Rationale:**
1. Specific reason 1 (with example)
2. Specific reason 2

**Alternatives:**
- Y — rejected (why)
- Z — rejected (why)

**What changes:** [specific file-level deltas]
```

Without explicit pinning → two weeks later the developer re-opens the discussion or makes the wrong choice.

### 4. Clear scope / out-of-scope

Each task has an explicit "Not in scope" section with a marker for where it goes:
- Separate fast-track after the task
- Separate epic
- Backlog
- Never (with reason)

Without this → the epic sprawls indefinitely.

### 5. Report after EVERY block

One block = one `report-NN.md` in the task log. Structure:
```
# Report NN — Block X: {name}

**Status:** ✅ Done | ⚠️ Partial | ❌ Failed

## What was done
## Architectural decisions realized in this block
## Files / git
## What was NOT done (intentionally)
## Known risks / mitigation
## What remains / next steps
```

Provides a **complete chronology of decisions** for future sessions and other agents.

### 6. Multi-layer data protection

Every DB change = at least **3 backup layers**:
1. ssh snapshot of the DB file before the block starts
2. Inside the migration script — its own backup before UPDATE/DDL
3. Git-hook snapshot on every push

For critical changes — a **pre-check script** that `exit 1` if data is found that would cause the migration to fail. Without a pre-check the migration must not be launched.

**Pre-check as bonus value:** pre-check scripts often find **data problems** useful independently of the main migration. Rule: even if the task failed — execute the fixes found by the pre-check separately (if safe and improve data consistency).

**Verify scripts account for staged migrations:** when a task is broken into phases, the verify script must know about the transient state and exclude legacy data via an explicit exclusion list. Once the final phase runs and legacy fields are removed — drop from the list.

**Real-client data is sacred (the main rule).**

Before any destructive action on tenant data — **classify the tenant**:

| Tenant type | Destructive allowed? |
|---|---|
| `demo`, `sandbox`, `test_*` | Yes, with a backup |
| Active client | **NO** without explicit confirmation from the **tenant owner** |

If unclear which category — **ask BEFORE formulating a recommendation**, not after.

**Alternatives to DELETE for legacy data of a live client** (in order of preference):
1. **Migration via mapper** — convert data to the new model with a mapper script. At ambiguities keep a `_legacy_fields` section for manual review.
2. **Archive** — export content to a legacy-archive folder, then DELETE from DB. Content preserved in git, DB clean.
3. **DELETE** — only with explicit confirmation from the tenant owner by name.

Lesson: "old model" != "can be deleted" — the old model often contains **current content** in an outdated format.

### 7. Idempotency of migration scripts

Every migration script must be safe to re-run:
- `CREATE TABLE IF NOT EXISTS`
- `CREATE UNIQUE INDEX IF NOT EXISTS`
- `INSERT OR IGNORE`
- `UPDATE ... WHERE col IS NULL` (fills only unfilled)
- Pre-check: "already done? — skip"

Without idempotency — a re-run breaks data, especially at a decision-gate.

### 7.5 Parameterize tools instead of copying

When a second instance of a tool (verify script, migration script) is needed for another component **of the same type** — **parameterize** the existing one, don't copy.

**Trigger:** 2+ instances differ by only one variable (`card_type`, `tenant`, `table_name`).

**When copying is actually better:** instances differ in essence of logic (different algorithms, different data sources). If the difference is only in parameters — parameterize.

### 8. Decision gates during execution

After critical steps — an **explicit gate** with a pause and agreement. In the plan-first table these steps are marked as `verify-gate` or `decision-gate`.

**If a gate-blocker is critical (task infeasible in current formulation) — create `decision-NN.md`:**

```
# Decision NN — {short fork description}

**Status:** Awaiting user decision

## Context
## Question to the user
| # | Option | Essence | Complexity |

## Recommendation (with rationale)

## User response
```

A **formal artifact** — a future agent in another session can read the decision and understand history.

### 9. Registration in routing DB and closure via the protocol

After task completion:
- Final `report-NN-closure.md`
- Update routing DB: `status='done'`
- Update project `STATUS.md`
- Append to `sessions.md`
- Follow-up → create a **new epic** (do not leave the task open)
- Push artifacts + sync

### 10. No scope creep

If a new problem is found during execution — **do not expand the current task's scope**. Pin the finding in:
- task.md section "Found along the way, not doing now"
- Create a separate fast-track or backlog item

### 11. Cross-skill consistency check

When updating one skill of a family — **mandatory** check of upstream/downstream pointers in other skills of the same family.

**Specific checks:**

```bash
# 1. Find all mentions of the updated skill as a pointer / next step
grep -rn "/skill-X\|skill-X SKILL\|next step.*skill-X" \
  {skills_root} --include="SKILL.md" | grep -v "skill-X/SKILL.md"

# 2. After sync — verify diff is empty across all targets
for t in {sync_targets}; do
  diff -q {master_path}/skill-X/SKILL.md "$t/skills/skill-X/SKILL.md"
done
```

**Rule:** on any change to a skill in a family — add to acceptance criteria "grep upstream/downstream pointers, fix stale ones". **5 minutes of checking = years of no regressions.**

---

## Workflow of an arch-first task

### Step 0 — Check/create the task

If `{log_dir}` is set — proceed silently.
If not — create task via slug, mkdir log_dir, INSERT into artifacts, create task.md.

**Cannot skip.** Without a known `{log_dir}` research data is lost on session drop.

### Step 0.5 — Calibrate incoming artifacts

Check for `idea-first-*.md` (task type + scope) and optionally `habit-first-*.md`.

- If found — read via Read tool, extract task type + scope + out-of-scope. Use in Phase 0 and Phase 2 as explicit context. If type is "fix" — consider calling audit-first instead.
- If not found — skip calibration, proceed with Phase 0 via standard dialog.

### Phase 0 — Task understanding

Do not start until it's clear:
- What exactly hurts? (root cause, not symptom)
- Which layers are affected?
- Where are the current gaps?
- What counts as "task closure" (acceptance criteria)
- If task is about a specific tenant: classify type. Affects allowed destructive actions.
- If task is about legacy data: technical junk or meaningful business content? Content = migration or archive, not DELETE.

### Phase 1 — Research (if needed)

Read-only research: read skills, SELECT from DB, grep across the project, compare with reference.

Output = **comparison table + criticality**. Save as `{log_dir}/research-doc.md` and register in task_artifacts.

**Cannot skip.** On session drop, chat research is unrecoverable.

### Phase 1.5 — Feasibility check (CRITICAL)

Before decomposition — **check basic constraints** that could make the task infeasible. A **5-minute check** that saves hours.

Common checks by task type:

| Task type | What to check |
|---|---|
| FK between SQLite tables | Tables in one DB file? SQLite doesn't support cross-file FK |
| Trigger on a view | SQLite supports only INSTEAD OF triggers on views |
| Recreate referenced table | Incoming FKs exist? Need `PRAGMA foreign_keys=OFF` |
| ALTER TABLE ADD CONSTRAINT | SQLite doesn't support — recreate needed |
| ATTACH DATABASE | Limit on attached DBs (default 10) |

**If feasibility check finds a blocker:**
1. Pin blocker in `decision-NN.md`
2. Propose alternatives
3. Don't try to "brute-force through" — that is anti-arch-first

### Phase 2 — Decomposition into blocks

Numbered list of blocks. Each block:
- Atomic (one thematic layer)
- Explicit goal
- Criticality rationale (P0/P1/P2)

Pin in task.md as "Plan". Execution order reflects dependencies.

**Prohibition of "urgent block 0".** Blocks numbered from 1. Urgent problems mid-task → separate fast-track via `idea-first` branch, not "block 0". After hotfix return to arch-first task.

**Mandatory final block — UI/AI-first audit.** Last block of the plan = UI/AI-first audit via `/ui-ai-first`. Surfaces operations accessible only via code/curl/SQL, forms roadmap. Without this report the task isn't considered closed.

After pinning — INSERT each block into task_blocks with source='arch-first', status='pending', sort_order=block_num*100.

Sub-blocks: `block_num` N.M = N*10+M, `sort_order` = block_num*10, `parent_block_num` = N.

### Phase 2.5 — Batch call to cadence-first

Right after INSERT loop and before final Phase 2 step — call cadence-first in batch mode so every created block receives `recommended_cadence` pre-baked.

```
Skill('cadence-first', task_id='{slug}', block_nums=BLOCK_NUMS)
```

Cadence-first applies Q1-Q5 per block, UPDATEs `recommended_cadence`, writes `cadence-decisions-{R}.md`.

**Why here:** cadence is decided at generation time (rich context in current session) not at execution time (block title alone is thinner).

### Final step of Phase 2 — Ask work mode

```
Blocks pinned. How do we work?

1. Manual — I run each block myself
2. Autopilot — dev-auto-first takes over
```

If "1" → `Skill('flow-first')` for the first block.
If "2" → `Skill('dev-auto-first')`.

**arch-first is done here.** Per-block cycle spins via `Skill()` links between skills without arch-first participation.

### Phase 3-6 — Per-block cycle (through Skill() chain)

```
flow-first → library-first → plan-first → execute → ship-first (per block)
     |
     (ship-first closes block, UPDATEs task_blocks)
     |
     (if open blocks) → flow-first of next block
     |
     (all blocks done) → ship-first task-level: UI/AI-first audit +
                         arch-map + sessions.md + STATUS.md + summary
```

arch-first **does not orchestrate** execution. The chain runs itself.

---

## Communication style

### Short messages, small blocks
Not writing walls of text. Every message — a specific step or question. Long report = in a file, in chat — a summary.

### Tables for comparisons
Comparing options, before/after, layers — use a table. Not text.

### Explicit recommendations with rationale
If there's a choice — I give my recommendation + 2-3 reasons + what changes with the alternative. Not "decide yourself what's best".

### Decisions = user's, execution = mine
Architectural forks — I ask. Technical details — I decide myself. If unsure where the line is — better to ask.

### Rollback always possible
Every step — reversible or with a backup. "Rollback points" in plan-first — a mandatory section.

---

## Anti-patterns

### ❌ "Do it all in one epic"
Better to decompose into 7 blocks and walk them one at a time than design everything at once and get lost.

### ❌ "Let both variants coexist"
A hybrid (old + new model in parallel) is an anti-pattern. That's the very "diverging truth" we usually come in to fix.

### ❌ "The script is complex, I'll help understand it later"
A script without `--apply` / dry-run by default + without a backup — I don't write it. The user must be able to run it safely on the first try.

### ❌ "This is obvious, I won't pin it"
An architectural decision taken in chat after 2 weeks = unknown. Pinning is **mandatory**, even if it seems obvious.

### ❌ "I'll expand this task's scope"
Every finding along the way = a separate ticket. Not "let's clean X while we're at it".

### ❌ "Brute-force through an architectural blocker"
If infeasible in current formulation — **stop**. Create decision-NN.md, propose options, wait. Do not invent a "hybrid" to avoid coming with a problem.

### ❌ "This is just legacy, delete and forget"
Before any DELETE on tenant data — find out tenant type (demo / sandbox / real client) and data meaningfulness. "Old model" != "can be deleted". On live-client data DELETE is prohibited without explicit owner confirmation.

### ❌ Inlining the skill instead of Skill()
Always launch via `Skill('arch-first')` tool. Never imitate the protocol inline — even if it seems you "know how it works".

---

## Related skills

- **library-first** — reuse audit per block
- **plan-first** — mandatory plan before any action
- **flow-first** — landscape alignment before library-first
- **cadence-first** — batch cadence assignment for created blocks
- **ship-first** — per-block closure + task-level closure with UI/AI-first audit
- **audit-first** — sibling protocol for "fix" type tasks (arch-first is for features/products)
- **dev-auto-first** — autopilot orchestrator invoked after arch-first blocks are pinned

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'arch-first', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true` keeps a logging failure from aborting the skill.
