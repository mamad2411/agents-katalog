---
name: safe-backfill
description: "Run a standalone production data repair or reprocessing pass without losing progress or overwriting newer writes. Use when asked to fix existing records at scale, replay a bounded set of records, resume a halted repair, design a checkpointed data job, or prove that a repair actually converged. Freeze the eligible population and transformation, scan immutable keys in bounded batches, advance a durable checkpoint only with committed work or replay safely, guard each update against concurrent changes, and reconcile missing, mismatched and still-eligible rows before closure. Stop on lag, contention or unexplained drift. This does not own a schema migration's backfill: use db-migration for expand/contract and column population tied to a schema deploy. Not for a recurring ETL pipeline or event consumer."
allowed-tools: "Read, Grep, Glob"
---

# Safe Backfill

Treat the checkpoint as evidence of what was scanned, not a count of changed rows. A retry must not overwrite a fresh production write.

## Scope

Use for one-off repair or reprocessing of existing data without a schema change. Hand schema migration backfills to `db-migration`; use `event-driven-reliability` for a continuing consumer.

## Workflow

1. Record the source of truth, eligible predicate, transformation version, immutable unique ordering key and upper bound at start. A predicate and a key bound do not freeze membership when eligibility can change mid-run: a row that becomes eligible after its key was scanned is missed, and one that turns eligible just ahead of the scan is repaired outside the declared scope. Freeze the population itself: materialise the eligible keys (with their versions) into a scope table, or read through a real as-of snapshot or an eligibility-time cutoff, and make the scan and the reconciliation both use that same frozen scope. Rows created or made eligible later get a separate catch-up pass with its own frozen scope, not a moving end condition. If no stable key or frozen scope is available, stop and design one before running.
2. Choose batch size, transaction time limit, maximum lock wait, rate and explicit pause thresholds for replica lag, errors, contention and load with operators. Dry-run a bounded sample and record expected before/after values and estimated volume. Verify the datastore's transaction, comparison and snapshot behaviour before selecting an implementation; do not assume a particular SDK's semantics.
3. Scan `key > checkpoint AND key <= upper_bound ORDER BY key LIMIT batch_size` by immutable key, not offset and not only rows still needing work. For every candidate, compare against the current authoritative state. Make the transformation idempotent; conditionally update only if the read version or relevant source fields still match, and skip or re-evaluate conflicts rather than overwriting newer writes. Bound writes and commit each batch.
4. Atomically persist the highest **scanned** key with its batch's writes, if the store supports it. Otherwise persist the checkpoint only **after** the work commits, and require safe replay of the entire last batch. Never checkpoint first. An already-complete or conflicting row still advances the scanned high-water mark; an empty scan terminates only after reaching the bound or checking for remaining keys.
5. Inject failures before batch commit and after work commit but before checkpoint; restart from durable state and prove no missing, duplicate harmful, or stale overwrite effects. Exercise concurrent edits and all pause thresholds. If the transformation has non-idempotent external effects, stop and design durable deduplication or transactional fencing before execution.
6. Pause on a threshold breach; record last committed checkpoint, cause and resume owner. Reconcile against the frozen scope: independently find missing keys, mismatched values and eligible rows remaining (including late arrivals in a separately bounded catch-up pass). Investigate each category and sample guarded skips; matching counts alone are not proof of completion.

## Output

Produce a run sheet with predicate, bound, version, key, batch limits, checkpoint transaction boundary, conflict policy, failure-test results, pause/resume owner and reconciliation queries or equivalent checks. Do not mark complete until each discrepancy is explained or corrected and the independent reconciliation is clean.

## Anti-patterns

**Checkpointing by affected-row count.** Already-complete records cause the cursor to stall or skip keys. Advance by scanned key range instead.
