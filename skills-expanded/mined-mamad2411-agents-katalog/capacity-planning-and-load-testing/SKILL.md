---
name: capacity-planning-and-load-testing
description: >
  Guides demand forecasting and load/stress/soak testing methodology
  (using tools such as k6, Locust, or JMeter) to find a system's real
  bottleneck — CPU, memory, a connection pool, or a downstream
  dependency — before production traffic finds it, and to set
  autoscaling/capacity triggers from actual test evidence rather than
  guesses. Use when a user asks to "capacity plan for an upcoming
  launch/event", "write a load test", "find out what breaks first under
  load", "our load tests pass but production still falls over", or "set
  our autoscaling thresholds correctly."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: site-reliability-engineering
  maturity: stable
---

# Capacity Planning and Load Testing

## Purpose

A system that "should" handle expected peak traffic is a hypothesis, not
a fact, until it's been tested against realistic load — and the whole
point of load testing is to find the actual bottleneck (which is very
often not where anyone assumed) before real users do. A load test that
only exercises the application tier while the database connection pool,
a downstream dependency's rate limit, or a fixed-size thread pool is the
real ceiling produces false confidence: the app tier looks fine at 2x
scale while the system as a whole falls over well before that. This
skill covers forecasting demand, choosing the right test type (load,
stress, soak) for the question being asked, instrumenting the *whole*
request path during a test (not just app-tier CPU/memory) so the real
bottleneck is found instead of assumed, and turning test results into
concrete, evidence-based autoscaling and capacity triggers.

## When to use

- Validating capacity before a known high-traffic event (product launch,
  marketing campaign, seasonal peak).
- Setting or revisiting autoscaling thresholds (HPA target metrics,
  connection pool sizes, thread pool limits) that were previously set by
  guesswork or copied defaults.
- "It works fine in staging but falls over in production under real
  traffic" — a strong sign the test never found the real bottleneck.
- Investigating whether a target SLO (see
  [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md))
  is actually achievable given current architecture and expected peak
  demand.
- Routine (e.g. quarterly) capacity review as traffic patterns and code
  change over time.

## Prerequisites & environment

- A load-testing tool: **k6** (scriptable in JavaScript, good CI
  integration, used for the examples below), **Locust** (Python,
  distributed load generation, good for complex user-behavior
  simulation), or **JMeter** (GUI/XML-based, long-established, strong
  protocol support) — any of the three is a reasonable choice; pick based
  on team language familiarity and whether distributed load generation
  is needed.
- A test environment that is either isolated from production or has
  explicit safeguards if it must touch shared/production infrastructure
  (see the warning in step 7) — running an uncontrolled stress test
  directly against production is a destructive action, not a shortcut.
- Historical traffic data (requests/sec over time, growth rate,
  known upcoming events) to forecast a realistic target peak.
- Monitoring across the *entire* request path — app tier, database
  (including connection pool utilization), cache, message queue, and any
  downstream/third-party dependency — available during the test run; see
  [Prometheus and Grafana monitoring stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  for how this is typically wired.
- Stakeholder awareness/scheduling for any test run that could affect
  shared staging capacity or, if unavoidable, production.

## Step-by-step guidance

1. **Forecast demand.** Pull historical peak RPS and month-over-month or
   year-over-year growth rate; fold in known upcoming events (a
   marketing push, a seasonal peak). Set a target test peak with a
   safety margin above the forecast — commonly 1.5-2x the expected real
   peak — rather than testing to exactly the forecast number.

2. **Choose the right test type(s)** — they answer different questions:
   - **Load test:** sustained traffic at expected peak, to confirm the
     system handles *normal* peak without degradation.
   - **Stress test:** traffic ramped past expected peak until something
     breaks, to find the actual ceiling and what breaks first.
   - **Soak test:** moderate, sustained load held for hours (often
     6-24h+), to catch problems that only appear over time — memory
     leaks, connection/file-descriptor exhaustion, log-disk fill —
     which a short test can never reveal.

3. **Write the test script.** k6 example combining a load stage and a
   stress ramp:
   ```javascript
   import http from 'k6/http';
   import { check, sleep } from 'k6';

   export const options = {
     scenarios: {
       load_test: {
         executor: 'ramping-vus',
         startVUs: 0,
         stages: [
           { duration: '2m', target: 200 },   // ramp to expected peak
           { duration: '10m', target: 200 },  // hold at peak
           { duration: '2m', target: 0 },
         ],
       },
     },
     thresholds: {
       http_req_failed: ['rate<0.01'],       // fail test if error rate > 1%
       http_req_duration: ['p(99)<300'],      // fail test if p99 > 300ms
     },
   };

   export default function () {
     const res = http.post('https://staging.example.internal/api/checkout', JSON.stringify({
       cart_id: `cart-${__VU}-${__ITER}`,
     }), { headers: { 'Content-Type': 'application/json' } });
     check(res, { 'status is 200': (r) => r.status === 200 });
     sleep(1);
   }
   ```
   For a stress test, replace the `stages` with a ramp that keeps
   increasing (`{ duration: '5m', target: 400 }`, `600`, `800`, ...)
   until thresholds start failing, to find the ceiling. Locust expresses
   the same idea as a `HttpUser` class with `@task` methods and a
   `--users`/`--spawn-rate` ramp; JMeter expresses it as a Thread Group
   with a ramp-up period.

4. **Instrument the whole path during the run, not just the app tier.**
   Watch, at minimum: app CPU/memory, **database connection pool
   utilization** (active vs. max connections), database CPU/IOPS, cache
   hit rate, message queue depth, and downstream/third-party dependency
   latency and error rate. A test that only graphs app-tier CPU will
   report "the app was only at 45% CPU" while the real ceiling — a
   fixed-size DB connection pool — was maxed out the whole time.

5. **Find the actual bottleneck systematically.** When the test's
   thresholds start failing (error rate/latency breach), check saturation
   signals in order rather than assuming it's the app tier: app CPU/
   memory → database connections/CPU → connection pool max setting →
   downstream dependency rate limits/latency. The bottleneck is whichever
   resource hits its ceiling *first* as load increases — it is very often
   a fixed pool size or a downstream rate limit, not raw app compute.

6. **Derive scaling triggers from the evidence**, not from defaults:
   if p99 latency breaches SLO once app CPU crosses 70%, set the HPA
   target below that (e.g. 60%) to leave headroom for scale-up lag; if
   the test shows the DB connection pool saturating at 300 concurrent
   app replicas, either cap `maxReplicas` at a safe value, increase the
   pool/add a read replica, or scale on a custom metric (e.g.
   requests-in-flight) that reflects the real constraint instead of CPU.

7. **Respect safety boundaries around where the test runs.**
   > **Warning:** Never run an uncapped stress or soak test against
   > production without an explicit plan — it can itself cause the exact
   > outage it was meant to prevent. If a test must touch production or
   > shared infrastructure: get stakeholder sign-off, schedule off-peak,
   > cap the request rate below the threshold that would cause
   > customer-visible impact, and have an abort/kill-switch and rollback
   > path ready before starting (the traffic-shifting/rollback mechanics
   > from
   > [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)
   > are a reasonable abort mechanism). Prefer an isolated,
   > production-topology-mirroring environment whenever the question can
   > be answered there.

8. **Re-run periodically.** Capacity assumptions decay as code and
   traffic patterns change — re-run before major events and on a fixed
   cadence (e.g. quarterly), and feed results into the pre-production
   gates in
   [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md)
   and the canary-analysis thresholds in
   [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md).

## Best practices

- Test with production-like data volume and cardinality — an empty or
  tiny test database gives artificially fast query times and hides
  index/query-plan problems that only appear at real data scale.
- Derive the test's traffic *mix* (ratio of reads/writes, which
  endpoints, payload sizes) from real production traffic (APM/access
  logs), not a synthetic guess — a GET-heavy synthetic test against a
  write-heavy checkout flow tells you almost nothing useful.
- Ramp gradually and hold at a plateau rather than spiking instantly —
  steady-state saturation behavior (the thing you actually care about)
  only shows up after a hold period, not during the ramp itself.
- Correlate every test run with distributed traces/APM to identify the
  slowest call in the request path, not just the aggregate pass/fail.
- Always run a soak test in addition to a short peak-load test — many of
  the worst production incidents (memory leaks, descriptor exhaustion)
  only manifest after hours of sustained load.
- Treat load-test-derived capacity numbers as an input to cost/FinOps
  conversations too — a validated capacity ceiling should inform reserved
  capacity purchases, not just autoscaling config.

## Common pitfalls

- **Symptom:** The load test passes cleanly at 2x expected peak with app
  CPU never exceeding 50%, but production falls over well below that
  traffic level with 5xx errors.
  **Fix:** The test likely stubbed or mocked the database/downstream
  dependencies, so it never touched the real connection pool or
  rate-limited API. Run tests against a production-like DB topology and
  pool configuration, and monitor pool utilization as a first-class
  saturation signal, not just app CPU/memory.

- **Symptom:** The test traffic profile is pure read-heavy GETs, but the
  real workload (checkout, payment) is write-heavy with transactional
  locking — the test result has no relationship to real behavior.
  **Fix:** Build test scenarios from actual production traffic
  mix/user-journey data (APM or access logs), not a generic synthetic
  guess at "typical" traffic.

- **Symptom:** A stress test run directly against production, with no
  rate cap and no abort plan, itself causes a customer-facing outage.
  **Fix:** This is exactly the destructive-action risk called out in
  step 7 — run in an isolated environment first; if production testing
  is truly necessary, cap the rate below customer-impact thresholds,
  schedule off-peak with stakeholder sign-off, and have a kill switch/
  rollback ready before starting, never as an afterthought.

- **Symptom:** A short load test passes every time, but a slow memory
  leak or a filled disk from verbose logging only surfaces in production
  after several hours of real traffic.
  **Fix:** No soak test was run. Add a multi-hour (6-24h+) soak test at
  moderate sustained load alongside the shorter peak-load test — this is
  the only test type designed to catch time-dependent degradation.

- **Symptom:** Autoscaling is configured with the default 70% CPU target
  "because that's what the docs suggested," with no test evidence behind
  it, and the service still degrades under real peak load.
  **Fix:** Derive the scaling trigger directly from where the test
  showed the SLI actually breaching (step 6), with margin for scale-up
  lag — not from a generic default.

## Worked example

**Scenario:** `checkout-service` capacity validation ahead of a major
seasonal sales event.

1. **Forecast:** last year's peak was 2,000 RPS; marketing expects 2x
   growth this year; target test peak set to 4,000 RPS (2x the
   forecast, i.e. 4x last year's observed peak, for safety margin).
2. **Load test:** the k6 script from step 3 ramped to 4,000 RPS and held
   for 10 minutes — passed cleanly, error rate <0.1%, p99 latency 210ms.
3. **Stress test:** ramp continued past 4,000 RPS; at 5,200 RPS, error
   rate crossed the 1% threshold and p99 latency spiked past 800ms.
   Checking saturation signals in order: app CPU was only at 45%
   (not the bottleneck); the database connection pool (fixed at 200
   connections) was pegged at 100% utilization — **the real bottleneck
   was the DB connection pool, not application compute.**
4. **Soak test:** 3,000 RPS held for 8 hours surfaced a slow memory leak
   in a caching client library, invisible in the shorter tests, ticketed
   and fixed before the event.
5. **Scaling triggers set from evidence:** HPA switched from a CPU-based
   target to a custom metric (`requests_in_flight`) that actually
   correlates with the real bottleneck; the DB connection pool increased
   from 200 to 350 and a read replica added for reporting queries to
   free up pool headroom on the primary; `maxReplicas` on the app
   deployment capped at the value that keeps pool demand under the new
   350-connection ceiling.
6. Results are fed into the canary-analysis error-rate/latency
   thresholds in
   [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)
   for the event-day release, and into the pre-event gate in
   [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md).

## Cross-references

- [chaos-engineering-and-resilience-testing](../chaos-engineering-and-resilience-testing/SKILL.md) — load testing finds capacity ceilings under expected traffic; chaos experiments find failure-*handling* gaps under fault conditions — run both, they answer different questions.
- [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md) — capacity test results tell you whether a target SLO is realistically achievable under peak demand.
- [toil-reduction-and-operational-automation](../toil-reduction-and-operational-automation/SKILL.md) — recurring manual load-test runs are good candidates for scheduling into CI rather than repeating by hand.
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md) — canary analysis thresholds and rollback mechanics should be informed by, and can serve as an abort path during, load testing.
- [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md) — capacity validation is a natural pre-production gate ahead of major traffic events.
