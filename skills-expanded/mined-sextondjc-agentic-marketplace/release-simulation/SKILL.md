---
name: release-simulation
description: Use when rehearsing a production promotion before it executes — covers rollback drills, traffic-switching rehearsals, and game-day validation for high-risk release scenarios.
---

# Release Simulation

## Specialization

Design and execute a release simulation: a rehearsal of the promotion procedure, rollback steps, and critical path actions in a pre-production environment before the real promotion window opens. Produces a simulation report and a go/no-go input for `release-readiness`.

This skill applies to high-risk releases: architecture changes, database migrations, traffic-switching events, security-critical deployments, and releases with complex rollback paths. It does not replace `release-readiness` — it feeds evidence into it.

## Trigger Conditions

- A release involves architecture changes, migrations, traffic routing changes, or steps that are difficult to reverse.
- The rollback procedure has never been exercised in the target environment.
- A release plan has a step sequence that has not been rehearsed and where errors during a live promotion would be costly.
- A security-sensitive deployment requires verification of hardening steps before production exposure.
- A release review identified that rollback confidence is low.

## Inputs

- Release plan: the full ordered sequence of promotion steps.
- Rollback procedure: the full ordered sequence of rollback steps and their triggers.
- Target environment description: what the production environment looks like (topology, dependencies, traffic routing).
- Simulation environment: what pre-production environment is available and how closely it mirrors production.
- Risk profile: the highest-risk steps in the promotion and rollback sequence.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Simulation plan | Ordered steps for the rehearsal: what will be executed, what will be observed, and what constitutes a pass for each step. |
| Rollback drill record | Result of executing rollback steps in the simulation environment. Each step: executed, result, and time taken. |
| Gap log | Steps that could not be simulated (e.g., production-only dependencies) with risk assessment for each gap. |
| Timing record | Actual time taken per step during simulation. Used to validate promotion window sizing and on-call SLAs. |
| Simulation verdict | Pass / Pass with conditions / Fail. Conditions and failures listed with recommended resolution before live promotion. |
| Release readiness input | Structured summary for `release-readiness` gate checklist: simulation result, timing record reference, gap log reference. |

## Workflow

1. Review the release plan and rollback procedure. Identify the highest-risk steps: those that are irreversible, dependency-sensitive, or time-constrained.
2. Assess the simulation environment: what steps can be rehearsed and what gaps exist vs. production.
3. Build the simulation plan: ordered steps with pass criteria for each.
4. Execute the rollback drill: run rollback steps in order in the simulation environment. Record each step result and time.
5. Execute the promotion rehearsal: run the promotion steps in order. Record each step result and time.
6. Build the gap log: document any steps that could not be simulated and assess the residual risk.
7. Record the timing record: aggregate step durations. Flag any steps that exceeded expected time.
8. Produce the simulation verdict: Pass if all executable steps passed and gap risks are acceptable; Fail if any step failed or gap risks are unacceptable.
9. Write the release readiness input summary.
10. Record the originating plan or workstream ID on all outputs.

## High-Risk Step Classification

| Risk type | Why it needs simulation |
|---|---|
| Database migration | Schema changes may be irreversible; rollback must restore data integrity |
| Traffic routing change | Misconfigured routing may cascade; rollback must restore traffic within SLA |
| Security configuration | Hardening errors may lock out systems; rollback must restore access safely |
| Feature flag dependency | Incorrect flag state may expose incomplete features; rollback must restore prior state |
| Third-party integration cutover | Integration downtime may breach SLA; timing must be validated pre-promotion |

## Done Criteria

- Simulation plan covers all executable high-risk steps.
- Rollback drill was executed and every step has a recorded result.
- Gap log is present (may be empty if all steps were simulatable).
- Timing record covers the full promotion and rollback sequence.
- Simulation verdict is explicit: Pass, Pass with conditions, or Fail.
- Release readiness input summary is present and references gap log and timing record.
- Originating plan or workstream ID is on the output.

## Guardrails

- Do not produce a Pass verdict if a rollback step failed during the drill — a failed rollback means the release is not ready.
- Do not skip the gap log because the simulation environment was close to production — document gaps even when small.
- Do not size the promotion window based only on plan estimates; use actual timing from the simulation record.

## References

- Related skills: `release-readiness`, `operability-design`, `test-orchestration`, `acceptance-governance`
