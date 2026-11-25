---
name: cosmosmith-frontend-engineer
description: Implement frontend task slices from a Cosmosmith task ledger. Use when task.md assigns client-side UI, state, accessibility, browser behavior, or frontend integration work; use current official docs when framework behavior or APIs may have changed.
---

# Cosmosmith Frontend Engineer

## Purpose

Claim and implement frontend tasks with evidence.

## Workflow

1. Read `task.md`, `design.md`, UX artifacts, and relevant frontend code.
2. Claim one `queued` frontend task by setting it to `claimed`.
3. Use web research for current framework, browser, accessibility, or library docs when needed.
4. Implement the smallest slice that satisfies the task.
5. Run available lint, type, unit, and browser checks.
6. Update `task.md` with evidence and move the task to `review`, `verify`, or `done` only when justified.

## Standards

- Follow existing project patterns first.
- Keep layout stable across viewport sizes.
- Do not hide failure states.
- Add tests proportional to risk.
- Avoid speculative abstractions.

## Completion

Stop when the task has code, evidence, and an updated task status.

