---
name: perf-budget
description: Set, wire and enforce performance budgets in CI with real measured numbers and a gate that actually fails the build. Use before a launch, after a latency regression, when performance work keeps being given back, or when someone asks "is this fast enough" without a number to answer it. Produces budgets.json, a measured noise floor, and a failing gate you can demonstrate. Do not use to profile or to design a load test.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[--baseline] [--gate] [--service <name>]"
user-invocable: true
model: sonnet
effort: medium
metadata:
  foundry.vertical: quality
  foundry.io: "measurements -> budgets.json + CI gate + finding.v1"
license: Apache-2.0
---

# Performance budgets with a real gate

A budget is a number, a percentile, a workload, a measurement point and a **consequence**.
Missing any of the five and it is not a budget, it is a preference.

The deliverable is not a document. It is a CI job that fails, which you have watched fail.

## When not to use this

- You do not know where the time goes yet → attribute first (`performance-engineer`). A budget
  on an unprofiled system is a guess with a threshold attached.
- Frontend Core Web Vitals and bundle sizes → `foundry-dev:frontend-performance-engineer` owns
  those; this skill covers server-side and pipeline budgets.
- You need an SLO with an error budget and burn-rate alerts → `define-slo`. A performance budget
  gates CI; an SLO governs production. They are different instruments and conflating them
  produces alerts nobody can action.

## Step 1 — Choose what gets a budget

Budget the operations that a user waits on and the resources that run out. Do not budget
everything: an unmaintained budget that fails for unrelated reasons gets disabled within a
month, taking the useful ones with it.

Start with at most **5 endpoints** (the top 5 by request volume x user-facing latency) and
**3 resources** (the three closest to saturation).

```bash
# Top endpoints by volume from access logs - use reality, not intuition
awk '{print $7}' access.log | sed -E 's/[0-9]{2,}/{id}/g' | sort | uniq -c | sort -rn | head -20
```

## Step 2 — Measure the baseline before choosing the number

A budget set without a baseline is either trivially met or instantly red. Measure first, then
choose a number that is tighter than today only where there is evidence of user harm.

```bash
SESSION=${SESSION:-local}; OUT=.foundry/scratch/$SESSION/perf; mkdir -p "$OUT"
git rev-parse --short HEAD > "$OUT/build.txt"
```

Use the bundled probe. It is a zero-dependency open-model harness — Node ≥ 20, standard library
only — that fires at a **fixed arrival rate** rather than waiting for each response, so it does
not under-report the tail (coordinated omission). It discards the warm-up window itself and
exits 1 when the generator, not the system under test, was the bottleneck.

```bash
node ${CLAUDE_SKILL_DIR}/scripts/perf-probe.mjs "$URL" 200 90 \
  --warmup 30 --label "GET /orders/{id}" >> "$OUT/runs.jsonl"
```

One JSON line per run:

```json
{"label":"GET /orders/{id}","targetRps":200,"achievedRps":198.4,"errors":3,
 "errorRatio":0.00017,"p50Ms":21.4,"p95Ms":88.1,"p99Ms":142.7,"maxMs":410.2,
 "steadyStateSamples":17840,"warmupSeconds":30}
```

**Every metric name carries its unit** — `p50Ms`, `p95Ms`, `p99Ms`, `maxMs`, `errorRatio`.
Step 4 and the gate in Step 5 index those exact spellings; do not rename them and do not
hand-roll a second probe that emits a different set.

Load profile design (executor model, warm-up exclusion, data cardinality):
`references/load-profiles.md`. The ways a number comes out confidently false:
`references/measurement-pitfalls.md` — read it before quoting any percentile.

Rules for the baseline run, all mandatory:
- **Discard the warm-up.** Run 60 s, report the last 30 s. JIT, caches and pools all need it.
- **Report p50, p95, p99 and max together.** A lone p99 hides the shape; a mean hides everything.
- **Record the workload**: rps, duration, request mix, dataset size, cache state, build sha.
- **Repeat 5 times** and record the spread — that spread is your noise floor and it decides
  every threshold below.

## Step 3 — Write budgets.json

```json
{
  "version": 1,
  "measurementPoint": "application, server-side duration excluding client network",
  "workload": { "rps": 200, "durationSeconds": 300, "warmupSeconds": 60, "datasetRows": 5000000 },
  "noiseFloorPercent": 6.2,
  "budgets": [
    { "id": "orders-read",  "target": "GET /orders/{id}",  "metric": "p99Ms",      "budget": 300,  "baseline": 218, "severity": "error", "rationale": "checkout blocks on this read; 300 ms keeps the journey under 1 s", "owner": "orders-team" },
    { "id": "orders-write", "target": "POST /orders",      "metric": "p99Ms",      "budget": 800,  "baseline": 611, "severity": "error", "rationale": "user waits on the confirmation; 800 ms is the current shape plus noise floor", "owner": "orders-team" },
    { "id": "errors",       "target": "all",               "metric": "errorRatio", "budget": 0.001, "baseline": 0.0002, "severity": "error", "rationale": "5xx under load is the first symptom of saturation", "owner": "orders-team" },
    { "id": "queue-lag",    "target": "orders-consumer",   "metric": "oldestAgeSecondsP99", "budget": 60, "baseline": 12, "severity": "error", "rationale": "downstream fulfilment SLA is 5 min end to end", "owner": "fulfilment-team" },
    { "id": "pool",         "target": "db-pool",           "metric": "utilisationPercent",  "budget": 70, "baseline": 41, "severity": "warn", "rationale": "30% headroom absorbs a single-instance failover", "owner": "platform-team" }
  ]
}
```

`baseline` is mandatory and must come from step 2. A budget without a recorded baseline cannot
be reviewed, and cannot be ratcheted. `rationale` and `owner` are mandatory too — the gate
**fails a budget entry that has neither**, deliberately, because a number nobody can defend gets
renegotiated away the first time it goes red.

Default starting budgets when there is no requirement to inherit — state them as chosen, not as
laws:

| Metric | Budget | Note |
|---|---|---|
| Read endpoint | p99 ≤ 300 ms | server-side |
| Write endpoint | p99 ≤ 800 ms | server-side |
| Interactive journey, end to end | p95 ≤ 1 s | includes fan-out |
| Error ratio under load | ≤ 0.1% | 5xx and timeouts |
| Saturation of the scarcest resource at peak | ≤ 70% | leaves headroom for a surge |
| Async job lag | p99 ≤ 60 s | oldest unprocessed item |

## Step 4 — Set the regression threshold above the noise floor

This is the step that decides whether the gate survives. A threshold tighter than your noise
floor produces false failures, and a gate that cries wolf is removed within two sprints.

```
regression_threshold = max(10%, noise_floor x 1.5)
```

Measure the noise floor honestly — 5 runs of the same commit:

```bash
for i in 1 2 3 4 5; do node ${CLAUDE_SKILL_DIR}/scripts/perf-probe.mjs "$URL" 200 90 --warmup 30; done | \
node -e '
let rows=[];process.stdin.on("data",d=>rows.push(...d.toString().trim().split("\n")));
process.stdin.on("end",()=>{
  const runs=rows.filter(Boolean).map(r=>JSON.parse(r).p99Ms);
  if (runs.length!==5 || runs.some(v=>typeof v!=="number")) {
    console.error("noise floor: expected 5 numeric p99Ms values, got "+JSON.stringify(runs));
    process.exit(2);
  }
  const s=[...runs].sort((a,b)=>a-b), min=s[0], max=s[4], med=s[2];
  console.log(JSON.stringify({p99Runs:runs,medianMs:med,spreadPercent:+(100*(max-min)/med).toFixed(1)}));
});'
```

The field is `p99Ms`, not `p99` — the probe names every metric with its unit, and reading the
wrong key yields `null` silently rather than an error, which is why the snippet above refuses to
print a spread it could not compute.

Put the resulting `spreadPercent` in `budgets.json` as `noiseFloorPercent` and derive every
threshold from it. **The gate exits 2, not 1, when `noiseFloorPercent` is absent or not a
number**, so this step is a precondition for Step 6, not an optional refinement. If the spread
exceeds 20%, the environment is too noisy to gate on percentiles — gate on the error ratio and
throughput only, and file that as a `finding.v1`.

## Step 5 — Wire the gate

Two tiers, because they answer different questions:

| Tier | When | Duration | Fails on |
|---|---|---|---|
| Smoke | every PR | ≤ 120 s | any error; p95 above budget x (1 + threshold) |
| Full | nightly on main | ≥ 20 min | p95 regression > 10% or p99 regression > 15% vs the **7-day median**, or any absolute budget breach |

Compare against the **7-day median of previous runs**, never against the single previous run —
single-run comparison is noise-driven, and the team learns to re-run rather than investigate.

**Aggregate the probe lines into `result.json` first.** The probe emits one flat line per
target; the gate indexes `result["<target>"]["<metric>"]`, so a conversion step is required and
it is the step people forget:

```bash
node -e '
const fs = require("node:fs");
const runs = fs.readFileSync(process.argv[1], "utf8").trim().split("\n")
  .filter(Boolean).map(JSON.parse);
const out = {};
for (const r of runs) out[r.label] = { p50Ms: r.p50Ms, p95Ms: r.p95Ms, p99Ms: r.p99Ms, maxMs: r.maxMs };
out.all = { errorRatio: Math.max(...runs.map((r) => r.errorRatio ?? 0)) };
fs.writeFileSync("result.json", JSON.stringify(out, null, 2));
' "$OUT/runs.jsonl"
```

The `target` in each budget must equal the probe's `--label` exactly, and resource budgets
(`db-pool`, `orders-consumer`) come from your own metrics export merged into the same object —
the probe measures HTTP only. Keep every run: copy `result.json` to `history/<sha>.json` so the
7-day median has something to compare against.

Then run the bundled gate — zero dependencies, deterministic, no clock:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/perf-gate.mjs budgets.json result.json history/
```

It exits **0** on pass, **1** on a gate failure (absolute breach, regression beyond
`max(10%, noiseFloor x 1.5)` against the median of the last 7 runs, a missing metric, or a
budget with no `rationale`/`owner`) and **2** on a usage or input error (`budgets.json` with no
`budgets` array, or a `noiseFloorPercent` that is not a number). Add `--json` for a
machine-readable row per budget.

## Step 6 — Prove the gate fails

An untested gate is decoration. Before you call this done, make it go red on purpose:

```bash
node -e 'const fs=require("node:fs");const r=JSON.parse(fs.readFileSync("result.json","utf8"));
r["GET /orders/{id}"].p99Ms *= 3; fs.writeFileSync("result.sabotaged.json",JSON.stringify(r));'
node ${CLAUDE_SKILL_DIR}/scripts/perf-gate.mjs budgets.json result.sabotaged.json history/ ; echo "exit=$?"   # must be 1
```

`exit=2` here does not mean the gate works: it means the gate refused to run. The usual cause is
`noiseFloorPercent` still missing from `budgets.json` because Step 4 was skipped. Fix Step 4 and
re-run; do not record a 2 as the sabotage evidence.

Record the sabotage run's output as evidence. This is the single check that distinguishes a
working gate from a YAML file.

## Step 7 — Ratchet

Every confirmed improvement lowers the budget **in the same change**, so the win cannot be
quietly given back. Budgets go down, never up, unless a written trade-off is recorded in the
finding (a feature genuinely costs latency and the product owner accepted it, by name).

## Exit criteria

1. `budgets.json` exists with ≤ 8 budgets, each carrying metric, percentile, budget, measured
   `baseline`, and a stated `measurementPoint` and `workload`.
2. `noiseFloorPercent` is measured from 5 same-commit runs and every threshold derives from it.
3. The PR smoke gate runs in ≤ 120 s and fails the build on breach.
4. The nightly gate compares against a 7-day median with history retained per commit sha.
5. The sabotage run exits 1 and its output is recorded.
6. Percentiles are computed from a full sample or merged histograms — never by averaging
   per-instance percentiles. State which.
7. The load generator uses an open model (fixed arrival rate), or the deviation is written down.
8. Every budget breach found during setup is filed as a `finding.v1` with a
   `kind: "measurement"` evidence item.

## Degradation

- **No CI** → ship `budgets.json` plus the two scripts and a documented manual command; every
  gate-related exit criterion is reported unmet, not waived.
- **Shared/noisy environment** → if `spreadPercent > 20`, gate on error ratio and throughput
  only, keep latency as a tracked-but-not-gating metric, and file a `high` finding on the
  environment. Do not tighten thresholds to compensate; that inverts the problem.
- **No access logs** → the endpoint ranking cannot come from reality. Ask; if unavailable, state
  the assumed mix in `budgets.json` under `workload.assumed: true` and cap confidence.
- **An existing load tool is present** (detect it, do not assume a version) → use it instead of
  the probe above and keep the gate script; the gate is the durable part.
- **`superpowers` installed** → use `superpowers:verification-before-completion` before
  declaring the gate working, and `superpowers:systematic-debugging` when a regression's source
  is not obvious after one bisect. If absent, use
  `${CLAUDE_PLUGIN_ROOT}/references/tdd-fallback.md`.

## Deliberately not covered

Profiling and attribution, capacity modelling, soak and spike design (all
`performance-engineer`); Core Web Vitals and bundle budgets (`foundry-dev`); SLOs, error budgets
and burn-rate alerts (`define-slo`); infrastructure cost optimisation.

## Bundled assets

- `scripts/perf-probe.mjs` — the open-model probe used in Step 2.
  `node ${CLAUDE_SKILL_DIR}/scripts/perf-probe.mjs <url> <rps> <seconds> [--warmup 10] [--label "GET /orders/{id}"]`
  Emits one JSON line, metrics named with their unit (`p50Ms`, `p95Ms`, `p99Ms`, `maxMs`,
  `errorRatio`). Exits 1 when the generator, not the system under test, was the
  bottleneck (achieved rate below 95% of target) — that result must never be quoted.
- `scripts/perf-gate.mjs` — the gate used in Step 5 and Step 6.
  `node ${CLAUDE_SKILL_DIR}/scripts/perf-gate.mjs budgets.json result.json history/`
  Fails on an absolute budget breach or a regression beyond `max(10%, noiseFloor x 1.5)`
  against the median of the last 7 runs. Also fails a budget entry that has no rationale or
  no owner, and refuses to gate percentiles when the noise floor exceeds 20%.
- `references/load-profiles.md` — load, stress, soak and spike design: what each answers,
  hold durations, pass conditions, and the data-cardinality rules that decide whether the
  numbers transfer.
- `references/measurement-pitfalls.md` — the ten ways a performance number looks
  authoritative and is wrong.
