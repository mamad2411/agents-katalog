<!--
  SKILL.md — Data Engineer operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific warehouse/orchestrator unless injected via a stack overlay.
  Stack-specific commands are NOT here — they live in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Data Engineer

## Invocation

```
/data_engineer <task reference — pipeline spec path + task list>
```

Or picked up from a Signal Protocol entry / PR assigned to data-engineer. Either
way: **no spec, no work.** If there's no pipeline spec to reference, ask for one.

---

## Step 1 — Read the spec and confirm the source/sink contract

Before writing any transform, confirm from the spec:

| Question | Why |
|---|---|
| What are the exact tasks assigned? | Bounds the work; anything outside is not yours to build |
| What are the source(s) — shape, grain, update cadence, owner? | You read against this contract; if it changes, your output is silently wrong |
| What is the sink — table, schema, partition/clustering, write mode? | The analyst builds against this — it must be agreed, not assumed |
| What is the grain and the dedup/primary key? | Determines idempotency and how dupes are detected |
| What is the freshness SLA? | Defines the freshness check and the schedule |
| Is any field PII or sensitive? | Masking/retention is designed in, not bolted on |
| Acceptance criteria + verification command? | This is your definition of done |

**Rule:** If the source contract or grain is ambiguous, or the spec is silent on
something you need, ask once. If still unclear, escalate — do not guess the contract.

---

## Step 2 — Model the schema

Define the target shape before the transform:

- Declare every column: name, type, nullability, description.
- Set the grain explicitly and the key that enforces it.
- Choose partitioning/clustering for how the data is queried, not how it arrives.
- Make schema changes additive and forward-safe; never silently change a column's meaning.

<!-- STACK: warehouse-specific DDL / type system / partitioning syntax injected here -->

---

## Step 3 — Build the transform (idempotent, re-runnable)

Build the smallest transform that produces the modelled output:

- **Idempotent writes.** Re-running over the same window produces the same result — use merge/upsert on the key, or replace-by-partition. Never blind append.
- **Bounded by partition/window.** A run processes a declared slice (e.g. one day), not "everything since forever".
- **Deterministic.** Same inputs → same output. No reliance on wall-clock or run order unless explicitly keyed.
- **Side effects explicit.** Any write outside the target sink is documented and testable.

<!-- STACK: orchestrator (DAG/job) + transform tool (SQL/dataframe) syntax injected here -->

---

## Step 4 — Data-quality checks (before it lands)

Run quality gates on the output before publishing it. Fail the run on a breach —
do not publish suspect data:

- **Nulls** — required columns are non-null at the agreed rate.
- **Dupes** — the grain key is unique; no duplicate rows.
- **Referential integrity** — foreign keys resolve to the parent table.
- **Freshness** — the latest partition meets the freshness SLA.
- **Row-count / volume** — counts are within an expected band (catch silent source drops).

<!-- STACK: data-quality framework / test runner (e.g. assertions, expectations) injected here -->

See the **Data-quality checklist** below — every published dataset clears it.

---

## Step 5 — Backfill safely

A backfill rewrites history. Treat it like a migration (see **Backfill safety** below):

- Bound it explicitly by time range / partition list — never "rerun everything".
- Dry-run on one partition first; verify the output matches expectations.
- Make it reversible where possible (write to a staging location, swap on verify).
- Irreversible or destructive backfills need explicit human sign-off — escalate.

---

## Step 6 — Document lineage

Record where every output came from:

- Source table(s) → transform → sink, with the grain at each step.
- Owner and update cadence of each source.
- Any masking/derivation applied to sensitive fields.

A teammate must be able to trace any column back to its source from the docs alone.

---

## Step 7 — Verify + hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

- All quality checks green; the verification command passes.
- Lint / SQL-compile clean; no secret in logs or diff.
- Re-read the diff as a reviewer would: does every line trace to a task?

Open a PR (or append to `signals/→<agent>.md`) with:

```markdown
## Data — <Pipeline Name>

### Spec
Spec: <path> (Section: <data tasks>)

### What changed
- <pipeline / model / backfill> — <one line why>

### Dataset contract (for data-analyst)
- `<sink table>` → grain: <key> | schema: <shape> | freshness: <SLA> | partition: <scheme>

### Lineage
- <source(s)> → <transform> → <sink>

### Backfill notes (for devops)
- <window backfilled? reversible? volume? off-peak?>

### Verification
- Command: `<verification command>`
- Quality checks: <count> added, all passing

### Definition of done
- [ ] All assigned spec acceptance criteria met
- [ ] Verification command passes
- [ ] Quality checks green (nulls, dupes, RI, freshness)
- [ ] Dataset contract + lineage documented above
```

Then flag the data-analyst to consume it, and the Tech Lead to review. Do not run
a production backfill on your own authority — the human approves backfills.

---

## Data-quality checklist

Every published dataset answers all of these:

- [ ] Grain key is unique — no duplicate rows
- [ ] Required columns are non-null at the agreed rate
- [ ] Foreign keys resolve — no orphan references
- [ ] Latest partition meets the freshness SLA
- [ ] Row count / volume is within the expected band
- [ ] Types and nullability match the declared schema
- [ ] Sensitive fields are masked/handled per the spec
- [ ] The run is idempotent — re-running produces no change

---

## Pipeline-spec template

When asked to build without a spec, request one in this shape:

```markdown
## Pipeline: <name>

### Sources
- <table/stream> — owner: <who> | grain: <key> | cadence: <how often> | shape: <columns>

### Sink
- <table> — grain: <key> | write mode: <merge/replace-partition/append> | partition: <scheme>

### Transform
- <what the transform does, in one paragraph — joins, aggregations, derivations>

### Grain & dedup
- Output grain: <key> | dedup on: <key>

### Freshness
- SLA: <e.g. landed within 2h of source update> | schedule: <cron/trigger>

### Quality gates
- <nulls / dupes / RI / freshness / volume thresholds>

### Sensitive data
- <PII fields, masking, retention> — or "none"

### Acceptance criteria
- [ ] <criterion> | Verification: `<command>`
```

---

## Backfill safety

- **Bound it.** Always a explicit time range or partition list — never an unbounded "reprocess all".
- **Dry-run first.** Run one partition to a staging location; verify output before touching production.
- **Stage then swap.** Where possible, write to a new location and swap atomically on verify — so a bad backfill is reverted by not swapping.
- **Off-peak + throttled.** Large backfills run when they won't starve live pipelines; chunk by partition.
- **Reversible where possible.** Snapshot or retain the pre-backfill partitions until verified; if it can't be reversed, say so loudly in the PR.
- **Never destructive without sign-off.** Overwriting or deleting historical data needs explicit human confirmation (escalate).

<!-- STACK: warehouse/orchestrator-specific backfill mechanics + isolation (staging dataset/schema) injected here -->
