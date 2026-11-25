---
name: idempotency-side-effects-discipline
description: Define idempotency keys, retry policy, deduplication, and delivery guarantees for side-effectful operations. Use for integrations, jobs, and handlers.
---

# Idempotency and Side-Effects Discipline

## Goal
Prevent duplicate or inconsistent side effects under retries.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Operation table with guarantee choice: at-least-once or exactly-once rationale.

## Verify Gate
Document replay behavior and duplicate suppression checks.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
