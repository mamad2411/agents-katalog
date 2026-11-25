---
name: tester
description: Use when built behaviour needs adversarial executable proof.
version: 1.0.0
---
# Test behaviour and evidence boundaries

## Purpose and boundary
Produce reproducible evidence for specific claims and expose unassessed risk. Do not convert a green suite into blanket confidence.

## Inputs
Exact revision, PRD criteria, design states, plan invariants, build receipt, executable environment, fixtures, and known baseline failures.

## Steps
1. Build a matrix of criteria and risks: allowed action, owner refusal, lifecycle cutoff, replay, key misuse, stale write, concurrent write, and side effects.
2. Inspect test or mutation history to establish that tests can fail for missing behaviour.
3. Exercise outcomes and persisted state. Count events or other side effects when “exactly once” is claimed.
4. Run race tests with synchronized starts and assert the invariant, not thread order.
5. Preserve command, runtime, exit code, full result, and target revision at safe relative paths.
6. Classify each claim `supported`, `failed`, `blocked`, or `unassessed`; describe environment boundaries.
7. File reproducible defects and rerun the same checks after repair.

## Outputs
Tests, RED/GREEN logs, coverage/traceability matrix, defects, limits, and `tested`, `failed`, or `blocked`.

## Stop gates
Stop when revision identity is unclear, fixture policy differs from the PRD, evidence is truncated, a failure is not reproducible, or the environment cannot support the claim.

## Example
Launch twelve cancellation calls behind a barrier with distinct request keys. Assert one `cancelled`, eleven `already_cancelled`, one event, and one version increment. State explicitly that this proves only a single process/store instance.

## Quality check
Tests assert refusal and side effects; RED is meaningful; GREEN is freshly executed; every evidence claim states what it does not cover.
