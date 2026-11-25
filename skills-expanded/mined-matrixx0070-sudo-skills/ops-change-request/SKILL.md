---
name: ops-change-request
version: 1.0.0
description: Draft a change management request with blast-radius impact analysis, validation checks, and a triggered rollback plan.
author: matrixx0070
tags: [operations, change-management, risk, rollback, itil, cab]
capabilities: []
---

# Change Request

## When to use
Use this before any production, infrastructure, or process change that could affect users, data, or dependent teams, and when a change advisory board or approver needs a structured record to review.

**Not for:** routine pre-approved standard changes with an existing runbook (just execute it), or incident firefighting (use an incident/runbook flow — a CR is written after, not during).

## Method
1. **Describe the change.** State what changes, why now, and the end state in one paragraph. *Decision:* classify as standard (pre-approved), normal (needs CAB), or emergency (expedited approval + retroactive record).
2. **Scope the blast radius.** List affected systems, services, teams, and users, plus upstream and downstream dependencies.
3. **Analyze impact.** Assess availability, performance, security, and cost effects. Rate risk (low/med/high) as likelihood x impact.
4. **Plan implementation.** Write ordered steps with owners, the maintenance window, and required approvals.
5. **Define validation.** Specify the exact checks (metrics, smoke tests, user paths) that confirm success after the change.
6. **Write the rollback.** Give concrete reversal steps, the decision trigger to invoke them, the point of no return, and the max acceptable recovery time (RTO). *Decision:* if there is no rollback (irreversible migration), say so explicitly and add extra pre-checks and a paused go/no-go gate.
7. **Communicate.** Note who is informed before, during, and after.

## Example
**Change:** upgrade Postgres 14 -> 15 on the orders DB (normal). **Blast radius:** orders API, reporting jobs, 3 downstream services. **Window:** Sun 02:00-04:00. **Validation:** replica lag < 1s, orders smoke test green, error rate flat 30 min. **Rollback:** promote standby on old version; **trigger** = smoke fail or error rate >2x baseline; **point of no return** = new writes accepted post-cutover; **RTO** 15 min.

## Pitfalls
- **Under-scoping the blast radius.** The dependency you forgot is the one that pages you. Trace both directions.
- **Untested rollback.** "Restore from backup" you have never rehearsed is a hope, not a plan.
- **No point-of-no-return marked.** Teams try to roll back after the migration is irreversible and make it worse.
- **Vague validation.** "Check it works" fails under pressure; list named, pass/fail checks.

## Output format
```
Header:         change ID | title | type | requested-by | date
Description:    what + why now + end state
Impact:         systems | dependencies | risk rating
Implementation: numbered steps | owners | window | approvals
Validation:     named pass/fail checks
Rollback:       steps | trigger | point of no return | RTO
Approvals:      required sign-offs
Communication:  before | during | after
```
