---
name: load-testing-patterns
description: k6 script templates, load profiles, response time thresholds, SLO validation, and performance testing strategies. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When validating performance, capacity, or SLOs for APIs, workers, or infra. Pair with profiler, backend-dev, devops, verifier, load-tester agent.
---

# Load Testing Patterns (Grok Port)

k6 (and equivalents) for realistic load, stress, spike, and endurance testing. Focus on thresholds that map to SLOs, realistic profiles, and Grok integration (friction from "we passed unit tests but died at 200 rps", compound for reusable scripts, palace for "why we chose this profile for this service").

## Script Template (k6)
```js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // ramp-up
    { duration: '1m',  target: 200 },  // normal load
    { duration: '30s', target: 500 },  // spike
    { duration: '1m',  target: 200 },  // sustain
    { duration: '30s', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<250', 'p(99)<500'], // SLO
    errors: ['rate<0.01'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/health');
  check(res, { 'status 200': (r) => r.status === 200 });
  errorRate.add(res.status !== 200);
  sleep(1);
}
```

## Profiles
- Smoke: 1-5 VUs, 30-60s — sanity.
- Load: expected peak + 20-50%, duration matching peak window.
- Stress: 2-5x expected, find breaking point.
- Spike: sudden 10x for 1-2 min, test autoscaling + queueing.
- Endurance / Soak: 4-8h at 70-80% peak, catch memory leaks / connection exhaustion.

## Realistic Data & Think Time
- Use shared or per-VU data sets (CSV, generated).
- Sleep / think time between actions (0.5-2s for human-like; lower for API-only).
- Parameterize (user ids, product ids) from real traffic samples (anonymized).

## SLO Mapping
Thresholds should be derived from actual SLOs (p95 latency, error rate, availability). If the load test can't meet the SLO at expected load, the release is blocked or capacity must increase.

## Grok Integration (Production Contract)
- Primary: profiler + backend-dev + devops + verifier + load-tester (if present).
- Fire on_infra_change, on_api_feature, on_run_completion when new endpoints, caching changes, or infra scaling rules are introduced.
- Pre-Flight (mandatory for user-facing or high-throughput services): "Do we have a load test for the new critical path? What is the expected peak rps/qps? p95/p99 thresholds mapped to SLO? Spike + endurance covered? Autoscaling / queue backpressure tested? Failure mode under load (circuit breaker, graceful degradation)?"
- Ledger: every load test run on a release candidate or after major change, with task_id + profile + max VUs + p95/p99 + error rate + SLO pass/fail.
- Handoff: script location, run command, results (html or json), identified bottlenecks, capacity recommendation, rollback or scale-up plan.
- Friction + compound: every "unit tests green, load test at 300 rps killed the DB with N+1" or "spike caused queue to 10k messages and OOM" → compound to preflight "load test before merge" or shared k6 templates + bottleneck checklist.
- Palace: "Chose 3x spike + 30min endurance for checkout flow because Black Friday pattern showed 2.8x normal + long tail; rejected 10x because it would require over-provisioning we can't afford year-round".
- Claim-verification: Two-pass. Grep "k6" or "load test" or "p95" → read_file actual script + latest run report → "Threshold p(95)<250 exists at load/checkout.js:18 and last run (2026-06-02) reported p95=187ms at 500 VUs ✓VERIFIED". Never claim "meets SLO under load" without reading the script thresholds + actual numbers from a run.
- Pair with: backend-patterns, api-patterns, kubernetes-patterns (HPA), caching-patterns, test-enforcement, preflight, compound-learnings, memory-palace (store capacity decisions).

## When to Activate
- New public or high-traffic API, worker, or data path.
- Any change that affects latency or throughput (caching, DB index, new dependency).
- Before major releases or events with known traffic spikes (shipper + verifier).
- After incidents that looked like "worked in staging".
- Swarm Phase 2 (perf/backend) + Phase 3 (validate).

See .grok/skills/backend-patterns/SKILL.md, kubernetes-patterns, preflight, test-enforcement. Run load tests in CI (or nightly) against staging-like env with production-like data volume. Production Contract: ledger + handoff + preflight + friction capture for every perf validation.

If it hasn't been load tested at expected + margin, it will break in prod. The question is only "when" and "how loudly".
