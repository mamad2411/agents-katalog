---
name: performance-test-report
description: Author a stakeholder-grade performance test report — context, method, results, SLO verdict, bottlenecks, recommendations, and re-test plan. Use after each significant load/stress/spike/soak run.
source: self
date_added: 2026-05-01
---

# Performance Test Report

A perf report exists to drive a decision: ship / don't ship / fix and re-run. Anything that doesn't help that decision is noise. This skill defines a tight structure stakeholders can read in 5 minutes and engineers can act on in 30.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Format | Markdown in repo + linked dashboard; PDF export only when external |
| Audience | Eng leads, SRE, PM, exec sponsor |
| Length | 2 pages narrative + appendices |
| Sources | Load tool output (k6/Gatling), Grafana panels, traces, profilers |
| Repository | `perf/reports/<service>/<date>-<run-id>.md` |

## When to Use

- After load / stress / spike / soak runs against staging or pre-prod.
- Pre-launch readiness sign-off.
- Quarterly capacity review.
- Post-incident perf re-validation.

## Report Structure

```
# Perf Report — orders-api 2026-05-01 #r142

## TL;DR (3 lines)
Verdict: ✅ Pass against SLOs at 800 RPS. 1 medium finding (cache eviction climbs after 12h soak).
Recommendation: Ship; queue cache size tuning for next sprint.
Owner / sign-off: @perf-lead, @orders-tech-lead

## Context
- Goal:         Validate v3.14 RC1 meets SLOs at forecast peak (800 RPS) for 24h
- Service/SHA:  orders-api @ a1b2c3d
- Environment:  pre-prod, 12 × m6i.large, eu-west-1, JVM 21.0.6
- Test type:    Load (1h) + Soak (24h)
- Workload:     mix v4 (70/25/5 read/browse/write); 0.05–0.5s think; auth via per-VU bot accounts
- Datasets:     5,000 SKUs; 50k users; cache cold start

## Method
- Tool: k6 0.55, open model (`ramping-arrival-rate`)
- Shape: ramp 5m → steady 45m → ramp-down 5m
- Soak: constant 800 RPS × 24h
- Trace correlation: traceparent injected per request
- Repeat: N=3 medians on load; single 24h soak

## Results — SLO verdict
Endpoint                     p95 ms   p99 ms   Err %    SLO   Status
GET /products                  138      286     0.00   200/400/0.5  ✅
GET /products/:id              196      410     0.00   250/500/0.5  ✅
POST /checkout                 248      612     0.18   300/800/0.5  ✅
Throughput delivered: 797.4 RPS / 800 target

## Resource utilization (steady-state)
CPU p99 64% | Mem RSS 1.6GB | Heap used max 1.5GB | GC pause p99 41ms
DB query p99 18ms | DB CPU 38% | Cache hit 88%

## Findings
1. (MEDIUM) Cache eviction rate doubles after h12 of soak; hit-rate dips 88→81%.
   Evidence: redis_evicted_keys/sec graph; latency p99 +6%.
   Hypothesis: hot key set exceeds maxmemory.
   Recommendation: bump Redis from 4GB to 8GB OR adopt LFU + key-size profiling.
2. (LOW) tax-svc 3p call consumes 92% of rate-limit at peak.
   Recommendation: client-side burst smoothing OR raise quota.

## Risks not exercised
- Multi-region failover (out of scope)
- Black-Friday spike profile (next test r143)

## Re-test
- After fixes for finding #1; same workload v4; expected p99 reduction 5–10%
- Re-baseline post-merge

## Appendices
A. Dashboard: <Grafana link>
B. Raw artifacts: <S3 path>
C. Workload script hash: sha256:7f...
D. Run log + alert events
```

## Quality Bar Checklist (PR review)

- [ ] TL;DR fits in 3 lines and contains the verdict
- [ ] SLOs explicit; verdict per endpoint
- [ ] Open vs. closed model declared
- [ ] Steady-state windowed assertions (no ramp pollution)
- [ ] Findings ranked Critical/High/Med/Low with evidence + recommendation
- [ ] Cost & resource utilization reported
- [ ] Risks not exercised listed
- [ ] Re-test plan owned and dated
- [ ] Reproducibility: env, SHA, workload hash, dataset

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| 30-page report, no decision | Lead with TL;DR + verdict; appendices below |
| Averages and totals only | Tails (p95/p99) per endpoint |
| Charts without numbers | Tables drive decisions; charts illustrate |
| "All green" with no caveats | List risks not exercised |
| No reproducibility info | Pin env, SHA, workload hash |
| Findings without owners | Each finding has owner + ETA |
| Cost ignored | $/1k req or replica delta |
| Re-test forgotten | Re-test plan with trigger and expected delta |

## References

- Google SRE Workbook — *Practical SLOs*
- B. Gregg — *Systems Performance* 2e (analysis methodology)
- k6 reporting: <https://grafana.com/docs/k6/latest/results-output/>
- ISO/IEC/IEEE 29119-3 — Test report contents
- Atlassian — Engineering blog on perf reports
