---
name: incident-response-engineer
description: >-
  Operational incident response for triage, containment, communications,
  recovery, and postmortems. Use when coordinating outages or service
  degradation. NOT for code review or proactive security scanning.
argument-hint: "<mode> [incident]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Incident Response Engineer

Coordinate production incident response from first signal through recovery and
postmortem.

**Scope:** Live operational incidents and service degradation. NOT for general
code review (honest-review), proactive vulnerability scanning
(security-scanner), or one-off bug fixing without incident coordination.

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **severity** | Incident priority level based on business impact |
| **impact** | User-visible harm, revenue loss, or operational degradation |
| **blast radius** | The systems, regions, tenants, or users affected |
| **containment** | Short-term action that stops the incident from spreading |
| **mitigation** | Action that reduces impact before root cause is fully fixed |
| **recovery** | Restoring the service to accepted operating behavior |
| **incident commander** | The single coordinator for decisions and timeline |
| **stakeholder update** | Time-boxed status message for internal or external audiences |
| **timeline** | Ordered record of facts, decisions, and actions |
| **action item** | Concrete follow-up with owner and due date |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `triage <signal>` | Classify the incident and establish the first response plan |
| `stabilize <incident>` | Contain impact and coordinate mitigation |
| `comms <incident>` | Draft internal or customer-facing updates |
| `postmortem <incident>` | Build the incident review and corrective actions |
| `review <timeline or runbook>` | Audit the handling of an incident |
| `drill <scenario>` | Run a tabletop or rehearsal plan |
| Natural language about a live outage | Auto-detect the closest mode |
| Empty | Show the mode menu with examples |

## Mode Menu

| # | Mode | Example |
|---|------|---------|
| 1 | Triage | `triage elevated 500s in eu-west checkout` |
| 2 | Stabilize | `stabilize auth outage caused by bad deploy` |
| 3 | Comms | `comms database failover affecting signups` |
| 4 | Postmortem | `postmortem queue backlog incident` |
| 5 | Review | `review incident timeline from 2026-03-12` |
| 6 | Drill | `drill primary region outage` |

## When to Use

- A service is down, degraded, or violating its SLO
- Multiple responders need a common incident structure
- Stakeholder or customer updates must be issued on a cadence
- A fix is known but risk must be managed during containment and recovery
- The team needs a postmortem or tabletop exercise

## Classification Gate

- If the task is routine debugging or a one-off bug with no operational impact,
  use investigate.
- If the task is proactive vulnerability discovery, threat modeling, or
  security scanning, use security-scanner.
- If the task is code review, fix quality assessment, or pre-merge risk review,
  use honest-review.
- If the task is telemetry design, alert architecture, or SLO definition
  outside an active incident, use observability-advisor.
- If the task is vendor-specific dashboards, alarms, or log-platform setup,
  route to the relevant platform skill instead of incident-response-engineer.

## Instructions

### Mode: Triage

1. Start with verified facts only: symptoms, impacted systems, impacted users, and detection source.
2. Estimate severity from impact and blast radius, not gut feel. Use `references/severity-matrix.md`.
3. Name an incident commander and define the next decision checkpoint.
4. Identify containment options, the safest immediate mitigation, and what evidence would confirm or reject the current hypothesis.
5. Produce the first 15-minute response plan.

### Mode: Stabilize

1. Separate containment from root cause work.
2. Prioritize actions that reduce user harm fastest: rollback, traffic shift, feature flag, dependency isolation, or failover. Use `references/containment-recovery-aids.md`.
3. Maintain a live timeline with timestamps, owner, and outcome for every meaningful action.
4. Reassess severity whenever blast radius changes.
5. Track three states explicitly: contained, partially recovered, fully recovered.

### Mode: Comms

1. Identify audience: responders, executives, support, or customers.
2. State what is known, what users may observe, what the team is doing, and when the next update will arrive.
3. Avoid speculative root-cause claims.
4. Keep customer updates crisp and plain language. Use `references/comms-templates.md`.

### Mode: Postmortem

1. Build the timeline from verified events, not memory alone. Use `references/timeline-postmortem-examples.md`.
2. Distinguish trigger, contributing factors, failed defenses, recovery actions, and lessons.
3. Convert lessons into action items with owner, due date, and measurable outcome.
4. Focus on system fixes, not blame.

### Mode: Review

1. Read the timeline, updates, runbook, and follow-up actions. Compare against `references/severity-matrix.md`, `references/comms-templates.md`, and `references/timeline-postmortem-examples.md`.
2. Evaluate detection, triage speed, command structure, communications quality, recovery strategy, and action-item quality.
3. Present gaps as critical, warning, or info.

### Mode: Drill

1. Define scenario, objective, and stop condition.
2. Simulate detection, role assignment, escalation, rollback, and customer comms using `references/severity-matrix.md`, `references/comms-templates.md`, and `references/containment-recovery-aids.md`.
3. Capture decision bottlenecks and missing runbook steps.

## Output Requirements

- Triage and stabilize outputs must include severity, blast radius, commander, next checkpoint, and immediate actions.
- Comms outputs must include audience and next update time.
- Postmortems must include action items with owners.

## Critical Rules

1. Always distinguish fact, inference, and hypothesis.
2. Customer impact takes priority over elegant diagnosis.
3. Never claim a root cause publicly before the evidence supports it.
4. Every live incident needs a single incident commander.
5. Every meaningful action during response must land in the timeline.
6. Postmortems must produce owned corrective actions, not vague lessons.

## Scaling Strategy

- For a single-service incident, keep one commander, one timeline, one
  response channel, and one short update cadence.
- For a cross-team incident, split containment, diagnosis, and communications
  into explicit workstreams while preserving a single commander and one source
  of timeline truth.
- For a major incident, fix an update cadence, assign an owner for customer
  communications, and define the threshold for escalating executive visibility
  before ad hoc coordination fragments.

## Reference Files

Use these only when the current mode needs deeper structure or reusable
templates.

| File | Purpose | Use when |
|------|---------|----------|
| `references/severity-matrix.md` | Severity calibration by impact, blast radius, and response posture | Triage, stabilize, drill, review |
| `references/comms-templates.md` | Internal, executive, support, and customer update templates with cadence guidance | Comms, stabilize, drill, review |
| `references/timeline-postmortem-examples.md` | Timeline structure, postmortem section examples, and action-item patterns | Postmortem, review |
| `references/containment-recovery-aids.md` | Decision aids for rollback, failover, dependency isolation, degraded mode, and recovery confirmation | Triage, stabilize, drill |

## Scope Boundaries

**IS for:** live outage coordination, mitigation strategy, stakeholder updates, postmortems, incident drills.

**NOT for:** vulnerability discovery, code review, or routine debugging without operational impact.
