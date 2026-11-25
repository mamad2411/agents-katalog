---
name: load-test
description: Design and run a load / stress / spike / soak campaign against an SLA on a prod-parity env, then interpret it — throughput, latency percentiles, breakpoint/knee, saturation — and return a PASS/FAIL verdict + headroom. Distinct from profile-endpoint (diagnoses ONE slow subject) and capacity-planner (analytical estimation); this is the empirical whole-system validation.
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# load-test

Design a load campaign against an SLA, drive it on a prod-parity env, read the result: throughput, latency percentiles, the breakpoint, the saturated resource. Ship a verdict, not a vibe.

## Premise

An SLA with no load test behind it is a promise no one has kept. This skill owns the campaign that either keeps it or breaks it — and the number that proves which.

**Cite-or-halt.** Every capacity claim cites the run config (tool, model, stages, rate, duration, env) AND the measured percentile / throughput it rests on. "It should handle the load" is a vibe; `p99 = 780ms at 4.2k rps with 0.3% errors on the staging fleet` is a finding. A single-VU "quick load" number quoted as capacity is the failure mode this skill exists to kill — one virtual user in a loop measures round-trip latency of an idle system, not what happens at peak.

**Boundary — `profile-endpoint` (sibling skill).** `profile-endpoint` diagnoses ONE slow subject under quick load — it points the flamegraph + slow-query log at a single endpoint and asks *where does the time go here*. `load-test` designs a CAMPAIGN validating whole-system throughput and headroom against an SLA — many paths, realistic mix, ramp to breakpoint, asks *does the system meet the SLA and where does it fall over*. Profiling explains a bottleneck; this skill finds and gates on it. When a campaign exposes a knee, hand the subject at the knee to `profile-endpoint` for the root cause.

**Boundary — `capacity-planner` (distributed-systems pack agent).** `capacity-planner` does ANALYTICAL back-of-envelope estimation — Little's Law, `peak QPS × payload`, single-node ceilings — proving on paper whether a design *should* fit before it's built. `load-test` does EMPIRICAL validation — it drives real traffic at the real system and measures what actually happens. They are complementary, not overlapping: the planner predicts the breakpoint, this skill confirms or refutes it against reality. A prediction that was never load-tested is a hope; a load test with no capacity model is a number with no expected value to compare against. Run the planner first for the target, then this skill to validate it.

## When to run

- Before a **launch**, a **capacity change** (new region, bigger fleet, autoscale retune), or a **big feature** on a hot path.
- To **validate an SLA/SLO** — you have a written `p99 < X at Y rps with <Z% errors` and need to prove or break it.
- After a suspected capacity regression, to re-establish the breakpoint.
- NOT on every CI run. A real load test needs a **prod-parity environment** (same instance sizes, same DB tier, realistic data volume, representative topology) and minutes of sustained traffic — it does not belong in the per-commit gate. A tiny smoke-load in CI is fine as a canary; do not mistake it for the campaign.

## Test taxonomy

Pick the campaign type by the question you need answered. Each has a goal and an explicit pass/fail.

| Type | Question it answers | Profile | Pass / fail |
|---|---|---|---|
| **Load** | Does it meet the SLA at *expected peak*? | Hold at target rps for a sustained window | PASS = p99 under SLA at target rps with errors < budget |
| **Stress** | *Beyond* peak, where does it break? | Ramp past peak until SLA violates or errors spike | Locate the rps where p99 or error-rate crosses the line |
| **Spike** | Does it survive a *sudden surge* and recover? | Jump from baseline to N× instantly, hold, drop | PASS = absorbs the spike and returns to baseline latency within the recovery window (no lingering queue) |
| **Soak / endurance** | Does it degrade over *hours*? | Hold moderate load for hours | PASS = flat latency + flat memory + flat conn-count; leak/creep = fail |
| **Breakpoint / capacity** | Where is the *knee*? | Slow ramp to find where latency turns non-linear | Report the knee (max sustainable rps) + the resource that binds there |

Load answers "are we safe at peak"; breakpoint answers "how much headroom past peak". Run both before a launch — the gap between them is your margin.

## Adapt to the codebase

Drive the project's existing load tool; do not import a new one for the campaign. Detect it (repo `load/`, `k6/`, `*.jmx`, `locustfile.py`, `*.scala`, `artillery.yml`, CI perf stage), then match the campaign to what the tool expresses.

| Tool | Scripting model | Percentile reporting | Ramp / stages | Open-model support |
|---|---|---|---|---|
| **k6** | JS scenarios | p90/p95/p99 in summary + thresholds | `stages` (ramping-vus) | `ramping-arrival-rate` / `constant-arrival-rate` |
| **Gatling** | Scala/Java DSL | full percentile HTML report | `rampUsers` / `during` | `constantUsersPerSec` / `rampUsersPerSec` |
| **Locust** | Python tasks | p50…p99 web UI + CSV | `LoadTestShape` / step-load | `constant_pacing` (approx); closed by default |
| **JMeter** | XML thread groups (GUI/CLI) | Aggregate + percentiles listener | thread-group ramp-up | Throughput Shaping Timer (arrival-rate approx) |
| **Artillery** | YAML phases | p95/p99 in report | `phases` with `arrivalRate` | native `arrivalRate` (open by default) |
| **`wrk` / `vegeta`** | HTTP microbench CLI | `wrk`: coarse; `vegeta`: full HDR percentiles | `wrk` fixed; `vegeta -rate` ramps | `vegeta` is open (`-rate`); `wrk` is closed (fixed conns) |
| **Cloud** (BlazeMeter / k6 Cloud / Gatling Enterprise) | wraps the above | dashboards + trends | distributed geo-load | inherits the underlying engine's model |

`wrk`/`vegeta` are for a fast HTTP microbench of one route; k6 / Gatling / Locust / Artillery for a multi-scenario campaign with a realistic mix. Whatever the tool, the report MUST expose p95/p99 and per-stage throughput — a tool that only prints an average cannot gate an SLA.

## Procedure / methodology

1. **Model the workload from prod traffic shape** — a realistic **request mix** (weight each endpoint by its real share), **think-time** between a user's actions, and the **arrival pattern** (diurnal, bursty) taken from access logs / APM, not invented. A hammer loop hitting one route at zero think-time tests that route's ceiling, not your system's behaviour.
2. **Establish env parity** — run against a prod-like environment: same instance class, same DB tier + connection limits, realistic data volume, representative caches/queues. Load-testing a laptop (or empty tables) is worthless — the numbers describe the laptop. Record the env in the run config so the result is interpretable.
3. **Define the SLA gate up front** — write it before the run: `PASS = p99 < X ms at Y rps with < Z% errors`. A gate defined after seeing the numbers is not a gate.
4. **Warm up, then measure** — discard an initial low-load burst so JIT, connection pools, and caches reach steady state; only the post-warm-up window counts (mirrors `performance-principles`: warm-up + variance + p50/p95/p99).
5. **Choose the load model — open vs closed (the critical call).**
   - **Closed model** (fixed VUs): N virtual users each fire, wait for the response, then fire again. Throughput is *bottlenecked by the system* — when it slows, VUs pile up waiting and offered load automatically drops. Good for modelling a fixed connection pool.
   - **Open model** (arrival rate): requests arrive at Y/sec **regardless** of whether prior ones finished — like real internet traffic. When the system slows, the queue grows and latency reveals the true pain.
   - For an SLA gate, prefer the **open / arrival-rate** model. A closed model masks saturation (see gotchas: coordinated omission) and answers a different question.
6. **Ramp in stages** — step or ramp the rate (e.g. 25% → 50% → 100% → 150% of target), holding each stage long enough for a stable percentile read.
7. **Measure the full vector per stage** — p50 / p95 / p99 latency, throughput (rps), error-rate, AND server-side **saturation**: CPU, memory, connection-pool utilisation, DB connections / lock waits, queue depth. Latency alone tells you *that* it hurt; saturation tells you *what* ran out.
8. **Find the breakpoint (the knee)** — the rps where latency stops rising linearly and turns vertical (or errors cross the budget). Below the knee is capacity; the knee itself is the ceiling; above it is collapse. Name the resource saturated at the knee — that is the binding constraint.
9. **Compute headroom** — `(breakpoint rps − expected peak rps) / expected peak rps`. This is the margin the launch has before it needs more capacity.

## Output

A literal report. Every claim traces to the run config and a measured number.

```
## Load campaign — <system / release>  ·  <load|stress|spike|soak|breakpoint>

### Run config
Tool: k6 0.5x · model: ramping-arrival-rate (OPEN) · env: staging (prod-parity: 3× c5.xlarge, db.r6g.large, 8M-row dataset)
Workload: prod mix (browse 60% / search 25% / checkout 15%), think-time 3–8s, warm-up 60s discarded
Stages: 1k → 2k → 4k → 6k rps, 5m each

### SLA gate
PASS = p99 < 500ms at 4000 rps with < 0.5% errors  →  RESULT: PASS

### Per-stage results
| Stage (rps) | p50 | p95 | p99 | throughput | error-rate | saturation |
|---|---|---|---|---|---|---|
| 1000 | 40ms | 90ms  | 140ms | 1000 | 0.0%  | CPU 28%, pool 20% |
| 2000 | 55ms | 150ms | 240ms | 2000 | 0.0%  | CPU 51%, pool 44% |
| 4000 | 92ms | 310ms | 470ms | 3980 | 0.3%  | CPU 82%, pool 78% |  ← SLA target, PASS
| 6000 | 480ms| 2.1s  | 4.8s  | 4600 | 7.2%  | pool 100%, DB conns maxed |  ← past knee

### Breakpoint
Knee at ~4600 rps. Binding constraint: DB connection pool exhaustion (100% util, requests queue for a connection).
Above the knee, throughput plateaus at 4600 while latency runs away — classic saturation.

### Headroom
Expected peak 3000 rps · breakpoint ~4600 rps · headroom ≈ +53% over peak.

### Handoff (root cause is NOT this skill's job)
- Connection-pool saturation at the knee → @performance-optimizer (pool sizing / query time) + @caching-architect (offload reads).
- If the bottleneck is one endpoint → skill:profile-endpoint on that route for the flamegraph.
- If the model says it shouldn't bind yet → reconcile with @capacity-planner's ledger.

### Verdict: PASS — meets SLA at target with +53% headroom; connection pool binds first past the knee.
```

Closure verbs: **PASS / FAIL** the gate, **breakpoint** named with its bound resource, **headroom** quantified, **handoff** filed to the owner of the fix.

## False positives / gotchas

- **Coordinated omission (the fixed-VU trap)** — the term and the analysis are Gil Tene's ("How NOT to Measure Latency", the HdrHistogram work). A closed model hides latency under saturation: when the server stalls, VUs simply wait to send their *next* request, so the requests that *would* have been slow are never issued — the histogram omits exactly the pain you were measuring. Reported p99 looks fine while real users time out. Prefer the **open / arrival-rate** model for any SLA gate; if you must use closed, use a tool that corrects for coordinated omission.
- **Non-parity env.** Numbers from a laptop, a shared dev box, empty tables, or a cold cache describe that environment, not production. A test against a non-parity env is not a smaller version of the real result — it can be qualitatively wrong. Record parity in the run config or discard the result.
- **The client is the bottleneck.** If the **load generator** saturates first (its CPU pegged, its network NIC full, too few source ports, one underpowered box), you are measuring the generator, not the system — throughput plateaus but server CPU is idle. Check generator-side saturation every run; distribute the load across machines / use cloud generation when one box can't push the target rate.
- **One run ≠ signal.** A single campaign carries variance (noisy-neighbour VMs, cache warmth, background jobs). Repeat the run; report the median and the spread. A breakpoint seen once, unrepeated, is an anecdote — mirror `performance-principles`' variance discipline.
- **Averages lie.** A mean latency under budget can hide a p99 that blows it; always gate on the tail (p95/p99), never the mean.

## Halt conditions

- **Refuse a capacity claim with no run config + parity note.** "Handles the load" without tool, model, stages, rate, env, and the measured percentile is not a result — halt and demand the run.
- **Single-VU / quick-load numbers are not capacity.** A number from one virtual user, a hammer loop, or a non-parity box may not be presented as system capacity — halt and re-run the campaign under a realistic mix on a parity env.
- **No SLA gate defined before the run** — halt; define `p99 < X at Y rps with < Z% errors` first, or the run has no verdict to reach.
- **Closed model quoted as an SLA pass** — halt; re-run open / arrival-rate before certifying, or the pass may be coordinated-omission theatre.
- **Hand the ROOT CAUSE off, don't fix it here.** This skill owns the campaign and the verdict — it finds the knee and names the saturated resource. It does NOT fix the bottleneck: route the fix to `@performance-optimizer` / `@caching-architect` / the relevant pack, and route single-subject diagnosis to `skill:profile-endpoint`. A load-test PR that also rewrites the query has exceeded its mandate.

## Related

- `profile-endpoint.md` — boundary: it diagnoses ONE slow subject under quick load; this skill runs the whole-system campaign. Hand it the subject at the knee for the flamegraph + slow-query root cause.
- `@performance-optimizer` — owner of the fix once the binding resource is named (pool sizing, query time, index).
- `@caching-architect` — read-offload / cache-strategy fixes when the knee binds on read load.
- `@capacity-planner` *(distributed-systems pack, when co-installed)* — analytical complement: predicts the breakpoint on paper (Little's Law, peak QPS × payload) that this campaign empirically confirms or refutes. Run the planner first, then validate here. Absent that pack there is no ledger to reconcile the knee against: report the measured breakpoint alone and label the headroom `measured, unmodelled` rather than implying a prediction agreed with it.
