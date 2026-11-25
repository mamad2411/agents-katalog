---
name: cadence-first
description: |
  Meta-orchestrator: assigns skill-chain cadence per block (Tier 1/2/3) via Q1-Q6 rules.
  Reads target task_blocks + task.md, writes cadence-decisions-{R}.md artifact.
  Standalone (executor invokes) or Batch (generator hand-off).

  Use when: deciding cadence for a batch of blocks, generator hand-off from decomposition skills
---

# Cadence-First Protocol

Assigns one of three tiers per block:

- **Tier 1 Full** — `flow-first → library-first → plan-first → execute → ship-first`
- **Tier 2 Partial** — `library-first → plan-first → execute → ship-first`
- **Tier 3 Plan-focused** — `plan-first → execute → ship-first`

Rules live in `CADENCE_HEURISTICS.md` (colocated). This SKILL is the executor; the manifest is the source of truth, read **conditionally**.

Does NOT execute the block itself. Decides cadence, then hands off.

---

## Step 0 — Check task context

Are `{log_dir}` and `{slug}` known in the current session?

If yes → continue. If no → list latest task folders, ask which is current, set `{slug}` and `{log_dir}`. Cannot skip — without `{log_dir}` the artifact cannot be saved.

---

## Step 1 — Parse invocation mode

### 1.1 Detect standalone vs batch

| Signal | Mode |
|---|---|
| ARGUMENTS has `task_id=X block_nums=[...]` | Standalone |
| Invoked from generator context (parent inherits state) | Batch |
| No args, no context | Standalone (ask user) |

### 1.2 Extract parameters

Standalone: parse `task_id`, `block_nums` from ARGUMENTS. Batch: inherit from parent. If missing → ask.

### 1.3 Anti-recursion guard

If `task_id == {slug}` (framework session's own task) → warn and default to abort. Prevents writing into the framework session's own task.

### 1.4 Verify task exists

Query the routing DB for `id={task_id}`. Empty → abort with "task not found".

---

## Step 2 — Read sources (minimal by default)

### 2.1 Read target task_blocks

```bash
sqlite3 {routing_db} \
  "SELECT block_num, title, type, atom_type, status, recommended_cadence
   FROM task_blocks
   WHERE task_id='{target_task}' AND block_num IN ({block_nums_csv})
   ORDER BY block_num"
```

**Defensive column check:** `PRAGMA table_info(task_blocks) | grep recommended_cadence`. Column exists → `write_to_db=true`. Missing → markdown only.

### 2.2 Read target task.md

Extract task type/scope, `## Blocks` table if present, HIGH-risk tags.

### 2.3 Scan landscape artifacts

List recent artifacts in the target log_dir. Look for `{layer}-plan-{code}.md`, recent `flow-first-*.md`, `note-*.md` claiming landscape coverage, roadmap docs referenced in task.md.

Landscape found → Q2 signal "skip flow". Absent → Q2 signal "keep flow".

### 2.4 HEURISTICS.md — CONDITIONAL read

**Do NOT read by default.** The cheat sheet below is authoritative. Read the manifest only when:

- Q1-Q6 answer ambiguous on ≥1 block → read the section for that Q
- Distribution alarm → read anti-pattern + ratios sections
- Output shape doubtful → read canonical spec
- Retroactive on legacy task → read legacy migration section

---

## Q1-Q6 Cheat Sheet

| Q | Question | Answer → signal | Effect |
|---|---|---|---|
| Q1 | Block changes PROD code / state? | title has push/deploy/migrate/schema/prod → **YES**. Doc/research titles → **NO**. | YES + Q4 NO → Tier 1 lock. YES + Q4 YES → Tier 2 batch cycle |
| Q2 | Landscape captured in adjacent artifact? | plan doc / prior flow-first / note claims landscape → **YES**. First block, no context → **NO**. | NO → flow-first mandatory (min Tier 1). YES → skip flow, continue |
| Q3 | New library-vs-scratch decision? | First-of-kind / new integration / new schema → **YES**. Sibling of audited / trivial mechanical / doc → **NO**. | YES → keep library-first (Tier 2). NO → skippable |
| Q4 | Deliverable = doc / diagnostic / mechanical batch? | note/spec/audit/smoke/verify/finalize titles → **YES**. N-identical mechanical → **YES**. Sibling mirror of audited block → **YES**. | YES → Tier 3 plan-only. NO → Tier 2 default |
| Q5 | HIGH-risk override? | Explicit HIGH tag / silent-failure watchpoint / cross-cutting / discovery-heavy / rollback-complex → **YES**. | YES → Tier 1 override regardless of Q1-Q4 |
| Q6 | Block CREATES lib primitive consumed by downstream? | Title has "extract to lib" / new file in `lib/` referenced later → **YES**. Consumer using existing lib → **NO**. | YES → Tier 1 anchor + FLAG if consumer's block_num < producer's |

### Q6 ordering check

For each Q6=YES producer, verify `producer.block_num < min(consumer.block_num)`. If violated → warn user with concrete swap suggestion. Do not silently INSERT consumer-first ordering. User confirms swap or overrides with explicit rationale.

---

## Step 3 — Apply Q1-Q6 per block

For each block: answer Q1→Q6, consolidate to tier via matrix.

### 3.1 Tier matrix

| Q1 | Q2 | Q3 | Q4 | Q5 | Tier |
|:-:|:-:|:-:|:-:|:-:|:-:|
| YES | — | — | NO | NO | **1** |
| YES | — | — | YES | NO | **2** (batch cycle) |
| NO | NO | — | — | NO | **1** (flow-first needed) |
| NO | YES | YES | NO | NO | **2** |
| NO | YES | NO | YES | NO | **3** |
| NO | YES | NO | NO | NO | **2** (median) |
| any | any | any | any | YES | **1** (override) |
| any | any | any | any | Q6=YES | **1** (lib-first anchor + ordering check) |

Store per-block: tier + Q-triggers rationale (yes/no + detected signal per Q) for Step 4.

### 3.2 Distribution sanity check

- **>70% Tier 1** → warn "possible uniform-cycle bias — verify HIGH-risk classifications"
- **>80% Tier 3** → warn "possible under-classification — flag skill-writing blocks for elevation"

---

## Step 4 — Generate output (canonical shape)

**Verbatim format. No column reorder, no rationale omission, no shape drift.**

### 4.1 Main table

```markdown
## Cadence decisions — {target_task}

| # | Block title | Flow | Library | Plan |
|:-:|---|:-:|:-:|:-:|
| {N} | {title} | ✓/✗ | ✓/✗ | ✓/✗ |
```

Tier mapping: Tier 1 → ✓✓✓, Tier 2 → ✗✓✓, Tier 3 → ✗✗✓.

### 4.2 Rationale per block

```markdown
### Rationale per block

**Block {N} — {title}:** 1-3 sentences citing Q-triggers with detected signals.
```

### 4.3 Aggregate observations (optional)

Fire if pattern spans blocks OR distribution warning triggers.

---

## Step 5 — Write artifact + routing.db

### 5.1 Round number

Scoped to target task's log_dir, not framework session's.

### 5.2 Write cadence-decisions-{R}.md

Header referencing target task.md, main table, rationale per block, aggregate observations if any, plus per-block Q-trigger audit trail (Q1-Q6 signals + assigned tier).

### 5.3 Register in task_artifacts

INSERT with `artifact_type='cadence-decision'`.

### 5.4 UPDATE task_blocks.recommended_cadence (defensive)

If `write_to_db=true`, UPDATE per block. Missing column → skip UPDATE, log warning. Existing non-NULL → prompt override, default preserve prior decision.

### 5.5 Append to task.md `## Task files`

---

## Step 6 — Hand-off

### Standalone

Chat summary: artifact path, blocks analyzed, distribution counts, manifest version, any warnings. Full table + rationale already shown in Step 4.

### Batch (called from generator)

Return structured JSON to caller: `task_id`, `artifact_path`, `manifest_version`, per-block `{block_num, tier, cadence}`, `warnings`. Batch does NOT print table to chat — the generator handles output.

---

## Anti-patterns

### ❌ Applying baked heuristics without version check

Read HEURISTICS when Q ambiguous / distribution alarm / shape doubt. Don't apply outdated baked heuristics.

### ❌ Framework recursion

`task_id` equals framework session slug — cadence-first writes into its own task. The Step 1.3 guard is mandatory.

### ❌ Output shape drift

Format change → manifest patch first, never SKILL-only. Consumers depend on the exact shape.

### ❌ Silent override of existing cadence

Existing non-NULL → prompt override, default preserve prior decision. Never silently overwrite.

### ❌ Inlining Q1-Q6 evaluation

Executing the logic manually without invoking the tool — no artifact, no audit trail. Always via `Skill('cadence-first')`.

---

## When to read HEURISTICS.md

| Trigger | Read section |
|---|---|
| Q1-Q6 answer ambiguous | the section for that Q |
| Distribution warning | anti-pattern + ratios |
| Output shape doubt | canonical spec |
| Retroactive on legacy task | legacy migration |
| Manifest version check | frontmatter |

Otherwise: skip. The cheat sheet above is authoritative.

---

## Related skills

- **decomposition skills** — invoke batch mode after generating a block list
- **flow-first / library-first / plan-first** — sub-skills whose invocation cadence-first decides; NOT invoked by this skill
- **dev-auto-first** — auto-invokes cadence-first before each block cycle

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'cadence-first', datetime('now'))" 2>/dev/null || true
```
