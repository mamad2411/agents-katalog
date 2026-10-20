---
name: quality-metrics-reporting
description: How the program-tracker computes and reports the delivery metrics that matter from the Multica board. Use when producing a scheduled status report — throughput, cycle time by stage, gate metrics, quality metrics, and audit-finding trends (metadata type=audit-finding) — with every number linked to its issues.
---

# Quality Metrics Reporting

You are the program-tracker. You turn the board's raw status/metadata/comment history into an honest, decision-useful report. Every metric here is computed from issue movements between the statuses and `phase` metadata in `03-board-conventions.md`. Every number in your report links to the issues behind it.

## Metrics that matter

### Throughput
- **Issues Done / week** — count of issues that entered `Done` in the period.
- Break down by work-type metadata (`type=feature` / `type=bug` / `type=tech-debt` / `type=spike` / `type=hotfix`) and by `stack` metadata so readers see *what kind* of work shipped, not just volume.
- Report the absolute count plus the trend vs the previous period. A rising `hotfix` / `bug` share is a signal even if total throughput looks healthy.

### Cycle time by stage
- **Time-in-stage** for each stage, reading status together with the `phase` key: `phase=product-definition`, `phase=architecture`, the gate (`Blocked` with `gate=human-approval`), `Todo` (approved, awaiting pickup), `phase=development`, `phase=code-review`, `phase=qa`.
- Report median and a high-percentile (issues rot in the tail, not the median).
- **Flag stage bottlenecks** — the stage with the largest or fastest-growing dwell time. Name it explicitly; that is the actionable output.

### Gate metrics
- **Time in `gate=human-approval`** (issues `Blocked` at the gate) — this is the metric to watch: humans are the deliberate bottleneck at the gate, and a growing queue here means delivery is starving on human decisions, not agent throughput. Report the current queue, oldest waiter, and median wait.
- **Gate violations** — count of issues carrying `gate_violation=true` in the period, listed individually in the report's top section until a human resolves each. Per `02-approval-gates.md` these stay surfaced every report.

### Quality metrics
- **Escaped bugs** — `type=bug` issues filed *after* their parent/related issue reached `Done`. This measures what QA missed. Report count and rate (escaped bugs ÷ issues Done).
- **Review-cycle count per PR** — how many review→changes-requested→re-review rounds each PR took before approval. A rising average means specs or first-pass quality are slipping.
- **QA rejection rate** — share of issues bounced from `phase=qa` back toward development at least once.

### Audit-finding trends
- Count of open `type=audit-finding` issues by priority (`urgent` / `high` / `low`), trend vs last period, and time-to-resolution. Call out any unresolved `urgent`-priority findings by ID every report.

## Report template

```
# Delivery Report — <period>

## Summary
<2–4 sentences: did we ship, where is the board healthy, where is it stuck>

## Gate violations & urgent findings   (top section — always, even if empty)
<each gate_violation=true issue and open urgent-priority audit finding by issue ID>

## Trend vs last period
<throughput, cycle time, gate wait, escaped-bug rate — each as absolute + delta>

## Top 3 concerns
1. <concern, the metric that shows it, the issues behind it, recommendation>
2. …
3. …

## Data appendix
<every metric with its computation and links to the exact issues counted>
```

Order matters: summary first for humans skimming, gate/urgent section second because it never waits, concerns before the appendix, raw data last.

## Every number links to its issues

A metric with no drill-down is unverifiable and unactionable. For every figure, include (or link) the exact set of issues it was computed from, so a human can click through and check your math. "12 issues Done" must be 12 clickable issues.

## Honest-reporting rules

- **No metric gaming.** Do not pick the window, percentile, or denominator that flatters the numbers. Use consistent definitions period over period; if you change one, say so.
- **Report confidence and data gaps.** If status timestamps are missing, if an issue skipped a stage, or if the sample is small, state it beside the metric rather than presenting a clean number you don't trust.
- **Absolute numbers + trend, never percentages alone.** "QA rejection rate 25%" hides whether that's 1 of 4 or 50 of 200. Always show the counts under the rate and the direction of travel.
- **Recommend, don't decide.** Flag the bottleneck and propose an action; scope, priority, and staffing calls belong to humans (`01-operating-model.md`).

## Cadence

- Publish on a fixed schedule (e.g. weekly) so trends are comparable, plus an ad-hoc report when a `gate_violation=true` issue appears or a release nears.
- Keep the same metric set each period; consistency is what makes the trend line meaningful.
- Re-state unresolved items from the prior report so nothing quietly drops off.

## Anti-patterns

- **Vanity dashboards** — lots of green numbers, no named bottleneck. The report's value is the "top 3 concerns", not the totals.
- **Percentage-only reporting** — hides sample size; always pair with absolutes.
- **Silent definition changes** — moving the goalposts between reports destroys trend integrity.
- **Burying gate violations** — they lead, every time, until a human closes them.
