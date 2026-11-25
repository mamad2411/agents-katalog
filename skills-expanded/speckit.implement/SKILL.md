---
name: speckit.implement
description: Code Builder (Anti-Regression) - Deploy code in tasks with IRONCLAD protocols.
---

## Mission
Execute approved implementation tasks atomically, safely, and test-first while enforcing anti-regression gates, deviation rules, and runtime consistency.

## Inputs and Outputs
- Read `.agents/specs/[feature]/tasks.md`, `plan.md`, `spec.md`, and `.agents/memory/constitution.md`.
- Modify source code, configuration, tests, and task tracking checkboxes; maintain atomic git commits.

## Protocol
1. Respect the 15-Minute Rule: each task must be atomic, touching at most 3 files with verifiable acceptance criteria.
2. Analyze blast radius before modifying code; choose direct targeted edit for isolated changes or Strangler Pattern for complex refactoring.
3. Apply TDD red-green cycle: reproduce failure or create unit test first, implement minimal passing code, then verify.
4. Re-anchor context against `constitution.md` every 3 tasks to guarantee adherence to Docker-first, ENV-first, and coding standards.
5. Handle deviations autonomously:
   - In-scope bugs: fix immediately and verify.
   - Missing critical files/configs: add with documented rationale.
   - Blockers: perform systematic root cause analysis before escalating.
   - Architectural shifts: STOP and request explicit user confirmation.
6. Verify after every task with targeted tests, linters, or type checks; run the full build/test suite at phase boundaries in Docker.

## Completion Gate
All task acceptance criteria met, targeted and suite tests pass with zero regression, task checkbox marked, and atomic conventional commit created.

## Guard Rails
Never commit failing code. Never hardcode secrets, tokens, or environment values. Never exceed task scope without updating plan or tasks.
