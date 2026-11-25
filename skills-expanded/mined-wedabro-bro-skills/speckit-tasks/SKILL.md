---
name: speckit.tasks
description: Task Breaker - Produce dependency-ordered, verifiable atomic tasks from an approved plan.
---

## Mission
Break a plan into executable tasks that are independently reviewable and verifiable.

## Inputs and Outputs
- Read `spec.md` and `plan.md`; write `.agents/specs/[feature]/tasks.md`.

## Protocol
1. Create Setup, Foundation, user-story, and Polish phases only when applicable; preserve dependency order.
2. Give every task a unique ID, priority, user-story link, exact path, action, dependency, and acceptance check.
3. Keep each task within 15 minutes and at most three files; split oversized work instead of hiding scope.
4. Include failure, security, migration, accessibility, observability, and test tasks when required by the plan.
5. Ensure every requirement maps to at least one task and every task maps back to a requirement or gate.
6. Mark `[P]` only for blocking work; do not pre-check boxes or invent completion evidence.

## Completion Gate
Tasks are atomic, ordered, traceable, path-specific, and each has a concrete verification signal.

## Guard Rails
Do not write implementation code, duplicate tasks, omit dependencies, or create tasks larger than the repository limits.