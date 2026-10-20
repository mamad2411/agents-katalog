---
name: slo-design
description: "Design or review service level objectives before alert rules exist: map the user journey to measurable good and valid events, choose availability, latency, freshness or correctness indicators, set a target and rolling compliance window from observed performance and user needs, calculate an error budget, and assign an owner and release decision. Use for requests such as 'what SLO should checkout have?', 'define SLIs for Pub/Sub processing', 'is 99.99% realistic?', or 'how much downtime can we afford?'. Produce a measurement specification with exclusions, low-traffic treatment and a validation plan. For PrometheusRule, paging thresholds, burn-rate alert implementation, Alertmanager routing or pager fatigue, use alert-design after the objective is agreed. For incident command use incident-response."
allowed-tools: Read, Grep, Glob, Edit, Write
---

# SLO Design

A useful SLO describes what users can rely on, can be computed from real telemetry, and leaves room to make deliberate release decisions. A target without a denominator, period or owner cannot guide operations.

## Scope

Use for defining or reviewing the user journey, SLI, target, compliance period, budget and decision policy. Do not use for implementing alerting rules (`alert-design`), troubleshooting a live outage (`incident-response`), or instrumenting missing measurements (`instrumentation`). If the requested SLI is unmeasurable, specify the telemetry gap and hand it to `instrumentation` before claiming compliance.

## Workflow

### 1. Choose the journey and accountable owner

Name the user and the operation they care about. Identify the team that controls reliability changes, dependencies and an escalation owner. For a multi-service journey, measure the end-to-end outcome where possible. State what is outside the team's control rather than silently excluding it.

### 2. Define an event-based indicator

Write `good events / valid events` with unit, source, labels, threshold and exclusions. Specify what happens to timeouts, retries, cancellations, client errors and missing telemetry. Count a request once at a stable boundary: attempts and retries can inflate the denominator. For asynchronous work, use an eligible item completed correctly before a deadline, with one durable identity per item. For low traffic, assess whether a few events dominate the budget; consider a longer window, synthetic probes or a journey-level objective, and distinguish probes from actual user events.

Do not use average latency as a success ratio. Choose a user-relevant threshold and count events served within it. Keep diagnostic p99 and resource saturation on dashboards. Verify the numerator cannot exceed the denominator and that empty denominators produce unknown, not healthy.

### 3. Select target and period from evidence

Compare historical SLI over several candidate windows with user expectations, incident history, contractual commitments and dependency limits. Record the baseline and uncertainty. Choose a target that separates acceptable experience from action-worthy degradation, not simply the current maximum or a round number. Specify rolling versus calendar window and time zone if calendar-based. Document planned maintenance treatment explicitly; do not erase failed user events merely because a change was scheduled.

### 4. Calculate and assign the budget

For event-based SLOs, `allowed bad events = valid events × (1 - target)` over the compliance window. At 99.9% of 1,000,000 valid requests, the budget is 1,000 bad requests. A duration equivalent (43.2 minutes over a 30-day window at 100% unavailability) assumes even traffic and total outage; it is not a second independent budget. Show the traffic and period assumptions when reporting it.

Specify who reviews budget consumption, how often, and which measured threshold changes release behaviour. Agree exceptions and approval owner in advance, including urgent security or recovery work. If the SLO is missed, investigate reliability work and the objective itself before applying a mechanical release freeze.

### 5. Validate the specification

Recompute numerator and denominator against raw samples for a normal period, a known incident, low traffic and missing data. Check aggregation by region and customer segment to avoid a high-volume segment masking a critical one. Compare end-to-end results with external user evidence. State coverage gaps and an owner/date for each. Hand an agreed SLI, target and window to `alert-design` for burn-rate rule and response-policy implementation; do not duplicate rule templates here.

## Output

| Item | Required decision |
| --- | --- |
| Journey and owner | User operation, service boundary, accountable team |
| SLI | Good and valid events, source, threshold, exclusions, missing-data behaviour |
| Objective | Target, compliance window, historical baseline and rationale |
| Budget | Event count, traffic assumption, review cadence and decision owner |
| Evidence | Normal and incident sample calculations, segment checks, telemetry gaps |
| Handoff | Agreed specification for `alert-design` and unresolved assumptions |

## Anti-patterns

**Infrastructure health as the objective.** A healthy pod says little about whether checkout succeeds. Use user outcomes; keep infrastructure signals for diagnosis.

**Changing exclusions after an incident.** Retrospective filtering makes the objective impossible to audit. Record exclusions before the window starts and retain the unfiltered series.

**A budget with no decision owner.** A number on a dashboard cannot guide a release unless someone has agreed what consumption changes.
