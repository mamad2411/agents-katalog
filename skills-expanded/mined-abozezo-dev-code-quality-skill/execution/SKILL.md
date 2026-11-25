---
name: execution
description: |
  Implements an approved software plan in small, verifiable increments while preserving the target
  repository's conventions. Hands completed work to verification and review.
  Use when: an implementation plan has been approved and code, configuration, tests, or documentation
  must be changed.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Implementation Execution

## Prerequisite

Start only after the implementation plan is approved. Treat the approved plan as the source of truth for
scope, acceptance criteria, and ordering. If it is absent, incomplete, or conflicts with the repository,
surface the discrepancy and request a clarified plan rather than silently expanding scope.

## Workflow

### 1. Establish the implementation baseline

1. Read the approved plan and restate the current plan item, its acceptance criteria, and its dependencies.
2. Inspect the affected code, neighboring modules, tests, build scripts, and repository guidance before editing.
3. Identify established conventions for naming, module boundaries, error handling, types, formatting, tests,
   documentation, and package tooling.
4. Check the working tree so unrelated changes are not overwritten or folded into the task.

### 2. Implement one small increment at a time

For each plan item, make the smallest coherent change that can be checked independently:

1. Implement only the behavior required by that increment.
2. Update or add the nearest appropriate test, fixture, type, or documentation needed to express its contract.
3. Run the narrowest relevant check immediately (for example, a focused test, type check, formatter, or build
   target).
4. Inspect the diff and correct regressions before starting the next increment.
5. Record any failed check, decision, or deviation from the plan so it can be reported accurately.

Do not batch unrelated refactors with feature work. Preserve public interfaces and backward compatibility unless
the approved plan explicitly changes them. Prefer existing project utilities, components, patterns, and commands
over introducing parallel abstractions or dependencies.

### 3. Apply framework-specific guidance only when needed

For repositories containing React or Next.js code affected by this work, read and follow the local
[`react-best-practices`](../react-best-practices/SKILL.md) skill before editing UI, hooks, components, routes,
or client/server boundaries. Apply it only to React/Next.js implementation work; this skill remains
framework-neutral for every other stack.

### 4. Preserve project conventions

- Use the repository's package manager, task runner, formatter, linter, test framework, and directory layout.
- Match existing naming, import ordering, typing, accessibility, logging, and error-handling conventions.
- Keep changes focused, readable, and reversible; avoid drive-by formatting or generated-file edits unless required.
- Add tests at the same layer and in the same style as adjacent tests.
- Never conceal failures by weakening assertions, disabling checks, swallowing errors, or adding broad exceptions.

### 5. Finish and hand off

After all plan items are implemented:

1. Re-read the approved acceptance criteria and confirm each is covered by the implementation and tests.
2. Run the repository's relevant aggregate checks in addition to the increment-level checks.
3. Prepare a concise handoff for verification and review containing:
   - changed files and the behavior delivered;
   - checks run and their results;
   - known limitations, skipped checks, and follow-up risks;
   - any intentional plan deviations and their rationale.
4. Hand the change to the verification and review workflow. In this repository, use
   [`code-verify-and-clean-skill`](../code-verify-and-clean-skill/SKILL.md) for the final validation and review.

## Completion Criteria

Implementation is complete only when every approved plan item is addressed, each increment has been checked,
repository conventions are preserved, and the verification/review handoff includes sufficient evidence to assess
the change independently.
