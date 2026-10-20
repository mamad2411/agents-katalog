---
name: slo-and-error-budgets
version: 1.0.0
description: Choosing SLIs, setting SLO targets, and running an error-budget policy — the mechanics behind site-reliability's SLI/SLO management responsibility. Use when defining service health signals, setting a reliability target, deciding alert thresholds, or using budget consumption to gate release velocity. Do NOT use for logs/metrics/traces/dashboard design — that is `observability-design`, which stops short of what target to set or how to act on budget burn.
---

# SLOs and Error Budgets

## SLI vs. SLO vs. SLA
- **SLI** (indicator) — a measurement of user experience: successful request rate, latency at a percentile, job completion rate. Not a raw infrastructure metric (CPU, memory) unless that metric is a direct, evidenced proxy for user impact.
- **SLO** (objective) — the target for that indicator over a measurement window: "99.9% of checkout requests complete in under 2s over a rolling 28 days."
- **SLA** (agreement) — a contractual commitment, usually looser than the internal SLO, with real consequences (credits, penalties) for breach. Not every SLO needs an SLA; every SLA needs an SLO backing it with margin.

## Choosing a good SLI
- Measure what the user experiences, not what's easy to measure. Server-side "request succeeded" can be true while the user's page never rendered correctly — prefer the signal closest to actual task completion.
- One SLI per meaningfully distinct user journey, not one SLI per service. A payment API and a search API serving the same backend deserve separate SLIs if users experience them differently.
- Avoid an SLI that's actually multiple things bundled together (availability + correctness + latency in one number) — split them; a target on a bundle can't be reasoned about.

## Setting a target
- **A target with no basis in user expectation or cost is a decoration, not an SLO.** 99.99% is not inherently better than 99.9% — it's substantially more expensive in engineering effort, for a difference (roughly 52 minutes/year vs. 8.8 hours/year of allowed downtime) users may never notice if the failure mode is graceful.
- Start from: what failure rate would users actually notice or complain about? What does the business case for higher reliability actually justify?
- Leave margin between the internal SLO and any external SLA — breaching the SLA should be rare even when the SLO is under real pressure.

## Error budget
- Budget = `1 - SLO` over the measurement window. A 99.9% monthly SLO allows roughly 43 minutes of unavailability per 30 days.
- **Track burn rate, not just remaining balance.** A service that consumes its entire month's budget in the first hour and one that consumes it evenly are in very different states even at the same "50% remaining" snapshot.
- **Multi-window, multi-burn-rate alerting** avoids both false alarms and slow detection: a short window at a high burn-rate threshold pages immediately (something is badly wrong right now); a longer window at a lower threshold files a ticket (a slow, sustained leak that will exhaust the budget before the window resets). A single fixed threshold on one window can't do both jobs.
- **The budget is a policy lever, not a dashboard.** Feed it into `release-manager`'s risk assessment (a service that's already burned its budget for the month is a reason to slow deployment velocity, not just a number to note) and into engineering prioritization (a service chronically burning budget needs reliability investment ahead of new features, and that tradeoff should be explicit and visible, not silently absorbed).

## Common mistakes
- Setting an SLO on a metric nobody owns — an SLO needs an owner who can actually act on budget burn, or it's just a number.
- Too many SLOs per service — if everything is tracked, nothing is prioritized; a handful of SLIs that actually reflect user experience beats a dashboard of twenty vanity metrics.
- Ignoring burn rate and only checking budget balance at the end of the period — by then it's too late to have acted on the trend.
- Copying a target from another team or a generic industry number without checking it against this service's actual user expectations and cost structure.
