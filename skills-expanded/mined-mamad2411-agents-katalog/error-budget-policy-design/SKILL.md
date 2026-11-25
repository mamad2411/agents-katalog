---
name: error-budget-policy-design
description: >
  Define SLO error budget policies with stakeholders for owned services: SLI
  selection, SLO targets, budget calculation, burn alerts, release freezes, and
  exception process. Use when error budget, SRE policy, SLO burn rate, or
  reliability vs feature velocity negotiations—not generic security scanning.
---

# Error Budget Policy Design

## Scope And Authorization

- **In scope:** Services your org operates and measures.
- **Out of scope:** Imposing SLOs on third-party systems you do not run (except vendor SLAs you consume).
- Policies need product + eng + SRE agreement—not a solo checkbox.
- Use production metrics you are allowed to access; redact customer identifiers.
- Pair with `observability-metrics-tracing` for instrumentation.

## When To Use

- Establishing or revising SLOs and what happens when budgets burn.
- Negotiating freeze vs ship decisions after incidents.
- Designing multi-window burn-rate alerts.
- Aligning platform reliability with feature roadmap.
- Post-incident: convert pain into policy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Metrics/traces instrumentation | `observability-metrics-tracing` |
| Envoy ejection tuning | `envoy-outlier-detection` |
| Feature flag kill switch | `feature-flag-kill-switch` |
| Security vuln SLAs | secure-sdlc / vuln management skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| SLI | User-centric (availability, latency, correctness) |
| SLO | Target over window (e.g. 99.9% / 30d) |
| Budget | 100% − SLO; consume on bad events |
| Policy | Actions at 50%/0% budget remaining |
| Alerts | Fast + slow burn rates (multi-window) |
| Exceptions | Written, time-bounded, owner |

## Workflow

### 1. Confirm stakeholders and success criteria

1. Service owners, product, on-call, exec sponsor.
2. Success: written policy approved; budgets visible; one practiced freeze decision.

### 2. Inventory user journeys and current metrics

1. Critical journeys (login, checkout, API write).
2. Existing dashboards; data quality gaps.
3. Historical 30/90 day availability and latency if available.

### 3. Choose SLIs

| Type | Example |
| --- | --- |
| Availability | Successful requests / total (exclude 4xx client if agreed) |
| Latency | % of requests faster than threshold |
| Quality | Correct job outcomes / total jobs |

1. Prefer metrics that match user pain over easy infra CPU.
2. Document inclusion/exclusion (maintenance, multi-tenant noise).

### 4. Set SLOs and compute budgets

```text
SLO: 99.9% availability over 30 days
Budget: 0.1% ≈ 43.2 minutes of full downtime
         or equivalent failed-request budget
```

1. Pick ambitious but achievable targets from baseline.
2. Separate SLOs for internal vs external APIs if needed.
3. Record measurement pipeline (PromQL/RUM) as source of truth.

### 5. Write the policy actions

| Budget remaining | Expected action |
| --- | --- |
| > 50% | Normal feature velocity |
| 25–50% | Reliability work prioritized; extra review on risky changes |
| < 25% | Feature freeze candidates; focus on toil/bug burn-down |
| Exhausted | Freeze non-critical releases; incident-style focus; exec notify |
| Exception | VP/director approval, expiry, risk accepted in writing |

1. Define **who** can declare freeze and unfreeze.
2. Tie to deploy tooling (require flag or change window).
3. Align with feature flags for progressive delivery under low budget.

### 6. Alerting (burn rates)

1. Fast burn: e.g. 2% budget in 1 hour → page.
2. Slow burn: e.g. budget path to exhaust in days → ticket.
3. Avoid alerts on budget already zero without recovery plan.
4. Dashboard: budget remaining, burn rate, top error contributors.

### 7. Verify and hand off

1. Tabletop: “budget exhausted Friday 4pm”—walk the freeze.
2. Simulate burn alert in staging/rules unit tests if possible.
3. Publish policy in eng handbook; review quarterly.
4. After major incidents, revisit SLI correctness.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| SLI | Checkout success rate | CPU < 80% as “SLO” |
| Policy | Clear freeze authority | “We’ll try harder” |
| Alerts | Multi-window burn | Page on every 5xx blip |
| Exceptions | Dated + owned | Silent permanent bypass |
| Culture | Budget drives decisions | Ignore red budget all quarter |

## Output Checklist

- [ ] Stakeholders named and policy approved
- [ ] SLIs/SLOs documented with measurement queries
- [ ] Budget math published
- [ ] Action tiers and freeze authority defined
- [ ] Burn alerts implemented
- [ ] Exception process documented
- [ ] Tabletop or real decision recorded
- [ ] Next review date set

## Rules

- Error budgets are product decisions, not only SRE vanity metrics.
- Do not set 100% SLOs.
- Protect measurement integrity (no gaming exclusions without review).
- Security incidents may override budget freezes—document interaction.
- Instrumentation gaps → observability skill first.
