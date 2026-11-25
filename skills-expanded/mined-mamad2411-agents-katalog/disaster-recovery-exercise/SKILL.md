---
name: disaster-recovery-exercise
description: "Rehearse restoration of a business service from recovery copies and measure whether the declared RTO, RPO and integrity criteria actually hold. Use when planning or reviewing a restore drill, proving cross-region recovery from backups, measuring the full dependency-ordered restore path, validating recovered transactions with a business owner, or testing recovery identity and keys. Establish an isolated scope, written abort, point-in-time evidence, timestamps and acceptance before the exercise. For backup topology, retention and recovery objectives use backup-recovery-design; for fault injection, chaos experiments, on-call and failover drills without restoration from copies use game-day; for a real outage use incident-response."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Disaster Recovery Exercise

A successful backup job proves that a copy was produced. A successful recovery exercise proves that a named business capability can be restored from that copy and accepted within its objective. Measure the entire path rather than the database restore command alone.

## Scope

Use for restore-from-copy exercises, including regional rebuilds and ransomware recovery rehearsals. Use `backup-recovery-design` to set the recovery architecture and objectives first. Use `game-day` for deliberate fault injection or failover that does not restore from copies, and `incident-response` when the failure is real. This procedure plans and assesses a drill; any destructive command or live traffic change needs its own approved change window and operator.

## Hard gates

1. Name the business capability, recovery point, RTO, RPO, integrity invariants and business acceptance owner before scheduling. Unknown objectives are a design finding, not a pass.
2. Prove the isolated target cannot write to production, receive production traffic, send customer notifications, replay into live queues, or overwrite recovery copies. Use dedicated credentials and bounded egress; confirm the separation before decrypting data.
3. Establish a stop condition and exercise the abort before restore starts. Identify who can stop, how to freeze writes and jobs, how to dispose of the target, and how to preserve evidence without exposing customer data.
4. Obtain the required change and data-handling approvals. Keep timestamps, identities and backup metadata in the audit trail; keep secrets and customer records out of the report.

## Workflow

### 1. Declare the scenario and clock

Record the simulated incident boundary `T0`, whether detection and declaration will actually be exercised or only assumed, the business deadline `T0 + RTO`, and the latest acceptable recovery point `T0 - RPO`. If detection or approvals are simulated, label the resulting total as a scenario estimate; measure technical restore duration separately and do not claim a proven full RTO. Choose a copy that would actually survive the declared threat; the newest production snapshot cannot prove recovery from compromised production administration. Record immutable copy ID, creation/completion timestamps, log position and retention status.

### 2. Walk the actual dependency graph

Start with the restore graph from `backup-recovery-design`; identify cycles and bootstrap access outside failed SSO or DNS. Write a timed plan for recovery identity and KMS, network/control plane, foundational stores and logs, application schemas and artefacts, consumers and derived state, observability, external integrations and traffic readiness. Record which tasks can run in parallel and the critical path. For every edge identify the owner, prerequisite, command or runbook, expected duration, validation and abort. Rehearse missing access or quota in a safe target; do not silently substitute administrator credentials that would be unavailable in the stated scenario.

### 3. Restore and capture evidence

Use the approved runbook without editing production state. Log start/end of detection, decision, provisioning, copy retrieval, key unlock, restore, replay, validation and business sign-off; distinguish observed timestamps from assumed durations. Record failed attempts and manual waits. Reconcile transaction IDs, sequence bounds, balances or other workload-specific invariants. Compare the last committed source event before `T0` with the latest usable restored event; `observed RPO = T0 - last usable recovery point`. Check that accepted service meets the minimum functionality and observed user-facing SLI. Only when detection, decisions and acceptance were exercised is `observed RTO = business acceptance timestamp - T0` a measured full-path value. Otherwise report the measured restore path and the modeled total separately.

A provider job marked successful, a healthy database process or a login screen is insufficient. Exercise a representative read and write in the isolated target, verify external dependency behaviour and obtain the named business owner's acceptance against recorded criteria. If the exercise cannot safely test a production-only step, mark that step unproven and bound its likely effect; do not report a full pass.

### 4. Close safely and revise the claim

Confirm no restored endpoint or consumer still targets production. Revoke temporary credentials, remove isolated data under the approved retention schedule, and retain redacted logs and timing evidence. Compare observed RTO/RPO with the declared objectives and document each invariant's result. Assign an owner and due date to every gap; if a target was missed, update the recovery plan or negotiate a revised business objective. Schedule the next exercise against the missing evidence, including peak-size data and an alternate operator where relevant.

## Evidence table

| Measure | Evidence | Decision |
| --- | --- | --- |
| Recovery point | Copy ID, completed time, log position, last usable transaction | Observed RPO versus target |
| Time to acceptance | `T0`, observed phase timestamps, assumed phases and sign-off time | Measured path and, if needed, modeled total versus target |
| Integrity | Reconciled invariants and representative transactions | Business acceptance or explicit rejection |
| Dependency path | Actual order, blocked edges, temporary privileges and waits | Critical path and remaining single points |
| Safety | Isolation and abort proof, teardown record | No effect on live writes or customer traffic |

## Anti-patterns

**Restoring only the database.** A store with no keys, identity, schema, application or business validation is not an accepted service.

**Starting the RTO clock at restore command execution.** Detection, decisions and business sign-off consume time and are part of a real recovery.

**Testing with a recent, convenient copy outside the scenario.** A copy inaccessible after the declared failure proves nothing about that failure mode.
