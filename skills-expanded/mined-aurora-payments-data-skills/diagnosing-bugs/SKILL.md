---
name: diagnosing-bugs
description: Diagnosis loop for hard data bugs and pipeline regressions. Use when the user says "diagnose"/"debug this", reports numbers that look wrong, rows missing or duplicated, a pipeline broken/failing/slow, a backfill gone bad, or a data-quality alert firing.
---

# Diagnosing Bugs

A discipline for hard data bugs: wrong numbers, missing rows, broken or slow pipelines. Skip phases only when explicitly justified.

When exploring the pipeline, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant models, check ADRs in the area you're touching, and pull the lineage of the affected asset from declarations (asset deps, `ref()` edges), since lineage is the map every later phase navigates by.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first** and write `<REDACTED>` in its place. Build loops against env vars and the project's existing credential file (`profiles.yml`, `.dbtconnection`, a service-account key path), so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers and connection strings: quote only the lines that carry the signal.

A data pipeline leaks a second class of secret that code alone does not: **the rows themselves**. A pinned query's output is real production data. Before showing query results, a sampled slice, or a captured source file, cut them to the columns the diagnosis needs, and mask the values that identify a person or a customer, such as cardholder and account numbers, names, emails, addresses and bank details. Row counts, aggregates, key hashes and the shape of a duplicate are what carry the diagnostic signal; the identifying values almost never are. Where a real key must be shown to be argued about, show one, not the set.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug, one that goes red on _this_ bug, you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one: try them in roughly this order

1. **Failing test** at whatever seam reaches the bug: a unit test with mocked inputs (dbt `unit_tests:` with `given:`/`expect:`), a data test, a pipeline integration test.
2. **Pinned failing query.** One SQL statement against time-travel-pinned inputs (pin per Phase 2's "Pin the evidence") that returns the rows violating the expectation. Zero rows = green.
3. **Single-partition rebuild.** Rebuild one model for one partition into a scratch schema from pinned inputs; assert on the output.
4. **Differential loop.** Run the same pinned input through old vs new code (or prod table vs scratch rebuild) and diff in SQL with `EXCEPT DISTINCT` (BigQuery; plain `EXCEPT`/`MINUS` in Snowflake) both directions, or a keyed `FULL OUTER JOIN`. The warehouse is the diff engine.
5. **Replay a captured source file.** Save the raw file / payload that produced the bad rows; replay it through the loader or parser in isolation.
6. **Throwaway harness.** The bug model's SQL with upstream refs swapped for fixture CTEs or seed tables: one query, mocked world.
7. **Bisection harness.** If the bug appeared between two known states (commit, run, partition date), automate "build at state X, check, repeat" with `git bisect run` across code, or walk partition dates to find where the bad data starts.
8. **Segment sweep.** If the bug is "sometimes wrong output", run the check across every partition × dimension value and map where failures concentrate.
9. **HITL bash script.** Last resort. If a human must eyeball a dashboard, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Query one partition, not the table. Diff only the failing keys. Never a full refresh inside the loop.)
- Can I make the signal sharper? (Assert on the exact rows and the exact measure, not "row counts look close".)
- Can I make it more deterministic? (Pin inputs per Phase 2's "Pin the evidence", pin the code ref, name the partition explicitly, because production tables mutate mid-diagnosis and an unpinned loop rots while you work.)

A ten-minute full-refresh loop is barely better than no loop; a seconds-scale pinned query is tight, and a debugging superpower.

### Non-deterministic bugs

In a pipeline, "flaky" almost always means a **moving input**, not a race: late-arriving rows, a scheduled rebuild landing mid-diagnosis, an unpinned `CURRENT_DATE()`. Pin first, because most flakes die there. For genuine non-determinism (unordered aggregates like `ANY_VALUE`, `LIMIT` over tied sorts, parallel writers), loop the build against pinned inputs and diff runs against each other. The goal is not a clean repro but a **higher reproduction rate**, so keep raising it until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to the warehouse or environment that reproduces it, (b) a redacted captured artifact (the raw source file, orchestrator run logs, warehouse job history, a snapshot of the bad table taken before it rots), or (c) permission to add temporary instrumentation to the production pipeline. Do **not** proceed to hypothesise without a loop.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** (a script path, a test invocation, a curl) that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring". It must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds for a pinned query; minutes at worst for a single-partition rebuild. Never a full refresh.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop. Jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red: the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Pin the evidence

Production tables mutate mid-diagnosis, because scheduled runs, backfills and other people's merges all move your repro. Before minimising, pin: query the inputs `FOR SYSTEM_TIME AS OF` the failure (BigQuery keeps 7 days by default; Snowflake 1), and snapshot the failing rows plus the aggregates you are chasing into a scratch table for any incident that might outlive the time-travel window. From here on the loop runs against pinned state, never against live tables.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut date ranges, segments, source files, columns, and upstream models **one at a time**, re-running the loop after each cut, keeping only what's load-bearing for the failure. The end state is usually one partition, a handful of keys, and one model.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

**Classify first.** Every data incident is some mix of three causes: the **data changed** (a source shifted shape or content), the **code changed** (a deploy altered logic), or an **operation failed** (a run didn't happen, half-happened, or ran twice). Name the mix before generating hypotheses, because each class has a different search space.

Then aim the hypotheses:

- **Walk lineage upstream.** Check each upstream input of the bad asset; the cause enters at the **most upstream node that exhibits the issue**. Hypotheses about downstream symptoms of an upstream defect are noise.
- **Segment the delta.** Slice the discrepancy by dimension: source, segment, time bucket. Where the anomaly concentrates is where the cause enters; a delta spread evenly across segments points at logic, a delta concentrated in one source points at that source.
- **Suspect the code that wrote the data, not HEAD.** The table was produced by whatever version last ran, whether a stale rebuild, a reverted hotfix or an old image. Arbitrate with the warehouse's last-modified timestamps, git history, and run artifacts (dbt's `target/manifest.json` carries the compiled SQL as-run). Reading HEAD to explain data HEAD never produced is the classic dead end.

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea. Expect more than one cause, because multi-factor incidents are the norm, so a confirmed hypothesis doesn't retire the list until the full delta is accounted for.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it; proceed with your ranking if the user is AFK.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Targeted diagnostic queries** at the lineage boundaries that distinguish hypotheses. One aggregate at the right boundary beats ten row dumps.
2. **Scratch rebuilds**: rerun one model into a scratch schema with exactly one variable changed: one input pinned to the old snapshot, one flag flipped, one CTE swapped.
3. Never "SELECT * and stare".

**Tag every probe artifact** with a unique prefix: scratch tables `debug_a4f2_*`, log lines `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep and a single `DROP`. Untagged scratch tables survive; tagged ones die.

**Perf branch.** For slow queries and slow pipelines, row-level probes are usually wrong. Instead: establish a baseline (query plan, bytes scanned, slot- or task-time from run history), then bisect the query or the DAG. Measure first, fix second.

## Phase 5: Fix + regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is the layer where the bug pattern actually lives. A parser defect gets a test at the parser, not a patch in downstream SQL; a join fan-out gets a test on the joining model with fixture inputs that reproduce the fan-out, not a distinct-count slapped on the mart. Fix and test at the **most upstream node that exhibits the issue**, since everything downstream inherits the correction.

**If no correct seam exists, that itself is the finding.** Note it. The pipeline architecture is preventing the bug from being locked down, whether by logic buried in a model too tangled to unit-test or an increment that can't be safely re-run. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam: a unit test with mocked inputs for logic bugs, a build-gating assertion (`severity: error`) for invariant violations.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. **Backfill down.** Recompute every downstream partition the bad data touched: fix upstream, then backfill down. Partition-overwriting, idempotent tasks make the re-run safe; if the affected models aren't idempotent, that is a Phase 6 finding.
6. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario, **against live tables this time**. The pinned snapshot proved the fix; the live re-run proves the backfill.

## Phase 6: Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop against live tables)
- [ ] Regression test passes **and is registered where it gates**: a test CI never runs guards nothing (or absence of seam is documented)
- [ ] Backfill verified: the full repaired range re-checked, not just the repro partition
- [ ] All tagged probe artifacts removed: `grep` the `[DEBUG-...]` prefix, `DROP` the `debug_*` scratch tables
- [ ] Throwaway harnesses and loop scripts deleted (fixture-CTE harnesses, replay scripts, bisection harnesses, copied `hitl-loop` scripts), or moved to a clearly-marked debug location
- [ ] The hypothesis that turned out correct, and its cause class (data change / code change / operational failure), is stated in the commit / PR message, so the next debugger learns

**Then ask: what would have caught this bug sooner?** Two guard shapes: an **assertion** if the invariant is now known (deterministic, gates the build), or an **anomaly monitor** if this was an unknown-unknown a learned baseline would have flagged (freshness, volume, schema, distribution). Ship one with the fix. If the answer instead involves architectural change (no good test seam, a non-idempotent increment, logic that can't be unit-tested), hand off to the `/improve-codebase-architecture` skill with the specifics. Make the recommendation **after** the fix is in, not before, because you have more information now than when you started.
