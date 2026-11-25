---
name: canary-analysis-basics
description: >
  Canary analysis for owned releases: traffic fraction, metric selection, statistical
  comparison to baseline, automated promote/rollback gates, and bake time. Use when
  canary deploy analysis, Kayenta-style judges, progressive delivery metrics, or
  go/no-go on partial traffic — pair cutover mechanics with `blue-green-deploy-checklist`.
---

# Canary Analysis Basics

## Scope And Authorization

- **In scope:** Services and metrics stacks you operate.
- **Out of scope:** Injecting faults into customer environments without approval; scraping others’ metrics.
- Canaries still touch production users — start tiny and guard blast radius.
- Redact user identifiers in analysis notebooks.
- Pair with `blue-green-deploy-checklist`, feature flags, `code-quality-standards`.

## When To Use

- Progressive delivery: 1% → 5% → 25% → 100% with evidence gates.
- Automated analysis (Kayenta, custom judges, Flagger metric templates, Argo rollouts analysis).
- Comparing canary vs baseline (old version) on golden signals + business metrics.
- Reducing “eyeball dashboard” promote decisions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Blue/green hard swap checklist | `blue-green-deploy-checklist` |
| Chaos experiments | `chaos-engineering-basics` |
| Feature flag targeting only | `feature-flag-patterns` |
| CI build pipelines | `ci-cd-pipeline-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Element | Guidance |
| --- | --- |
| Baseline | Stable previous version, same traffic shape when possible |
| Canary | New version, small % or mirrored |
| Metrics | Latency, errors, saturation + **business** KPI |
| Analysis | Relative comparison, not absolute thresholds alone |
| Gate | Pass / fail / inconclusive → promote / abort / extend |
| Bake time | Enough samples for statistical power |

## Workflow

### 1. Confirm scope and success criteria

1. Service, SLOs, user cohorts, regions, change ticket.
2. Success: automated or checklist analysis that would catch last bad deploy class; rollback owner named.
3. Exclude canary from risky cohorts if needed (enterprise tenants).

### 2. Instrument versions

1. Every metric/log/trace must include `version` or `revision` label.
2. Traffic split mechanism: mesh weight, Ingress, Flagger, LB, feature flag.
3. Confirm canary and baseline receive **comparable** traffic (same region mix).

```promql
# Example: error ratio by version
sum(rate(http_requests_total{service="checkout",status=~"5.."}[5m])) by (version)
/
sum(rate(http_requests_total{service="checkout"}[5m])) by (version)
```

### 3. Select metrics and thresholds

| Class | Examples | Fail when |
| --- | --- | --- |
| Reliability | 5xx rate, success rate | Significant regression vs baseline |
| Latency | p95/p99 | Regression beyond margin |
| Saturation | queue lag, CPU | Unsustainable climb |
| Business | checkout convert, login success | Drop vs baseline |
| Custom | cache hit, dependency errors | Cross SLO |

1. Use **relative** checks: canary_error <= baseline_error * (1 + margin) + epsilon.
2. Avoid flaky low-traffic absolute thresholds as sole gate.
3. Record metric sources (Prometheus, Datadog, CloudWatch, Stackdriver).

### 4. Design analysis windows

```text
Step 1%:  bake 15–30m (or N requests minimum)
Step 5%:  bake ...
Step 25%: bake ...
Then full
```

1. Minimum request count before judge runs (statistical power).
2. Exclude deploy minute (cold start / JIT) if it skews.
3. Multi-region: analyze per region or ensure traffic share equal.

### 5. Automate judge (conceptual)

```yaml
# Flagger-like sketch
analysis:
  interval: 1m
  threshold: 5   # successful checks
  maxWeight: 50
  metrics:
    - name: error-rate
      thresholdRange: { max: 1 }  # or built-in templates comparing versions
    - name: p99-latency
      thresholdRange: { max: 500 }
```

**Kayenta-style:**

1. Baseline + canary queries over same lookback.
2. Mann-Whitney / classification → higher/lower/pass.
3. Critical metrics fail → automatic rollback.

### 6. Execute release

1. Deploy canary pods/instances alongside baseline.
2. Shift tiny weight; run analysis; publish report link in PR/ticket.
3. On **fail**: revert weight to 0, rollback canary, page owner.
4. On **inconclusive**: extend bake, do not blind promote.
5. On **pass**: next weight step; repeat until 100%; then scale down baseline.

### 7. Hand off

1. Store analysis reports with release version.
2. Tune metrics that false-failed (too sensitive) vs missed incidents (add business KPI).
3. Document manual override procedure with approval.
4. Apply `code-quality-standards` to analysis config as code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Compare | Canary vs baseline same window | Only vs historical week |
| Labels | version on all golden signals | Aggregate only |
| Traffic | Enough samples | Promote on 20 requests |
| Business | Include conversion | Only CPU |
| Fail | Auto abort | “Watch for an hour” without owner |
| Start | 1% protected | Jump 50% immediately |

## Output Checklist

- [ ] Version labels present on metrics
- [ ] Traffic split mechanism verified
- [ ] Metric list with margins documented
- [ ] Min sample / bake times set
- [ ] Automated or checklist judge defined
- [ ] Rollback path tested
- [ ] Analysis report retained per release
- [ ] Manual override policy written
- [ ] Post-release metric tuning notes
- [ ] Related deploy skill linked if hard cutover used

## Rules

- Never promote on gut feel when analysis fails without documented override.
- Comparable traffic is required for fair comparison.
- Start small; protect high-value tenants if needed.
- Inconclusive ≠ pass.
- Mechanics of dual environment swap → `blue-green-deploy-checklist`.
