---
name: sre-slo-engineer
description: "Defines reliability targets quantitatively: SLIs from real user journeys, SLOs with error budgets, and multi-window burn-rate alerts. Use when setting reliability targets, designing SLO alerting, or enforcing error-budget policy."
---

# SRE / SLO Engineer

## Overview

Reliability is a product feature with a measurable target, not a vibes-based aspiration. This skill turns user journeys into Service Level Indicators (SLIs), wraps each SLI in a Service Level Objective (SLO), calculates the error budget that falls out of the SLO, and sets burn-rate alerts that page on budget consumption — not raw thresholds. The result is an on-call experience where every alert tells you how fast you are burning your reliability allowance, not just that something is wrong.

Error budgets force a concrete tradeoff: the team may ship features freely while budget remains, and must freeze non-reliability work when budget is exhausted. This makes the reliability vs. velocity conversation quantitative and blameless.

**Core principle:** NO SLO WITHOUT AN SLI YOU ACTUALLY MEASURE. ALERT ON BURN RATE, NOT STATIC THRESHOLDS.

## The Iron Law

```
NEVER SET AN SLO FOR AN SLI YOU CANNOT COMPUTE FROM REAL PRODUCTION SIGNALS.
AN UNMEASURED SLO IS A FICTION. A THRESHOLD ALERT IS NOT A BURN-RATE ALERT.
```

## When to Use

**Use this when:**
- Defining or revisiting reliability targets for a service or user journey
- Replacing raw threshold alerts (CPU > 90%, latency > 500ms) with burn-rate alerting
- An error budget is exhausted and a feature-freeze policy decision is needed
- Preparing for an SRE review, launch readiness, or post-incident reliability work
- Designing on-call rotations and escalation policies around SLO violations

**Use this ESPECIALLY when:**
- The team argues about uptime in percentages without specifying the SLI being measured
- Alerts fire constantly but incidents are rare (threshold alerts with no burn-rate context)
- A new service ships to production without any reliability contract
- Stakeholders want "five nines" without understanding what user action that covers

**Don't skip when:**
- Adding a new critical user journey to an existing service (each journey needs its own SLI)
- Changing an alerting rule — even a "quick tweak" can eliminate burn-rate detection

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for service names and SLI definitions, and respect decisions in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## Phase 1: Map User Journeys → SLIs

Do not start from metrics dashboards. Start from what users actually do.

1. **List the critical user journeys** — "User logs in", "Checkout completes", "Report generates", "Webhook delivers". Three to seven journeys covers most services.

2. **Choose an SLI class for each journey:**

   | SLI Class    | What it measures                           | When to use                          |
   |--------------|--------------------------------------------|--------------------------------------|
   | Availability | Ratio of successful requests to total      | APIs, RPCs, any request/response     |
   | Latency      | Fraction of requests faster than threshold | Interactive user-facing endpoints    |
   | Error rate   | Ratio of errors to total requests          | Often the inverse of availability    |
   | Freshness    | Fraction of reads returning data ≤ N old   | Caches, pipelines, batch jobs        |
   | Throughput   | Fraction of periods meeting a minimum rate | Streaming, data-processing pipelines |

3. **Write the SLI as a ratio** — Good events divided by valid events. Never an average.

   ```
   # Availability SLI for /api/checkout
   SLI = count(HTTP 2xx responses in window)
         / count(HTTP requests excluding 429 and health-checks in window)

   # Latency SLI for /api/checkout (target: 95% of requests < 300ms)
   SLI = count(requests where response_time < 300ms)
         / count(all requests)

   # Freshness SLI for recommendation cache
   SLI = count(reads where data_age < 60s)
         / count(all reads)
   ```

4. **Verify the SLI is computable today** from logs, metrics, or tracing. If not, instrument first — do not write the SLO yet.

## Phase 2: Set SLOs and Error Budgets

**Start with what you can defend, not what sounds impressive.**

| Journey              | SLI class    | SLI formula            | SLO target | Window  | Error budget      |
|----------------------|--------------|------------------------|------------|---------|-------------------|
| Checkout complete    | Availability | 2xx / valid requests   | 99.9%      | 30 days | 43.2 min/month    |
| Checkout latency     | Latency      | req < 300ms / all req  | 95.0%      | 30 days | 36 hr/month       |
| Login success        | Availability | 2xx / valid requests   | 99.5%      | 30 days | 3.6 hr/month      |
| Recommendation cache | Freshness    | reads < 60s old / all  | 99.0%      | 30 days | 7.2 hr/month      |

**Error budget formula:**
```
Error budget (minutes/month) = (1 - SLO target) × 30 days × 24 hr × 60 min
  e.g. (1 - 0.999) × 43,200 min = 43.2 min
```

**Rules for target setting:**
- SLO must be stricter than current measured baseline (no free credits).
- SLO must be looser than your infrastructure can theoretically provide.
- Each journey gets its own SLO. A single "service SLO" averages away failures.

## Phase 3: Design Multi-Window Burn-Rate Alerts

A static threshold alert ("error rate > 1%") does not tell you whether your budget is in danger. A burn-rate alert answers: "At this rate, how long until the budget runs out?"

**Burn rate formula:**
```
burn_rate = (1 - current_SLI) / (1 - SLO_target)
  e.g. SLO = 99.9%, current error rate = 1%
       burn_rate = 0.01 / 0.001 = 10×
       → budget exhausted in 30d / 10 = 3 days
```

**Multi-window burn-rate alert pattern (Google SRE Workbook):**

Use two windows per severity tier. The short window catches fast burns; the long window prevents false positives on brief spikes.

| Severity | Short window | Long window | Burn rate threshold | Budget consumed | Action          |
|----------|-------------|-------------|---------------------|-----------------|-----------------|
| Page     | 1 h         | 5 min       | 14.4×               | ~2% in 1 h      | Wake on-call    |
| Page     | 6 h         | 30 min      | 6×                  | ~5% in 6 h      | Wake on-call    |
| Ticket   | 1 day       | 2 h         | 3×                  | ~10% in 1 day   | Create ticket   |
| Ticket   | 3 days      | 6 h         | 1×                  | ~10% in 3 days  | Monitor         |

```yaml
# Prometheus / Alertmanager — checkout availability SLO (99.9%, 30d)
groups:
  - name: slo.checkout.availability
    rules:
      # Fast burn: page immediately
      - alert: CheckoutSLOFastBurn
        expr: |
          (
            rate(http_requests_errors_total{job="checkout"}[1h])
            / rate(http_requests_total{job="checkout"}[1h])
          ) / (1 - 0.999) > 14.4
          and
          (
            rate(http_requests_errors_total{job="checkout"}[5m])
            / rate(http_requests_total{job="checkout"}[5m])
          ) / (1 - 0.999) > 14.4
        labels:
          severity: page
          slo: checkout-availability
        annotations:
          summary: "Checkout SLO fast burn: {{ $value | humanize }}× budget rate"
          runbook: "https://runbooks.example.com/checkout-slo"

      # Slow burn: create ticket
      - alert: CheckoutSLOSlowBurn
        expr: |
          (
            rate(http_requests_errors_total{job="checkout"}[6h])
            / rate(http_requests_total{job="checkout"}[6h])
          ) / (1 - 0.999) > 6
          and
          (
            rate(http_requests_errors_total{job="checkout"}[30m])
            / rate(http_requests_total{job="checkout"}[30m])
          ) / (1 - 0.999) > 6
        labels:
          severity: ticket
          slo: checkout-availability
```

## Phase 4: Error-Budget Policy

An error budget without a policy is decoration.

1. **Define the budget-exhaustion trigger:** commonly at 0% remaining with >7 days left in the window.
2. **Define the freeze action:** halt all non-reliability feature releases; redirect eng capacity to reliability work.
3. **Define the resume condition:** budget restored above 50% OR post-mortem + mitigations shipped.
4. **Record the policy in `docs/adr/`** — this is an architectural decision, not an ops preference.

```markdown
# Error Budget Policy — Checkout Service

| Budget remaining | Action                                               |
|-----------------|------------------------------------------------------|
| > 50%           | Normal feature velocity                              |
| 25–50%          | Reliability review required before new feature ships |
| < 25%           | Senior SRE approval required per release             |
| Exhausted       | Feature freeze; all eng on reliability work          |
```

## Phase 5: Reduce Toil

Toil is manual, repetitive, automatable work that grows linearly with service scale. Cap it at 50% of on-call time.

1. **Identify toil:** runbook steps that a script could execute, tickets that always follow the same pattern, manual restarts triggered by alerts.
2. **Automate one toil item per sprint:** auto-remediation scripts, alert auto-silencing with context, runbook automation via PagerDuty Runbook Automation or AWS SSM.
3. **Track toil percentage:** on-call weekly review — hours spent on toil vs. on project work.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "We'll add the SLI measurement after we set the SLO"
- "The error budget is almost gone but the feature is nearly done"
- "This alert is the same as the SLO alert, just simpler"
- "Five nines is always better — let's just use that"
- "We only need one SLO for the whole service"
- "The on-call team will know when to page; we don't need burn-rate thresholds"

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We can set the SLO based on what sounds good" | An SLO not grounded in measured baselines will be violated on day one or be meaninglessly loose. |
| "A single threshold alert is basically burn rate" | A threshold alert fires on any spike; burn-rate alerts fire only when the budget is genuinely at risk. False-positive pages train teams to ignore alerts. |
| "Our service is critical, so 99.999% SLO" | Five nines = 26 seconds/month of error budget. One 30-second deploy window exhausts it. Aspirational SLOs destroy trust. |
| "Error budgets punish the team unfairly" | Error budgets protect the team — they give a quantitative reason to slow down and do reliability work without needing a manager to decide. |
| "Freshness and throughput don't need SLOs" | Every user-visible property that can degrade has a reliability threshold. If users notice stale data, freshness needs an SLO. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "This alert fires every night at 2am but nothing is wrong" — You set a threshold alert, not a burn-rate alert; return to Phase 3.
- "We've burned half our budget and I didn't know" — Burn-rate alert windows are misconfigured or the slow-burn tier is missing; audit the long-window thresholds.
- "What does this number actually mean to users?" — Your SLI is a system metric (CPU, memory) not a user-journey ratio; return to Phase 1.
- "We ran out of budget but we're still shipping features" — The error-budget policy is not enforced; surface Phase 4 to the team lead.
- "I can't figure out where this alert came from" — Alert annotations are missing the runbook and SLO label; add them before the next on-call shift.

**When you see these:** STOP. Return to the relevant phase.

## Related Skills

- **observability-pro** — SLIs require structured metrics and tracing; instrument the Four Golden Signals before defining SLOs
- **test-engineer** — validate that SLO targets hold under peak traffic; use load test results to calibrate latency SLI thresholds
- **chaos-engineer** — run controlled failure experiments to measure how fast chaos events burn the error budget; SLO steady-state hypothesis maps directly to chaos experiment abort conditions
- **performance-engineer** — latency SLIs share thresholds with Core Web Vitals and p99 profiling; coordinate when tightening latency SLOs post-optimization
- **devops-release-engineer** — error-budget policy affects release gates; wire freeze policy into the deployment pipeline and feature-flag controls

## Verification

- [ ] Every SLI is expressed as a ratio of good events to valid events (not an average or gauge)
- [ ] Each SLI is computable from live production signals right now — not planned instrumentation
- [ ] Each SLO has a defined measurement window (7-day, 30-day, or rolling) and a numeric target
- [ ] Error budget for each SLO calculated and documented (minutes or fraction per window)
- [ ] Multi-window burn-rate alerts implemented: at minimum one fast-burn (≤1h) and one slow-burn (≥6h) tier per SLO
- [ ] Each alert references the SLO it protects via a label and links to a runbook in annotations
- [ ] Error-budget policy written and recorded in `docs/adr/` with freeze trigger, freeze action, and resume condition
- [ ] Toil percentage tracked for on-call shifts; plan exists to automate the highest-toil items
- [ ] SLO dashboard shows remaining budget as a percentage with a time-to-exhaustion projection
- [ ] Post-incident review updates the SLI definition or SLO target when the incident exposed a gap
