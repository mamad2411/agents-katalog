---
name: autonomous-milestone-run
description: Orchestrate a ratified multi-slice milestone with one lead integrator, bounded subagent assignments, internal senior slice passes, integrated validation, and a senior milestone verdict. Use only after the milestone outcome, authority envelope, acceptance evidence, and escalation conditions are explicit.
---

# Autonomous Milestone Run

This skill coordinates existing engineering passes. It does not weaken their gates or authorize silent scope expansion.

## Preconditions

1. Read `docs/HANDOFF.md`, `docs/SPEC.md`, `docs/DATA_CONTRACT.md`, and `docs/07-ops/autonomous-development-operating-model.md`.
2. Confirm the active milestone contains the fields from `docs/07-ops/autonomous-milestone-template.md`.
3. Inspect current branch, worktree state, existing user changes, and shared-file ownership.
4. Stop if the outcome, authority envelope, external dependencies, or acceptance evidence are too ambiguous to execute safely.

## Build The Execution Graph

1. Decompose the milestone into small coherent slices.
2. Order durable contracts before repositories, routes, providers, read models, and UI consumers.
3. Identify shared files and assign one writer.
4. Mark work that can be investigated in parallel without overlapping writes.
5. Record the slice map and status in `HANDOFF.md`.

## Delegate Safely

Give each subagent one bounded task with:

- objective;
- required source material;
- exact write scope or read-only scope;
- prohibited scope;
- required evidence;
- return format.

Use separate worktrees for parallel writing. Keep final integration, canonical docs, and milestone verdict with the lead agent.

## Execute

For each meaningful slice:

1. Run `.agents/skills/senior-slice-pass`.
2. Inspect relevant prior behavior and classify it.
3. Implement only the current slice.
4. Run focused and proportionate broader verification.
5. Run the closing senior slice pass and fix every `fix now` finding.
6. Update the active contracts and milestone evidence.
7. Create a reversible checkpoint when stable.

Continue through the slice graph unless an operating-model stop condition is reached.

## Integrate

1. Reconstruct the complete user journey and durable data lineage.
2. Run cross-slice tests, database/browser gates, accessibility checks, and optimized build evidence required by the milestone.
3. Run `.agents/skills/senior-milestone-pass`.
4. Fix all `fix before milestone` findings.
5. Record bounded deferrals with owner and activation trigger.
6. Push only when the authority envelope permits it.

## Return

Report:

- outcome and commit range;
- internal slices completed;
- prior-behavior dispositions;
- verification evidence;
- findings and remediation;
- assumptions and external dependencies;
- untested areas;
- rollback or forward-repair posture;
- `ready`, `conditional`, or `hold` verdict.

Do not invoke `.agents/skills/senior-release-pass` unless the user is making a deployment, pilot, migration, or release decision.
