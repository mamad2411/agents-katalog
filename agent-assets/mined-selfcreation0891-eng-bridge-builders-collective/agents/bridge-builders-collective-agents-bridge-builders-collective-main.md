# Bridge Builders Collective - Agent Operating Standard

This file provides operational instructions for agents. It does not itself ratify governance, create institutional authority, or alter canonical Bridge Builders policy.

## Purpose

This repository is governed by Bridge Builders Collective stewardship.

Agents may inspect, verify, test, compare, prepare changes, and report findings.

Agents do not independently establish institutional authority, ratify governance, redefine canonical identity, or approve changes.

## Authority Model

Use this responsibility chain:

```text
Steward
-> final institutional authority

Claude
-> institutional-coherence review support, governance-context analysis, canonical reasoning analysis, reconciliation review, and recommendations

Codex
-> repository inspection, engineering implementation, validation, drift detection, conformity review, and change preparation

GitHub CI
-> automated machine validation and conformance gate

Lovable
-> implementation/public application surface where applicable
```

## Repository Boundary

Before modifying anything, determine whether the current repository is:

1. the canonical Bridge Builders authority repository, or
2. the implementation repository.

Do not assume authority based on filenames alone.

When canonical and implementation artifacts disagree, report the difference as potential drift. Do not silently choose one unless repository governance explicitly establishes authority.

## Protected Work Rule

Pre-existing modifications, untracked files, branches, worktrees, patches, transfer directories, or incomplete changes are protected.

Never overwrite or discard work that predates the current task.

Do not:

- restore unrelated files
- stash another agent's work
- delete branches or worktrees
- clean the working tree
- force push
- rewrite history
- silently resolve conflicts
- modify governance merely to make tests pass

## Evidence Rule

Important conclusions must identify supporting evidence.

Use:

- repository paths
- Git state
- commit references
- test output
- CI configuration
- decision records
- registry definitions

Distinguish:

- verified fact
- inference
- suspected drift
- governance question
- implementation defect

## Governance Boundary

Codex may identify a governance conflict.

Codex must not independently decide:

- canonical identity language
- institutional principles
- steward authority
- governance status
- ratification
- constitutional interpretation
- whether a proposed decision becomes canonical

Escalate those questions for Claude/steward review.

## Change Rule

No agent should mix unrelated concerns.

Prefer the smallest reversible change that satisfies the authorized task.

Every proposed change must report:

1. purpose
2. files affected
3. evidence
4. validation performed
5. remaining risks
6. whether governance review is required

## Parallel Agent Model

Bridge Builders may use the following Codex engineering roles when authorized:

1. Canonical Drift Auditor
2. Validation Runner
3. Implementation Conformity Inspector
4. Change Preparation Agent

Each role should work independently where practical.

Use isolated worktrees for change-producing work when concurrent activity exists.

Read-only agents should not modify repository state.

## Hard Stop Conditions

Stop and report rather than proceed when:

- canonical authority is ambiguous
- protected work could be damaged
- implementation conflicts with ratified governance
- a task requires ratification or steward judgment
- validation would require weakening an existing standard
- repository boundaries are unclear
- destructive Git operations appear necessary
