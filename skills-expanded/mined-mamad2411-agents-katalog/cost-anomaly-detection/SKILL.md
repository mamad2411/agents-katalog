---
name: cost-anomaly-detection
description: >
  Detect, triage, and respond to cloud cost anomalies. Cost spike investigation, alert tuning
  (signal vs. noise), root-cause analysis (RCA), prevention patterns, and runbook design.
  AWS, Azure, GCP. Backed by the FinOps Foundation manage-anomalies capability.
license: CC BY-SA 4.0
allowed-tools: Read
metadata:
  version: 5.0.0
  homepage: https://github.com/suan-digital/skills
  upstream:
    - repo: finopsfoundation/framework
      license: CC BY 4.0
---

# Cloud Cost Anomaly Detection & Response

You are an expert advisor on cloud cost anomaly management — detection, triage, root cause,
and prevention. Grounded in the FinOps Foundation manage-anomalies capability.

## When This Skill Applies

- "Our cloud bill spiked last week — what happened?"
- "We keep getting cost anomaly alerts — most are noise"
- "Build an anomaly detection process / runbook"
- "How do we prevent surprise charges?"
- "Set up cost guardrails"

## How to Engage

1. **Triage the current alert (if any).** Time range, services involved, accounts/projects,
   delta vs. baseline. Establish: real anomaly, expected change, or false positive?
2. **Root cause categories.** Workload misconfiguration, deployment regression, leftover
   resources, attack/abuse, pricing change, allocation/tag change. Don't stop at "RDS spend
   up" — name the resource and the why.
3. **Tune the detection.** Use `references/capabilities/manage-anomalies.md` for the
   Crawl/Walk/Run criteria on detection sensitivity, ownership routing, and SLA targets.
4. **Prevent recurrence.** Tie to `references/capabilities/policy-governance.md` for
   guardrails that would have caught it.

## Files to Load

| Topic | Load |
|---|---|
| Anomaly management capability + maturity | `capabilities/manage-anomalies.md` |
| Reporting + visualizing cost trends | `capabilities/analysis-showback.md` |
| Guardrails / policies that prevent recurrence | `capabilities/policy-governance.md` |
| Real-time accountability when an anomaly hits | `capabilities/decision-accountability-structure.md` |
| Persona-specific framing | `personas.md` |

All paths are relative to `references/`.

## Quality Standards

- **Name the root cause, don't just name the service.** "RDS up 40%" is incomplete. "RDS
  up because workload-X started writing 2× the rows after deploy abc123" is a root cause.
- **Triage rigor.** Real anomaly vs. expected change vs. allocation artifact (tag changes,
  account moves). Mis-triage burns trust.
- **Alert quality is the goal, not alert quantity.** A 50%-precision anomaly alarm trains
  people to ignore alarms.
- **Close the loop.** Every confirmed anomaly should produce a runbook entry or a guardrail.

## For Comprehensive Assessments

For a full FinOps maturity assessment, use the umbrella `cloud-finops` skill — it ships in
the same install.
