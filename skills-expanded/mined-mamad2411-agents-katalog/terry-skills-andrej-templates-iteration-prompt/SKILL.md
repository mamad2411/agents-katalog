# ANDREJ — One-Iteration Prompt Template

A fill-in-the-blanks contract for running ONE disciplined observe→analyze→act
iteration — either to brief yourself before a cycle, or to hand to a dispatched
worker so it iterates with the same discipline. ONE iteration = ONE bounded
change, gated on ONE scalar metric, logged to the ledger. The loop repeats the
contract; each pass changes exactly one variable.

> Fill every `<PLACEHOLDER>`. Strip the `>` operator-note lines before use.
> Copy everything between the BEGIN/END markers as the iteration brief.

---

```
=== BEGIN ITERATION BRIEF ===

You are running ONE Andrej iteration. Do NOT guess a fix and re-run; gather
ground-truth signal, change exactly ONE variable, measure, keep-or-revert, log it.

## GOAL + METRIC + BUDGET (the three preconditions — all required)
GOAL:    <OBSERVABLE END STATE, e.g. "0 flaky failures / 20 fixed-seed runs">
METRIC:  <ONE SCALAR + direction, e.g. "failures_per_20_runs (min)">  BASELINE: <N>
BUDGET:  <FIXED unit per trial — ticks/steps/iterations/K-reruns; NOT wall-clock>

## 1. OBSERVE (ground truth, not intuition)
SIGNAL CHANNEL: <how you read the live system — a /state endpoint, a --metrics
       stream, a trace, a runtime probe. NOT "grep the log".>
- If the cause is UNCLEAR, your FIRST act is to INSTRUMENT the exact live code
  path (per-iteration index / state / inputs / return value), run ONCE, and READ
  the trace. Resolve the mechanism from FACT before hypothesizing. Then revert
  the instrumentation.
- REPRODUCE the failure first (this is your baseline). "Can't reproduce" is a
  finding — chase the nondeterminism; it has a cause.
- For facts about the running system, trust a RUNTIME PROBE over a static model.

## 2. ANALYZE (orient — don't act on a stale picture)
- Run the analyzer over the signal; identify the HOTSPOT/SINK (most-visited
  node), OSCILLATION (top A<->B bounce), and FINAL STATE.
- Write 1-2 FALSIFIABLE hypotheses for the hotspot (each predicts an observable
  the next experiment can confirm or kill). Few, not a shotgun.
TOP HYPOTHESIS THIS ITERATION: <ONE falsifiable cause + its predicted observable>

## 3. ACT (one variable, fixed budget, keep-or-revert)
THE ONE CHANGE: <EXACTLY ONE variable you will change — no bundling>
- Run to the BUDGET above. Diff the scalar METRIC vs BASELINE.
- Improved past <THRESHOLD> → KEEP (git commit). Worse/same → REVERT
  (git revert / git checkout -- .).
- PROVE DETERMINISM: run twice at the SAME budget; show two byte-identical output
  hashes. Divergence is NEVER "flaky" — it's a real cause (wall-clock branch,
  code change, shared state). Hunt it.
- VERIFY BEFORE CLAIM: read and PASTE the actual end-state artifact (the flag /
  exit code / metric readout / the two equal hashes). No evidence line = not done.
- APPEND the trial to the ledger: {change, metric_before→after, kept?, hypothesis
  tested, evidence, commit}.

## ESCALATION (after the 2nd failed attempt on the SAME wall — don't start a 3rd)
STOP serial tweaking. Climb the ladder: read the source/spec → web-search how
others solved it → check a reference implementation → fan out ONE experiment per
distinct hypothesis from a common checkpoint, then merge the winner. Note which
rung you climbed and the outcome in the ledger.

## REPORT (return exactly this)
OBSERVED:   <the hotspot/sink + final state you measured>
HYPOTHESIS: <the one you tested + confirmed | killed>
CHANGE:     <the one variable changed>
METRIC:     <before → after> | KEPT: <yes/no> | DETERMINISM: <hashes equal? y/n>
EVIDENCE:   <the end-state artifact line proving GOAL progress>
COMMIT:     <sha, or "reverted">
NEXT:       <the next hypothesis OR "goal met" OR "escalate: <rung>">

=== END ITERATION BRIEF ===
```

---

## Filled example (a perf-tuning iteration)

```
=== BEGIN ITERATION BRIEF ===

You are running ONE Andrej iteration. Do NOT guess a fix and re-run; gather
ground-truth signal, change exactly ONE variable, measure, keep-or-revert, log it.

## GOAL + METRIC + BUDGET
GOAL:    p99 latency of /checkout under 200ms at fixed load.
METRIC:  p99_ms (min)   BASELINE: 340
BUDGET:  one fixed benchmark — 100k requests at a fixed RPS and seed.

## 1. OBSERVE
SIGNAL CHANNEL: continuous profiler flamegraph + the benchmark's latency
       histogram JSON; live /metrics endpoint scraped each run.
- Cause unclear, so first run was INSTRUMENT-ONLY: a span around each downstream
  call. Read the trace: 70% of p99 is in a synchronous inventory lookup inside
  the request path. Mechanism is fact now, not a guess.
- Reproduced: p99 = 340ms over 100k requests (baseline confirmed).

## 2. ANALYZE
- Analyzer over the histogram + spans: HOTSPOT = inventory-lookup span (longest);
  no oscillation; FINAL p99 = 340ms.
TOP HYPOTHESIS: the inventory lookup is an uncached synchronous call per request;
       caching it for the request's lifetime should drop p99 — if it's the cause,
       p99 falls and the inventory span shrinks in the flamegraph.

## 3. ACT
THE ONE CHANGE: add a request-scoped cache around the inventory lookup (ONLY that;
       not the parallel DB-pool change I also want — that's a separate trial).
- Ran the fixed 100k-request benchmark. p99 340 → 150ms (beat the 200ms goal).
- KEEP → git commit. Determinism: two benchmark runs at the same seed produced
  histogram hashes 7c1f.. == 7c1f.. (equal).
- VERIFY: pasted p99=150ms from the histogram JSON + the two equal hashes — not
  "feels faster".
- Appended trial to the ledger.

## REPORT
OBSERVED:   inventory-lookup span = 70% of p99; baseline p99 340ms.
HYPOTHESIS: uncached synchronous inventory lookup — CONFIRMED.
CHANGE:     request-scoped cache around the inventory lookup (one variable).
METRIC:     340 → 150 ms | KEPT: yes | DETERMINISM: hashes equal? y
EVIDENCE:   histogram p99=150ms; hashes 7c1f..==7c1f..
COMMIT:     b3d9a01
NEXT:       goal met (p99 < 200ms); DB-pool change deferred to a separate trial.

=== END ITERATION BRIEF ===
```
