---
name: tdd-failing-tests-loop
description: This skill should be used when overhauling, refactoring, or hardening a code path with strict failing-tests-first TDD. Apply it when a subsystem needs safer behavior changes, regression coverage, clarified contracts, or code/docs/tests alignment without drifting from the existing product contract.
---

# TDD Failing Tests Loop

## Overview

Turn “use TDD” into a repeatable delivery loop instead of a slogan.

Use this skill to drive a subsystem overhaul by:
- mapping the current contract first
- writing purposeful failing tests before changing implementation
- making the smallest green changes possible
- tightening docs and instructions so the runtime contract, tests, and implementation all agree
- finishing with a clear red → green timeline another agent can audit

## When To Use

Use this skill when:
- a user explicitly asks for TDD, failing tests first, red-green-refactor, or a safe subsystem overhaul
- behavior is spread across code, tests, prompt text, and internal docs
- the current implementation feels brittle and needs contract-driven cleanup
- a refactor needs proof that behavior changed intentionally rather than accidentally
- the right fix is unclear until the expected behavior is stated as tests first

## When Not To Use

Do not use this skill when:
- the task is pure greenfield scaffolding with no meaningful contract to preserve
- the user only wants brainstorming or design discussion without implementation
- the codebase has no runnable test surface and adding one would be larger than the requested change
- the request is a tiny edit where a full red-green loop would add overhead without reducing risk

## Core Workflow

### 1. Map The Existing Contract Before Touching Code

Read only the minimum high-signal inputs needed to state the current behavior:
- internal docs or architectural contracts
- existing focused tests
- implementation files at the likely seam
- any prompt/profile/instruction text that shapes the feature at runtime

Prefer:
- `rg` to find the surface area fast
- targeted file reads instead of bulk-loading whole directories
- starting with docs and tests when the subsystem has a published contract

Summarize the contract in one short list before editing:
1. What behavior must remain true?
2. What behavior is brittle, missing, or contradictory?
3. Which seams are small enough for a safe first red test?

### 2. Choose Behavioral Seams, Not Internal Helpers

Write tests against behavior the team actually cares about:
- visible output
- lifecycle transitions
- durable metadata
- tool gating
- routing decisions
- sync contracts between code and docs/prompts

Avoid starting with:
- implementation-detail helpers already covered by typecheck
- broad integration suites when a smaller focused suite can go red first
- aspirational behavior that the user did not ask for

### 3. Write Purposeful Red Tests First

Add failing tests that each express one contract gap.

Good red tests usually fall into these buckets:
- missing structured metadata
- brittle heuristic that should become explicit state
- instructions/docs/policy no longer matching intended runtime behavior
- regression where user-authored data is misclassified as system-generated
- edge case revealed by the first green pass

Name tests so the failure itself explains the desired behavior.

Prefer 2-4 sharp red tests over a giant speculative batch.

### 4. Run The Smallest Relevant Test Slice

Run the focused suite immediately after writing the tests.

Capture:
- which tests failed
- whether the failures match the intended contract gaps
- any surprise failure that reveals a deeper seam

If the failures are noisy or unrelated, stop and tighten the test surface before changing implementation.

### 5. Make The Smallest Green Change

Change as little as possible to satisfy the new contract:
- add explicit metadata instead of more string heuristics
- preserve backward compatibility when older durable state exists
- prefer one shared seam rather than duplicating fixes in multiple call sites
- preserve unrelated user changes and dirty-worktree state

After each code change, rerun the smallest relevant test slice.

### 6. Refactor Only After The New Contract Is Green

Once the first red tests pass:
- collapse duplicated logic
- move heuristics behind named helpers
- tighten types around the new state
- simplify gates and transitions now that behavior is covered

If a refactor reveals a new edge case, add another failing test first.

### 7. Sync The Human And Agent Contract

If the subsystem has prompt text, internal docs, policy files, or skill instructions:
- update them in the same pass
- make the tests cover the changed contract where practical
- keep policy order, prompt guidance, and implementation behavior aligned

Do not leave docs or agent instructions describing behavior the code no longer implements.

### 8. Broaden Verification Deliberately

Expand from narrow to broad:
1. focused new/edited tests
2. adjacent subsystem suites
3. shared contract suites
4. typecheck or build validation

If a mixed-suite run fails for an unrelated harness reason, isolate it and verify the touched suites directly instead of chasing noise.

### 9. Report The Work As A Red → Green Timeline

Close out with a compact timeline:
- red test
- what failed
- code/doc change
- green result

This makes the TDD process auditable and reusable.

## Default Response Pattern

Use this shape when applying the skill:

1. State the subsystem under test and the first files to inspect.
2. Read the contract and current tests.
3. Add failing tests before implementation changes.
4. Run the focused suite and confirm the failures are the intended ones.
5. Implement the smallest fix.
6. Rerun focused tests.
7. Add any newly discovered edge-case red tests.
8. Sync docs/instructions if part of the contract.
9. Run broader verification.
10. Summarize the red → green timeline and final validation commands.

## Guardrails

- Do not start by rewriting large implementation files without a failing test target.
- Do not add broad snapshot-style tests when a narrower behavioral test will do.
- Do not treat “refactor” as permission to change product behavior silently.
- Do not rely on brittle title or string matching when structured state can express the same contract.
- Do not stop after the first green test if docs, prompts, or adjacent suites still contradict the new behavior.
- Do not commit unrelated workspace files.

## Worked Example

Load this reference for a concrete example of the loop applied to Vesper Factory Production:
- `references/factory-production-example.md`

## Done Criteria

Consider the loop complete only when all are true:
- the intended behavior was expressed as failing tests before implementation changes
- the new behavior passes focused tests
- adjacent impacted suites are green
- typecheck or equivalent structural validation passes
- docs and agent-facing instructions match the new runtime contract
- the final report includes the red → green timeline
