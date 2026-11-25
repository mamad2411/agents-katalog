---
name: feature-implementation
description: Use for end-to-end feature delivery or extension work across Swift, Kotlin/Android, Flutter, Tauri, Rust, and frontend code when the goal is to ship behavior with production-quality defaults, tests, and release-aware validation.
---

# Feature Implementation

## Use when
- the main task is adding or extending product behavior
- the work spans design, implementation, testing, and validation
- the user expects code, not just analysis

## Do not use when
- the task is primarily a bug investigation, refactor-only cleanup, or pure review
- the request is architecture-only and should be settled before coding

## Working rules
- Start from existing patterns in the repo before inventing new abstractions.
- Prefer the smallest complete slice that solves the request cleanly.
- Think through happy path, failure path, interruption path, and recovery path together.
- Keep UI state, domain logic, and transport boundaries explicit.
- Treat accessibility, observability, and rollback awareness as part of implementation quality.

## Workflow
1. Restate the feature in a few precise bullets and identify acceptance criteria.
2. Inspect the relevant code paths, tests, naming, state flow, and UI conventions.
3. Choose the minimum file set and implementation slice required.
4. Implement in small coherent steps.
5. Add or update the narrowest tests that protect the new behavior.
6. Run focused validation first, then broader checks when justified.
7. Self-review for regressions, placeholder content, and release gaps before finishing.

## Quality bar
- No invented APIs or guessed behavior.
- User-visible states are deliberate.
- Public contracts, serialization, permissions, and migrations are handled intentionally.
- The result should be merge-ready by default and release-ready when feasible.

## Reference routing
- Read `references/coding-agent-guidance.md` for repo-first implementation guidance.
- Read `references/platform-ux-checklist.md` for UI and UX quality checks.
- Read `references/release-quality-gates.md` when the change affects product quality, rollout, or user trust.
- Read `references/official-docs.md` only when primary platform guidance changes the implementation.

## Output contract
Provide:
- files changed
- behavior added or modified
- tests or validation added
- commands run and outcomes
- release-readiness status
- real follow-up risks only if they remain
