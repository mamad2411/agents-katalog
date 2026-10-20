---
name: load-stress-test
description: Designs and runs load, stress, soak, and spike tests against an HTTP/gRPC service using an open arrival-rate model — driving a realistic endpoint mix with think-time past the saturation knee and reporting latency percentiles, throughput ceiling, and breaking point against machine-checkable SLO thresholds.
when_to_use: Before a launch/scale event, for capacity planning, or to validate an SLO — when the question is sustained req/s, where p99 degrades, or whether the service survives a soak/spike. Distinct from performance-profiling (explains why one already-measured request is slow) and optimize-sql-query (tunes one query's plan); this skill finds the limit, those explain it.
---

## When to Use

Reach for this skill when the question is **"how much can it take, and where does it break"** — a capacity/SLO question, not a code question:

- "How many req/s can this hold before p99 blows past 500ms?"
- "Will checkout survive Black Friday / the launch spike?"
- "Find the breaking point — ramp until error rate crosses 1%."
- "Does it leak / degrade over an 8-hour soak at steady load?"
- "Validate the SLO: p95 < 300ms, p99 < 800ms, errors < 0.5% at 2k RPS."
- "Gate CI so a PR can't regress p95 by >10%."

NOT this skill:
- *Why* one endpoint is slow when you already know it is (flame graph, allocations) → performance-profiling
- A specific slow SQL query's plan/indexes → optimize-sql-query
- A prod incident already happening (this is a planned test, not a live outage) → incident-response-sre, or debug-root-cause for a reproducible failure
- Adding the metrics/traces you watch during the run → observability-instrument (a prerequisite, not this)
- Wiring the gate into the pipeline mechanics → cicd-pipeline-author (this defines the threshold; that plumbs it in)

## Steps

1. **Write the goal as numbers before touching a tool.** A test with no pass/fail line is just a graph. Fix four things:
   - **Objective + scenario** (drives the load shape):

     | Scenario | Question it answers | Shape | Duration |
     |---|---|---|---|
     | **Smoke** | Does the script even work? | 1–5 VUs | 1 min |
     | **Load** | Holds at *expected peak*? | ramp to target RPS, hold | 10–30 min |
     | **Stress** | Where's the knee / breaking point? | ramp **past** target until SLO breaks | until failure |
     | **Soak** | Leak/degradation over time? | steady moderate load | 2–8 hr |
     | **Spike** | Survives a sudden surge + recovers? | flat → instant 5–20×, then drop | 1–5 min spike |

   - **SLO thresholds** as concrete inequalities: e.g. `p95 < 300ms`, `p99 < 800ms`, `error_rate < 0.5%`, `throughput ≥ 2000 req/s`. These become the exit code.
   - **Target intensity** in **arrival rate (RPS)**, not just VUs — VU count without think-time is meaningless (see Common Errors). Derive VUs from Little's Law: `VUs ≈ target_RPS × (avg_response_time + think_time)`.
   - **Environment**: a prod-like staging box (same instance class, DB size, cache warm, autoscaling either off or explicitly in-scope). Never load-test prod blind.

2. **Model a realistic workload, not a hammer on one URL.** A single hot endpoint at 100% gives a fantasy number.
   - **Endpoint mix** weighted to real traffic (read from access logs / APM): e.g. 70% `GET /feed`, 20% `GET /item/:id`, 8% `POST /cart`, 2% `POST /checkout`.
   - **Think-time** between steps (`sleep(rand 1..3)`) so each VU models a user, not a tight loop.
   - **Parameterized + correlated data**: unique users/items per iteration from a CSV/SharedArray (no caching by accident); capture a token/ID from response N and feed request N+1 (login → use `access_token`; create order → reuse `order_id`).
   - **Auth**: log in once per VU and reuse the token; don't re-auth every iteration unless that's the scenario under test.

3. **Pick the tool by team + need, encode thresholds as exit-code gates.** Default to **k6** for code-first, CI-friendly tests — it has RPS-precise arrival-rate executors and native threshold gates, so it covers most cases. Reach for the others only for the listed reason:

   | Tool | Script lang | Reach for it when | Native threshold gate |
   |---|---|---|---|
   | **k6** (default) | JS | CI, scripted, RPS-precise (`constant-arrival-rate`) | `thresholds` → exit 99 on breach |
   | Locust | Python | dynamic per-user logic, Python shop | `--exit-code-on-error` + custom |
   | Gatling | Scala/Java DSL | JVM teams, rich HTML report | `assertions` → non-zero exit |
   | Artillery | YAML/JS | quick YAML scenarios, serverless | `ensure` plugin |
   | JMeter | XML/GUI | legacy/enterprise, protocol breadth | clunky; prefer above for CI |

   k6 with an **open model** (arrival rate — the correct way to fix RPS and dodge coordinated omission) and SLOs as code:

   ```js
   import http from 'k6/http';
   import { check, sleep } from 'k6';
   import { SharedArray } from 'k6/data';
   const users = new SharedArray('u', () => JSON.parse(open('./users.json')));

   export const options = {
     scenarios: {
       ramp_to_knee: {
         executor: 'ramping-arrival-rate',   // open model: fixed RPS, k6 adds VUs as needed
         startRate: 100, timeUnit: '1s',
         preAllocatedVUs: 200, maxVUs: 2000,
         stages: [
           { target: 500,  duration: '2m' },  // warm-up — exclude from SLO judgment
           { target: 2000, duration: '5m' },  // hold at target peak
           { target: 4000, duration: '5m' },  // push PAST to find the knee
         ],
       },
     },
     thresholds: {                            // breach → process exits non-zero → CI fails
       http_req_duration: ['p(95)<300', 'p(99)<800'],
       http_req_failed:   ['rate<0.005'],
       http_reqs:         ['rate>1800'],      // throughput floor
     },
   };
   export default function () {
     const u = users[Math.floor(Math.random() * users.length)];
     const r = http.get(`https://staging.internal/feed?u=${u.id}`);
     check(r, { 'status 200': (res) => res.status === 200 });
     sleep(Math.random() * 2 + 1);            // think-time 1–3s
   }
   ```
   Run: `k6 run --summary-trend-stats="avg,p(95),p(99),max" test.js`.

4. **Run staged, and watch the server while the client pushes.** Escalate; don't jump to max:
   1. **Smoke** (1–5 VUs) — fix the script/correlation before scaling.
   2. **Baseline** at low steady load — record reference percentiles.
   3. **Ramp to target** — confirm SLO holds at expected peak.
   4. **Push past** — keep ramping until a threshold breaks; the load just below that is the **breaking point / knee**.

   The client number alone is half the picture. Capture **server-side** metrics over the same window (Grafana/Prometheus/APM): CPU%, memory (RSS trend for soak), **DB/connection-pool saturation**, thread/worker queue depth, GC pauses, downstream latency. The first resource to hit ~100% (CPU, pool exhaustion, disk I/O, a downstream rate limit) **is the bottleneck** — that's the finding. Always confirm the **client isn't the bottleneck** (load-gen box CPU/network not saturated, file descriptors raised) before trusting a ceiling.

5. **Report the four numbers + the saturated resource, then gate.** A useful report states: **(a)** latency percentiles (p50/p95/p99/max) at target load, **(b)** sustained throughput ceiling (max RPS where SLO still holds), **(c)** breaking point (load where it broke + how — errors, timeouts, or latency cliff), **(d)** the saturated resource at that point. For soak, add the RSS/latency trend over time (flat = healthy; rising = leak). For CI: store the baseline summary, fail the build when p95/p99/error-rate regress beyond an allowed delta.

## Common Errors

- **Coordinated omission.** A closed-model loop that waits on each slow response stops *issuing* new requests during a stall, so the slowest requests are undercounted and p99 looks great. Fix: use an **open/arrival-rate model** (k6 `*-arrival-rate`, Gatling `constantUsersPerSec`, wrk2) that schedules requests on a fixed clock regardless of in-flight latency.
- **No warm-up.** First requests hit cold JIT, empty caches, unconnected pools, and cold autoscalers — folding them in poisons percentiles. Run a warm-up stage and **exclude it** from the SLO judgment window.
- **VUs as the target, no think-time.** "500 VUs" in a tight loop is an unrealistic, immeasurable arrival rate. Specify **RPS**; add think-time so a VU models a user. Convert via Little's Law.
- **Single-VU extrapolation.** "1 user got 50ms, so 1000 users = 50ms each" — ignores contention, queueing, and pool limits, the entire point of the test. Latency is non-linear past the knee; you must actually ramp.
- **Client is the bottleneck.** A maxed-out load-gen box (CPU, NIC, ephemeral ports, `ulimit -n`) caps *your* throughput, not the server's. Raise FD limits, distribute across machines (k6 cloud / multiple agents), and verify the generator is under ~70% before believing any ceiling.
- **Testing a non-prod-like env.** Tiny DB, no cache, debug logging, a shared box — numbers don't transfer. Match instance class, data volume, and config; disable verbose logging.
- **One endpoint at 100%.** Over-caches and misses cross-endpoint contention (shared pool, locks). Use a weighted mix from real traffic.
- **Reusing the same record every iteration.** One user ID hits a hot cache row and reports impossibly low latency. Parameterize from a dataset of unique keys.
- **Reporting only the average.** A 40ms mean can hide a 4s p99. Averages lie under load — always report **p95/p99/max**.
- **Load-testing production unannounced.** Real users, real bills, real pages. Use staging; if prod is mandatory, schedule it, cap blast radius, and tell the on-call.
- **Ignoring server metrics.** Client-only results tell you *that* it broke, never *why*. Without CPU/mem/pool/DB you can't name the bottleneck or fix it.

## Verify

1. **Threshold gate is real:** intentionally set an impossible threshold (`p(95)<1`) → the run **exits non-zero**. Proves the SLO is machine-checked, not eyeballed.
2. **Open model confirmed:** the actual issued RPS tracks the configured arrival rate even as latency rises (not throttled by in-flight count) — no coordinated omission.
3. **Warm-up excluded:** reported percentiles come from the steady window, and the first-stage cold numbers are visibly separated, not blended in.
4. **Breaking point is named with a cause:** report states "broke at ~N RPS — `http_req_failed` crossed 1% / p99 hit the cliff" **and** the saturated resource (e.g. "DB pool at 100%, CPU 95%"), not just a latency graph.
5. **Client wasn't the limiter:** load-gen CPU/network stayed below ~70% and FD limits weren't hit at the reported ceiling — otherwise the number is the generator's, not the service's.
6. **Realism holds:** endpoint mix ≈ production weights, data was parameterized (cache-hit ratio sane, not artificially 100%), think-time present.
7. **Soak (if run):** memory RSS and p95 are **flat** across the full duration — a rising slope is a leak/degradation finding, not a pass.
8. **Reproducible:** the script, dataset, env spec, and exact command are committed so the run can be replayed and CI-gated.

Done = the scenario ran on a prod-like env with an open arrival-rate model and excluded warm-up, every SLO threshold is enforced by a non-zero exit code, and the report states latency percentiles, the sustained throughput ceiling, the breaking point with its cause, and the saturated server-side resource — with the load generator proven not to be the bottleneck.
