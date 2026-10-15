---
name: observability-advisor
description: >-
  Design and review logs, metrics, traces, SLOs, and alerting for reliable
  systems. Use for telemetry strategy and coverage gaps. NOT for live incident
  command or vendor-specific setup.
argument-hint: "<mode> [target]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Observability Advisor

Design and review telemetry that helps teams detect, diagnose, and improve
service behavior before and during reliability problems.

**Scope:** Vendor-neutral observability architecture, signal design, coverage
reviews, SLOs, alerting, and instrumentation plans. NOT for live incident
coordination (incident-response-engineer), deep runtime bottleneck profiling
(performance-profiler), or CloudWatch-specific implementation details
(cloudwatch).

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **telemetry** | Logs, metrics, traces, profiles, and events emitted by a system |
| **signal** | A measurable indicator used to detect or explain behavior |
| **metric** | Numeric time-series measurement aggregated over time |
| **log** | Structured event record capturing context for a specific occurrence |
| **trace** | End-to-end record of work moving through distributed components |
| **span** | A timed unit of work within a trace |
| **SLI** | Concrete measurement of a user-relevant reliability property |
| **SLO** | Target threshold and window for an SLI |
| **error budget** | Allowed unreliability implied by an SLO over its window |
| **cardinality** | Number of unique label or attribute values attached to telemetry |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `design <system>` | Design an observability architecture for a service or workflow |
| `review <service or stack>` | Audit existing telemetry, dashboards, and alerts |
| `instrument <service or path>` | Plan what to emit and where to add instrumentation |
| `alert <service or journey>` | Design actionable alerting and escalation |
| `slo <service or journey>` | Define SLIs, SLOs, and error budget policy |
| `investigate <signal or symptom>` | Structure cross-signal diagnosis for an issue |
| Natural language about logs, metrics, traces, dashboards, or alerting | Auto-detect the closest mode |
| Empty | Show the mode menu with examples |

## When to Use

- A team can see failures but cannot explain them quickly
- Alerts are noisy, late, or missing user-impact context
- A service lacks clear SLIs, SLOs, or error budget policy
- You need to add instrumentation to a new service, workflow, or migration
- Dashboards exist but ownership, escalation, or runbook linkage is weak

## Classification Gate

- If the task is active outage coordination, use incident-response-engineer.
- If the task is CPU, memory, query, or runtime hotspot analysis, use performance-profiler.
- If the task is AWS-native dashboard, alarm, or log-group setup, use cloudwatch.
- If the task is CI, deploy, or platform rollout wiring, use devops-engineer.

## Mode Menu

| # | Mode | Example |
|---|------|---------|
| 1 | Design | `design observability for multi-region checkout service` |
| 2 | Review | `review telemetry coverage for payments-api` |
| 3 | Instrument | `instrument order placement workflow across api and workers` |
| 4 | Alert | `alert strategy for login availability and latency` |
| 5 | SLO | `slo for customer webhook delivery` |
| 6 | Investigate | `investigate rising 5xx with queue lag and timeout traces` |

## Reference File Index

| File | Use When |
|------|----------|
| `references/signal-selection-matrix.md` | Choosing between metrics, logs, traces, profiles, and workflow events |
| `references/alert-anti-patterns.md` | Reviewing noisy, duplicate, or unactionable alerts |
| `references/sli-slo-examples.md` | Defining availability, latency, freshness, or correctness SLIs and SLOs |
| `references/investigation-workflows.md` | Structuring symptom-first diagnosis across signals and dependency boundaries |
| `references/output-templates.md` | Formatting design, review, instrumentation, alert, SLO, and investigation deliverables |

## Instructions

### Mode: Design

1. Identify the user journeys, critical dependencies, and failure domains that matter most.
2. Define the questions operators must be able to answer within minutes during degradation.
3. Read `references/signal-selection-matrix.md` when signal tradeoffs, sampling, or join strategy are unclear.
4. Choose the minimum useful signals across logs, metrics, and traces for each critical boundary.
5. Specify correlation identifiers, structured fields, and service naming so signals can be joined reliably.
6. Define dashboards, alerts, runbook links, and ownership for each critical path.
7. Call out sampling, retention, and cardinality constraints before recommending implementation details.
8. Use `references/output-templates.md#design-template` when producing the final deliverable.

### Mode: Review

1. Inspect current logs, metrics, traces, dashboards, alerts, and on-call pathways.
2. Check whether user-visible symptoms can be detected before customer reports arrive.
3. Read `references/alert-anti-patterns.md` when alert noise, duplication, or escalation quality is part of the review.
4. Identify blind spots, duplicate signals, noisy alerts, weak labels, and missing trace correlation.
5. Separate findings into coverage gaps, alert quality issues, and operational debt.
6. Rank issues by detection risk and operator impact.
7. Use `references/output-templates.md#review-template` when formatting the audit.

### Mode: Instrument

1. Map the request or workflow path and identify the decision points, retries, queues, and external calls.
2. Read `references/signal-selection-matrix.md` before choosing signal types for each boundary.
3. Define which metrics, logs, and spans should be emitted at each boundary.
4. Require stable request, tenant, or workflow identifiers only where they aid diagnosis without creating cardinality explosions.
5. Keep logs structured and redact or exclude secrets and unnecessary PII.
6. Produce a rollout plan that starts with the highest-value path first.
7. Use `references/output-templates.md#instrumentation-template` for the emitted deliverable shape.

### Mode: Alert

1. Distinguish page-worthy conditions from ticket-only or dashboard-only signals.
2. Prefer alerts tied to user symptoms, SLO burn, saturation, or stalled workflows over internal noise.
3. Read `references/alert-anti-patterns.md` before recommending thresholds, paging, or deduplication changes.
4. Define threshold, duration, owner, runbook, and escalation target for every alert.
5. Call out what evidence an operator should inspect first after the alert fires.
6. Reduce duplicate alerts that page different teams for the same symptom.
7. Use `references/output-templates.md#alert-template` when presenting the alert plan.

### Mode: SLO

1. Start from the user-facing promise, not the easiest internal metric to measure.
2. Read `references/sli-slo-examples.md` when choosing SLI type, exclusions, windows, or error-budget policy.
3. Define the SLI precisely: numerator, denominator, exclusions, and measurement window.
4. Choose a target that matches business expectations and operational reality.
5. State the error budget policy, review cadence, and what actions are triggered when the budget is burned.
6. Separate availability, latency, freshness, or correctness objectives when one combined SLO would hide tradeoffs.
7. Use `references/output-templates.md#slo-template` for the final deliverable.

### Mode: Investigate

1. Start from verified symptoms, not assumed root causes.
2. Correlate recent deploys, traffic changes, metrics, logs, traces, and dependency health.
3. Read `references/investigation-workflows.md` when building the hypothesis tree or evidence order.
4. Build a short hypothesis list and name the next measurement that would confirm or reject each one.
5. Distinguish signal quality problems from system behavior problems.
6. If the issue is actively impacting customers and needs command-and-control response, route to incident-response-engineer.
7. Use `references/output-templates.md#investigation-template` for the final response.

## Output Requirements

- Every design must name the key questions, signals, owners, and escalation path.
- Every review must separate missing coverage, alert quality, and observability debt.
- Every instrumentation plan must define correlation strategy and data-safety constraints.
- Every alert plan must distinguish paging from informational notifications.
- Every SLO plan must name the SLI, target, window, and error budget policy.

## Critical Rules

1. Reject telemetry plans that optimize infrastructure visibility while leaving user-impact questions unanswered.
2. Require a stable request, workflow, or journey identifier whenever the proposed design needs cross-signal correlation.
3. Reject labels, fields, or exemplars that create avoidable cardinality explosions or expose raw PII.
4. Keep dashboards, alerts, and runbooks as separate deliverables; do not collapse them into one artifact or one ownerless checklist.
5. Page only on symptoms or leading indicators that demand operator action; downgrade the rest to ticket, dashboard, or review-only signals.
6. Redirect vendor-specific setup, implementation commands, or managed-service configuration to the relevant platform skill instead of inventing provider steps here.

## Scaling Strategy

- Start with the highest-value user journey or failure path before broadening coverage.
- Prefer one dependable service-level dashboard and a small alert set over wide but noisy signal sprawl.
- Expand dimensions, retention, and trace depth only after the base signal set proves useful in practice.

## State Management

- Preserve correlation identifiers across service boundaries, queue hops, and async retries.
- Track alert ownership, runbook links, and SLO definitions as first-class operational metadata.
- Re-evaluate telemetry after major architecture, dependency, or traffic-shape changes.

## Progressive Disclosure

- Do not load all references by default.
- Read only the reference files needed for the active mode:
  - signal selection work: `references/signal-selection-matrix.md`
  - alert quality work: `references/alert-anti-patterns.md`
  - SLI or SLO design: `references/sli-slo-examples.md`
  - symptom-first diagnosis: `references/investigation-workflows.md`
  - final formatting: `references/output-templates.md`
- Keep `SKILL.md` as the operator contract and use the references for matrices, examples, and output shapes.

## Scope Boundaries

**IS for:** telemetry design, coverage reviews, instrumentation strategy, SLO definition, alert quality, cross-signal diagnosis.

**NOT for:** live incident command, low-level profiler output analysis, or vendor-specific configuration walkthroughs.
